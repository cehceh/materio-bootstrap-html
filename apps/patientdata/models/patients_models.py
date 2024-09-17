from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import now

# from phonenumber_field.modelfields import PhoneNumberField
import os
import random

import barcode
from barcode.writer import ImageWriter

# from barcode import EAN13
from io import BytesIO
from django.core.files import File

# import subprocess
# import os
# import code128

# from datetime import date
# import random

current = timezone.now


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return "patients/{new_filename}/{final_filename}".format(
        new_filename=new_filename, final_filename=final_filename
    )


# Create your models here.
class Patients(models.Model):
    name = models.CharField(max_length=200, unique=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    birth_date = models.DateField(default=now, blank=True, null=True)
    age = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=150, blank=True, null=True)

    mobile = models.CharField(max_length=30, blank=True, null=True)
    cardid = models.CharField(max_length=20, blank=True, null=True)
    barcode = models.CharField(max_length=20, blank=True, null=True)
    barurl = models.CharField(max_length=80, blank=True, null=True)
    barimg = models.ImageField(upload_to="patients", null=True, blank=True)

    class Meta:
        app_label = "patientdata"
        verbose_name = "patients"
        verbose_name_plural = "Patients"

    def __str__(self):
        return "{}".format(self.name)

    def edit_patient_url(self):
        # return "/clinic/edit/{}/".format(self.id)
        return reverse("patientdata:edit_patient", kwargs={"id": self.id})

    def create_barcode(self):
        print("I AM HERE IN CREATE BARCODE")
        number = str(random.randint(1000000000000, 9999999999999))
        print("NUMBER*************************", number)
        EAN = barcode.get_barcode_class("ean13")

        print("EAN****************************", EAN)
        my_ean = EAN(number, writer=ImageWriter())
        print("my_ean****************************", my_ean)

        ## Save barcode image
        buffer = BytesIO()
        my_ean.write(buffer)  # * uncomment this line make it work as expected
        barcode_image = File(buffer)

        # print("barcode_image****************************", barcode_image)
        # * Save barcode image to the model field
        img = "{0}/code_{1}.png".format(
            str(my_ean)[8:], str(my_ean)[9:]
        )  # * use my_ean var instead of number
        print(
            "str(my_ean)[:9]******************",
            str(my_ean)[:9],
            "str(my_ean)[9:]**********",
            str(my_ean)[9:],
            "str(my_ean)[0:9:-1]***",
            str(my_ean)[0:9:-1],
        )
        # self.bar_img.save(f"code_{number}.png", barcode_image)
        # if self.barcode != my_ean:
        self.barcode = my_ean  # * use my_ean var instead of number
        # split_name = str(self.name.split("-"))
        name = "-".join(self.name)  # .split()

        self.barurl = "patients/{0}/code_{1}.png".format(str(name), str(my_ean)[9:])
        # ? bar_url not for saving image path but
        # ? for saving REAL URL
        self.barimg.save(img, barcode_image)
        print(
            "MY-EAN***",
            my_ean,
            "barcode_image****",
            self.barurl,
            "self.pro_barcode***",
            self.barcode,
        )

        self.save()

    # Override the save method
    def save(self, *args, **kwargs):
        # Call the create_barcode method before saving
        if not self.barimg:  # Create a new barcode if it doesn't already exist
            self.create_barcode()

        super().save(*args, **kwargs)  # Save the model after creating barcode
