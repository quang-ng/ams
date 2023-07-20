from django.db import models
from accounts.models import MyUser
from djmoney.models.fields import MoneyField


EXPENSE = "EXPENSE"
INCOME = "INCOME"

ACTIVITY_TYPE_CHOICES = [(EXPENSE, "Chi"), (INCOME, "Thu")]


FINANCIAL_ASSETS = "FINANCIAL_ASSETS"
REAL_ESTATE = "REAL_ESTATE"
CASH = "CASH"
FIXED_TERM_SAVINGS = "FIXED_TERM_SAVINGS"
OTHERS = "OTHERS"
ASSERT_CATEGORIES = [
    (CASH, "Tiền mặt"),
    (FIXED_TERM_SAVINGS, "Sổ tiết kiệm"),
    (FINANCIAL_ASSETS, "Tài sản tài chính"),
    (REAL_ESTATE, "Bất động sản"),
    (OTHERS, "Khác"),
]


class ActivityCategory(models.Model):
    name = models.TextField(max_length=200, blank=False)
    activity_type = models.CharField(
        max_length=10,
        choices=ACTIVITY_TYPE_CHOICES,
        default=EXPENSE,
    )

    def __str__(self):
        return self.name


class Asset(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    name = models.TextField(max_length=200, blank=False)
    amount = MoneyField(max_digits=19, decimal_places=2, default_currency="VND")
    category = models.CharField(
        max_length=50,
        choices=ASSERT_CATEGORIES,
        default=CASH,
    )

    def __str__(self):
        return self.name

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
    amount = MoneyField(max_digits=19, decimal_places=2, default_currency="VND")
    category = models.CharField(
        max_length=50,
        choices=LIABILITY_CATEGORIES,
        default=CREDIT_CARD,
    )

    def __str__(self):
        return self.name

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
    input_date = models.DateField()
    amount = MoneyField(max_digits=19, decimal_places=2, default_currency="VND")

    CREDIT_CARD = "CREDIT CARD"
    SHORT_TERM_DEBT = "SHORT-TERM DEBT"
    LONG_TERM_DEBT = "LONG-TERM DEBT"
    CASH = "CASH"

    FUNDING_SOURCE_CATEGORIES = [
        (CASH, "Tiền mặt"),
        (CREDIT_CARD, "Thẻ tín dụng"),
        (SHORT_TERM_DEBT, "Khoản nợ ngắn hạn"),
        (LONG_TERM_DEBT, "Khoản nợ giải hạn"),
    ]

    funding_sources = models.CharField(
        max_length=50,
        choices=FUNDING_SOURCE_CATEGORIES,
        default=CASH,
    )
    notes = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
