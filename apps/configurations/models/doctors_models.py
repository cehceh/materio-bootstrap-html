from django.db import models
from django.utils.translation import gettext_lazy as _
from .conf_models import BasicData


class DoctorSpecializations(BasicData):
    name = models.CharField(
        max_length=100, unique=True, verbose_name="Doctor Specialization"
    )
    name_ar = models.CharField(
        max_length=100,
        unique=False,
        blank=True,
        null=True,
        verbose_name="Arabic Specialization",
    )
    # doctor = models.OneToOneField(
    #     DoctorNames,
    #     related_name="doctor_name_specializations",
    #     on_delete=models.CASCADE,
    # )
    code = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name=_("Code"),
    )

    description = models.TextField(blank=True, null=True)
    updated_user = models.ForeignKey(
        "users.CustomUser",
        related_name="user_make_doctor_specialization_changes",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        app_label = "configurations"
        verbose_name = "doctor_specialization"
        verbose_name_plural = "Doctor Specializations"
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

    def save(self, *args, **kwargs):
        generated_code = "spec-" + str(self.id)
        # Only generate a code if it doesn't already exist
        if not self.code:
            super().save(*args, **kwargs)  # Save to generate the ID first
            self.code = (
                generated_code  # "spec-" + str(self.id)  # Create code based on ID
            )
        super().save(*args, **kwargs)  # Save again to store the updated code

    def __str__(self):
        return f"{self.name} - {self.name_ar}"


class DoctorNames(BasicData):
    name = models.CharField(max_length=100, unique=True, verbose_name="Doctor Name")
    code = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name=_("Code"),
    )
    specializations = models.ManyToManyField(
        DoctorSpecializations,
        related_name="doctors_specializations",
        # on_delete=models.CASCADE,
    )

    mobile1 = models.CharField(
        max_length=25, default="", unique=False, verbose_name=_("Mobile1")
    )
    mobile2 = models.CharField(
        max_length=25, blank=True, null=True, verbose_name=_("Mobile2")
    )
    phone1 = models.CharField(
        max_length=25, blank=True, null=True, verbose_name=_("Phone1")
    )
    phone2 = models.CharField(
        max_length=25, blank=True, null=True, verbose_name=_("Phone2")
    )

    description = models.TextField(blank=True, null=True)
    updated_user = models.ForeignKey(
        "users.CustomUser",
        related_name="user_make_doctornames_changes",
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

    def save(self, *args, **kwargs):
        # Only generate a code if it doesn't already exist
        if not self.code:
            super().save(*args, **kwargs)  # Save to generate the ID first
            self.code = "doctor-" + str(self.id)  # Create code based on ID
        super().save(*args, **kwargs)  # Save again to store the updated code

    def __str__(self):
        return f"{self.name}"
