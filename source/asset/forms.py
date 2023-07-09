from django import forms
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import get_user_model

from asset.models import Activity, ActivityCategory
from asset.models import EXPENSE

User = get_user_model()


class UserCacheMixin:
    user_cache = None


class DateInput(forms.DateInput):
    input_type = "date"


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
