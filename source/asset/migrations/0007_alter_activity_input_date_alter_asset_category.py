# Generated by Django 4.2.3 on 2023-07-13 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("asset", "0006_alter_activity_notes"),
    ]

    operations = [
        migrations.AlterField(
            model_name="activity",
            name="input_date",
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name="asset",
            name="category",
            field=models.CharField(
                choices=[
                    ("CASH", "Tiền mặt"),
                    ("FIXED_TERM_SAVINGS", "Sổ tiết kiệm"),
                    ("FINANCIAL_ASSETS", "Tài sản tài chính"),
                    ("REAL_ESTATE", "Bất động sản"),
                    ("OTHERS", "Khác"),
                ],
                default="CASH",
                max_length=50,
            ),
        ),
    ]
