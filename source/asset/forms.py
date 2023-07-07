from datetime import timedelta

from django import forms
from django.forms import ValidationError
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import get_user_model

from asset.models import (
    ACTIVITY_TYPE_CHOICES,
    ActivityCategory,
    Asset,
    Liability,
    Activity,
)

User = get_user_model()


class UserCacheMixin:
    user_cache = None


class DateInput(forms.DateInput):
    input_type = "date"


class InsertActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = [
            "activity_type",
            "category",
            "input_date",
            "amount",
            "asset",
            "liability",
            "notes",
        ]
        widgets = {
            "input_date": DateInput(),
            'notes': forms.Textarea(attrs={'rows':3})
        }
        field_order = fields
