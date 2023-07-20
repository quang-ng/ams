from datetime import datetime
from typing import Any, Dict
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from django.shortcuts import redirect
from django.contrib import messages
from djmoney.money import Money
from django.conf import settings
from django.views.generic import ListView
from datetime import datetime, timedelta, date

from asset.forms import InsertActivityForm
from asset.models import ActivityCategory
from asset.models import Activity
from asset.models import INCOME, EXPENSE
from asset.models import Asset
from asset.models import CASH
from asset.models import Liability
from accounts.models import MyUser
from asset.forms import AssetLiquidationProcessForm


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


class ListActivityView(LoginRequiredMixin, ListView):
    paginate_by = 5
    model = Activity
    template_name = "asset/list_activity.html"
    ordering = ["-input_date"]

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        summary_data = {}
        for activity in queryset:
            if activity.category.name not in summary_data:
                summary_data[activity.category.name] = {INCOME: 0, EXPENSE: 0}

            summary_data[activity.category.name][activity.activity_type] += int(
                activity.amount.amount
            )

        chart_data = []
        for k, v in summary_data.items():
            chart_data.append({"label": k, "data": [v[INCOME], v[EXPENSE]]})

        import json

        chart_data_json_str = json.dumps(chart_data)

        print("CCC: ", chart_data_json_str)
        context["chart_data_json_str"] = chart_data_json_str

        return context

    def get_queryset(self):
        user = self.request.user

        users_in_family = MyUser.objects.filter(family=user.family)

        queryset = Activity.objects.filter(user__in=users_in_family).order_by(
            "-input_date"
        )

        input_date_filter = self.request.GET.get("input_date")
        datefilter = self.request.GET.get("datefilter")

        if input_date_filter == "last_7_days":
            queryset = queryset.filter(
                input_date__gte=datetime.now() - timedelta(days=7)
            )
        elif input_date_filter == "last_30_days":
            queryset = queryset.filter(
                input_date__gte=datetime.now() - timedelta(days=30)
            )
        elif input_date_filter == "last_month":
            last_day_of_prev_month = date.today().replace(day=1) - timedelta(days=1)
            start_day_of_prev_month = date.today().replace(day=1) - timedelta(
                days=last_day_of_prev_month.day
            )
            queryset = queryset.filter(
                input_date__range=(start_day_of_prev_month, last_day_of_prev_month)
            )

        elif datefilter:
            dates = self.request.GET.get("datefilter").split("-")
            from_date = datetime.strptime(dates[0].strip(), "%d/%m/%Y")
            to_date = datetime.strptime(dates[1].strip(), "%d/%m/%Y")
            queryset = queryset.filter(input_date__range=(from_date, to_date))

        self.queryset = queryset
        return self.queryset


class AssetLiquidationProcessView(LoginRequiredMixin, FormView):
    template_name = "asset/asset_liquidation_process.html"
    form_class = AssetLiquidationProcessForm
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
