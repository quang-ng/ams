from django import forms
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import get_user_model

from asset.models import Activity, ActivityCategory
from asset.models import EXPENSE

from django.forms import Select
from django.conf import settings
from djmoney.forms import MoneyWidget

User = get_user_model()


class UserCacheMixin:
    user_cache = None


class DateInput(forms.DateInput):
    input_type = "date"

class BlankWidget(Select):
    template_name = "asset/django-money/fake-widget.html"


class NoCurrencyMoneyWidget(MoneyWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, currency_widget=BlankWidget)

    def value_from_datadict(self, data, files, name):
        val = super().value_from_datadict(data, files, name)
        if val[1] is None:
            val[1] = settings.DEFAULT_CURRENCY
        return val


class InsertActivityForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "activity_type" in self.data:
            try:
                activity_type = self.data.get("activity_type")
                self.fields["category"].queryset = ActivityCategory.objects.filter(
                    activity_type=activity_type
                ).order_by("id")
            except (ValueError, TypeError):
                pass
        else:
            self.fields["category"].queryset = ActivityCategory.objects.filter(
                activity_type=EXPENSE
            ).order_by("id")
# 
        # self.fields['amount'].widget.attrs['class'] = "form-control col-xs-3"

    class Meta:
        model = Activity
        fields = [
            "activity_type",
            "category",
            "input_date",
            "amount",
            "funding_sources",
            "notes",
        ]

        widgets = {
            "input_date": DateInput(),
            "notes": forms.Textarea(attrs={"rows": 3}),
            "amount": NoCurrencyMoneyWidget
        }
        field_order = fields
        labels = {
            "activity_type": "Họat động",
            "category": "Danh mục",
            "input_date": "Ngày thực hiện",
            "amount": "Số tiền",
            "funding_sources": "Nguồn tiền",
            "notes": "Ghi chú riêng",
        }
