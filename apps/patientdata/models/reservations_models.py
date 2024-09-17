from django.db import models
from django.urls import reverse
from django.utils.timezone import now

import os

# import random

# import barcode
# from barcode.writer import ImageWriter

# from io import BytesIO
# from django.core.files import File
from apps.configurations.models import BasicData


# current = timezone.now


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


# def upload_image_path(instance, filename):
#     new_filename = random.randint(1, 3910209312)
#     name, ext = get_filename_ext(filename)
#     final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
#     return "patients/{new_filename}/{final_filename}".format(
#         new_filename=new_filename, final_filename=final_filename
#     )


# Create your models here.
class PatientReservation(BasicData):
    patient = models.ForeignKey(
        "patientdata.Patients",
        related_name="patient_reservation_of_patient",
        related_query_name="patient",
        on_delete=models.CASCADE,
    )

    start_date = models.DateTimeField(default=now, blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    # phone = models.CharField(max_length=150, blank=True, null=True)

    # mobile = models.CharField(max_length=30, blank=True, null=True)
    # cardid = models.CharField(max_length=20, blank=True, null=True)
    # barcode = models.CharField(max_length=20, blank=True, null=True)
    # barurl = models.CharField(max_length=80, blank=True, null=True)
    # barimg = models.ImageField(upload_to="patients", null=True, blank=True)

    class Meta:
        app_label = "patientdata"
        verbose_name = "patient_reservation"
        verbose_name_plural = "Patients Reservations"

    def __str__(self):
        return "{}".format(self.name)

    def edit_reservation_url(self):
        # return "/clinic/edit/{}/".format(self.id)
        return reverse("patientdata:edit_reservation", kwargs={"id": self.id})

    # Override the save method
    # def save(self, *args, **kwargs):
    #     # Call the create_barcode method before saving
    #     if not self.barimg:  # Create a new barcode if it doesn't already exist
    #         self.create_barcode()

    #     super().save(*args, **kwargs)  # Save the model after creating barcode
