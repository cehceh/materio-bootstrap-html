# Generated by Django 4.2.5 on 2024-08-06 06:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("management", "0009_createwallet_wallet_name_createwallet_wallet_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="createvisa",
            name="is_client",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name="createwallet",
            name="is_client",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddIndex(
            model_name="createvisa",
            index=models.Index(
                fields=["is_client"], name="management__is_clie_4c1b76_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="createwallet",
            index=models.Index(
                fields=["is_client"], name="management__is_clie_4f9b2d_idx"
            ),
        ),
    ]
