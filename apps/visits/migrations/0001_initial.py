# Generated by Django 5.0 on 2024-07-20 11:36

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('patientdata', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visitdate', models.DateField(blank=True, default=datetime.date.today, null=True)),
                ('complain', models.TextField(blank=True, default='comp', null=True)),
                ('sign', models.TextField(blank=True, default='sign', null=True)),
                ('diagnosis', models.CharField(blank=True, max_length=150, null=True)),
                ('intervention', models.CharField(blank=True, max_length=150, null=True)),
                ('amount', models.IntegerField(default=0)),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='patientdata.patients')),
            ],
        ),
    ]
