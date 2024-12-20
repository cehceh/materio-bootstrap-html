# Generated by Django 5.0 on 2024-09-09 07:36

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patientdata', '0004_alter_patients_barcode'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=False, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Deleted')),
                ('deleted_at', models.DateTimeField(auto_now=True)),
                ('start_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient_reservation_of_patient', related_query_name='patient', to='patientdata.patients')),
            ],
            options={
                'verbose_name': 'patient_reservation',
                'verbose_name_plural': 'Patients Reservations',
            },
        ),
    ]
