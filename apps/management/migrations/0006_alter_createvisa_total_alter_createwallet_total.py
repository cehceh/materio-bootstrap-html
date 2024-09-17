# Generated by Django 4.2.5 on 2024-01-06 17:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("management", "0005_remove_createwallet_balance_createvisa_total_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="createvisa",
            name="total",
            field=models.DecimalField(
                blank=True,
                decimal_places=3,
                default=0.0,
                max_digits=15,
                null=True,
                verbose_name="Visa Balance",
            ),
        ),
        migrations.AlterField(
            model_name="createwallet",
            name="total",
            field=models.DecimalField(
                blank=True,
                decimal_places=3,
                default=0.0,
                max_digits=15,
                null=True,
                verbose_name="Wallet Amount",
            ),
        ),
    ]
