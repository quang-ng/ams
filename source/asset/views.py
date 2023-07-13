from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from django.shortcuts import redirect
from django.contrib import messages
from djmoney.money import Money
from django.conf import settings

from asset.forms import InsertActivityForm
from asset.models import ActivityCategory
from asset.models import Activity
from asset.models import INCOME, EXPENSE
from asset.models import Asset
from asset.models import CASH
from asset.models import Liability


def load_category(request):
    activity_type = request.GET.get("activity_type")
    categories = ActivityCategory.objects.filter(activity_type=activity_type).order_by(
        "id"
    )
    return render(
        request,
        "asset/category_ city_dropdown_list_options.html",
        {"categories": categories},
    )


class InsertActivityView(LoginRequiredMixin, FormView):
    template_name = "asset/new_activity.html"
    form_class = InsertActivityForm

    def get_initial(self):
        initial = super().get_initial()
        initial["input_date"] = datetime.now()
        initial["category"] = (
            ActivityCategory.objects.filter(activity_type=EXPENSE)
            .order_by("id")
            .first()
        )
        return initial

    def form_valid(self, form):
        user = self.request.user
        activity = Activity(**form.cleaned_data, user=user)
        activity.save()

        if activity.activity_type == INCOME:
            self.income_process(user, activity)
        else:
            if activity.funding_sources == CASH:
                self.expense_cash_process(user, activity)
            else:
                self.expnse_non_cash_process(user, activity)

        return redirect("asset:new_activity")

    def expnse_non_cash_process(self, user, activity):
        liability, _ = Liability.objects.get_or_create(
            user=user,
            category=activity.funding_sources,
            defaults={
                "name": activity.funding_sources,
                "amount": Money(0, settings.DEFAULT_CURRENCY),
            },
        )
        liability.amount.amount += activity.amount.amount
        liability.save()
        messages.success(
            self.request,
            ("Lưu hoạt động thành công. Đã cập nhật khoản nợ tương ứng"),
        )

    def income_process(self, user, activity):
        cash_asset, _ = Asset.objects.get_or_create(
            user=user,
            category=CASH,
            defaults={
                "name": "Tiền mặt",
                "amount": Money(0, settings.DEFAULT_CURRENCY),
            },
        )
        cash_asset.amount.amount += activity.amount.amount
        cash_asset.save()

        messages.success(
            self.request,
            ("Lưu hoạt động thành cộng. Đã tăng tài sản tiền mặt tương ứng"),
        )

    def expense_cash_process(self, user, activity):
        cash_asset, _ = Asset.objects.get_or_create(
            user=user,
            category=CASH,
            defaults={
                "name": "Tiền mặt",
                "amount": Money(0, settings.DEFAULT_CURRENCY),
            },
        )
        if cash_asset.amount >= activity.amount:
            cash_asset.amount.amount -= activity.amount.amount
            messages.success(
                self.request,
                ("Lưu hoạt động thành cộng. Đã giảm tài sản tiền mặt tương ứng"),
            )
        else:
            cash_asset.amount.amount = 0
            short_debit = activity.amount.amount - cash_asset.amount.amount
            short_debit_liability, _ = Liability.objects.get_or_create(
                user=user,
                category=Liability.SHORT_TERM_DEBT,
                defaults={
                    "name": "Nợ ngắn hạn",
                    "amount": Money(0, settings.DEFAULT_CURRENCY),
                },
            )

            short_debit_liability.amount.amount += short_debit
            short_debit_liability.save()

            messages.success(
                self.request,
                (
                    "Lưu hoạt động thành công. Bạn không còn đủ tiền mặt, đã tạo một khoản nợ ngăn "
                    f"hạn trị giá {short_debit}."
                ),
            )

        cash_asset.save()
