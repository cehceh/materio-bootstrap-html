from django.db import models
from django.utils.translation import gettext_lazy as _

from . import BasicData, DoctorSpecializations


class ClinicName(BasicData):
    name = models.CharField(max_length=100, unique=True, verbose_name="Clinic Name")
    doctor_specialization = models.OneToOneField(
        DoctorSpecializations,
        related_name="doctor_specializations_clinic",
        on_delete=models.CASCADE,
    )
    code = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name=_("Code"),
    )
    description = models.TextField(blank=True, null=True)
    updated_user = models.ForeignKey(
        "users.CustomUser",
        related_name="user_make_clinic_name_changes",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        app_label = "configurations"
        verbose_name = "clinic_names"
        verbose_name_plural = "Clinic Name"
        indexes = [
            ##BasicData
            models.Index(fields=["name"]),
            models.Index(fields=["code"]),
            models.Index(fields=["active"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
            models.Index(fields=["is_deleted"]),
            models.Index(fields=["deleted_at"]),
        ]

    def __str__(self):
        return f"{self.name}"


class CreateClinic(BasicData):
    name = models.ForeignKey(
        ClinicName,
        related_name="create_clinic_name",
        on_delete=models.CASCADE,
        verbose_name="Clinic Name",
    )
    # doctor = models.ForeignKey(
    #     DoctorSpecializations,
    #     related_name='doctor_create_clinic',
    #     on_delete=models.CASCADE
    # )

    # doctor = models.OneToOneField(
    #     DoctorNames,
    #     related_name="doctor_name_specializations",
    #     on_delete=models.CASCADE,
    # )
    code = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name=_("Code"),
    )

    description = models.TextField(blank=True, null=True)
    updated_user = models.ForeignKey(
        "users.CustomUser",
        related_name="user_make_clinic_changes",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        app_label = "configurations"
        verbose_name = "doctor_names"
        verbose_name_plural = "Doctor Names"
        indexes = [
            ##BasicData
            models.Index(fields=["name"]),
            models.Index(fields=["code"]),
            models.Index(fields=["active"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
            models.Index(fields=["is_deleted"]),
            models.Index(fields=["deleted_at"]),
        ]

    def __str__(self):
        return f"{self.doctor}: {self.name}"
