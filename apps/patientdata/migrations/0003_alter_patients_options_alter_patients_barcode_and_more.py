# Generated by Django 5.0 on 2024-08-23 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patientdata', '0002_alter_patients_mobile_alter_patients_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='patients',
            options={'verbose_name': 'patients', 'verbose_name_plural': 'Patients'},
        ),
        migrations.AlterField(
            model_name='patients',
            name='barcode',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='patients',
            name='barurl',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
    ]
