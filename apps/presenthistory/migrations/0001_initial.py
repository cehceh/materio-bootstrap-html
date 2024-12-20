# Generated by Django 5.0 on 2024-07-26 12:48

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('patientdata', '0002_alter_patients_mobile_alter_patients_name'),
        ('visits', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PresentHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visitdate', models.DateField(blank=True, default=datetime.date.today, null=True)),
                ('temprature', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=5)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=5)),
                ('height', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=5)),
                ('cholestrol', models.CharField(blank=True, max_length=150, null=True)),
                ('pulse', models.CharField(blank=True, max_length=150, null=True)),
                ('bloodpr', models.CharField(blank=True, max_length=150, null=True)),
                ('bsl', models.CharField(blank=True, max_length=150, null=True)),
                ('hb', models.CharField(blank=True, max_length=150, null=True)),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='patientdata.patients')),
                ('visit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='visits.visits')),
            ],
        ),
    ]
