from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from django.shortcuts import redirect
from django.contrib import messages
from djmoney.money import Money


from asset.forms import InsertActivityForm
from asset.models import ActivityCategory
from asset.models import Activity
from asset.models import INCOME, EXPENSE
from asset.models import Asset
from asset.models import CASH


def load_category(request):
    activity_type = request.GET.get('activity_type')
    categories = ActivityCategory.objects.filter(activity_type=activity_type).order_by('id')
    return render(request, 'asset/category_ city_dropdown_list_options.html', {'categories': categories})

class InsertActivityView(LoginRequiredMixin, FormView):
    template_name = "asset/new_activity.html"
    form_class = InsertActivityForm


    def get_initial(self):
        initial = super().get_initial()
        initial['input_date'] = datetime.now()
        return initial

    def form_valid(self, form):
        user = self.request.user
        
        activity = Activity(**form.cleaned_data, user=user)
        activity.save()


        if activity.activity_type == INCOME:
            # Increase cash asset
            cash_asset = Asset.objects.filter(user=user, category=CASH).first()
            if not cash_asset:
                cash_asset = Asset(
                    user=user,
                    name="Tiền mặt",
                    amount=Money(0, 'VND'),
                    category=CASH
                )
                cash_asset.save()
            cash_asset.amount.amount += activity.amount.amount
            cash_asset.save()

            messages.success(
                self.request,
                (
                    "Lưu hoạt động thành cộng. Đã tăng tài sản tiền mặt tương ứng"
                ),
            )
        # else:



        return redirect("asset:new_activity")
