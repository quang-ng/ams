from django.db import models
from accounts.models import MyUser


EXPENSE = "EXPENSE"
INCOME = "INCOME"

ACTIVITY_TYPE_CHOICES = [(EXPENSE, EXPENSE), (INCOME, INCOME)]


class ActivityCategory(models.Model):
    name = models.TextField(max_length=200, blank=False)
    activity_type = models.CharField(
        max_length=10,
        choices=ACTIVITY_TYPE_CHOICES,
        default=EXPENSE,
    )


class Asset(models.Model):
    FINANCIAL_ASSETS = "FINANCIAL_ASSETS"
    REAL_ESTATE = "REAL_ESTATE"
    CASH = "CASH"
    FIXED_TERM_SAVINGS = "FIXED_TERM_SAVINGS"
    OTHERS = "OTHERS"
    ASSERT_CATEGORIES = [
        (FINANCIAL_ASSETS, FINANCIAL_ASSETS),
        (REAL_ESTATE, REAL_ESTATE),
        (CASH, CASH),
        (FIXED_TERM_SAVINGS, FIXED_TERM_SAVINGS),
        (OTHERS, OTHERS),
    ]

    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    name = models.TextField(max_length=200, blank=False)
    amount = models.BigIntegerField()
    category = models.CharField(
        max_length=50,
        choices=ASSERT_CATEGORIES,
        default=CASH,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Liability(models.Model):
    CREDIT_CARD = "CREDIT CARD"
    SHORT_TERM_DEBT = "SHORT-TERM DEBT"
    LONG_TERM_DEBT = "LONG-TERM DEBT"

    LIABILITY_CATEGORIES = [
        (CREDIT_CARD, CREDIT_CARD),
        (SHORT_TERM_DEBT, SHORT_TERM_DEBT),
        (LONG_TERM_DEBT, LONG_TERM_DEBT),
    ]
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    name = models.TextField(max_length=200, blank=False)
    amount = models.BigIntegerField()
    category = models.CharField(
        max_length=50,
        choices=LIABILITY_CATEGORIES,
        default=CREDIT_CARD,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Activity(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    activity_type = models.CharField(
        max_length=10,
        choices=ACTIVITY_TYPE_CHOICES,
        default=EXPENSE,
    )
    category = models.ForeignKey(ActivityCategory, on_delete=models.CASCADE)
    input_date = models.DateTimeField()
    notes = models.TextField(null=True)
    amount = models.BigIntegerField()
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, null=True)
    liability = models.ForeignKey(Liability, on_delete=models.CASCADE, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
