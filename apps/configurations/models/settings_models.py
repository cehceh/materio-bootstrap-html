from django.utils import timezone
from django.db import models
import uuid
import os
from config import choices

from config.storage import OverwriteStorage
from django.utils.translation import gettext_lazy as _
from apps.management.models import BasicData


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def company_image_path(instance, filename):
    file_name, ext = get_filename_ext(filename)
    file_ext = "{ext}".format(ext=ext)
    code = str(instance.photo_code)
    """
        split_name = str(instance.employee.name).split()
        name = "".join(split_name)
    """
    image_path = "{0}/{1}{2}".format(str(instance.company), (code[:4]), file_ext)
    print("image_path", image_path)
    return image_path


def reciept_image_path(instance, filename):
    file_name, ext = get_filename_ext(filename)
    file_ext = "{ext}".format(ext=ext)
    code = str(instance.photo_code)

    image_path = "{0}/{1}{2}".format(str(instance.company), (code[:6]), file_ext)
    return image_path


class ManageAppSettings(BasicData):
    company = models.CharField(max_length=50, blank=True, null=True)
    app_type = models.IntegerField(
        default=0,
        choices=choices.APP_TYPES,
        # verbose_name=_('')
    )
    start_date = models.DateTimeField(default=timezone.now)
    expire_date = models.DateTimeField(default=timezone.now)

    days_count = models.IntegerField(
        default=0,
    )
    months_count = models.IntegerField(
        default=0,
    )
    years_count = models.IntegerField(
        default=0,
    )

    photo = models.ImageField(
        upload_to=company_image_path,
        storage=OverwriteStorage(),
        default="",
        blank=True,
        null=True,
        verbose_name=_("Image"),
    )

    reciept_logo = models.ImageField(
        upload_to=reciept_image_path,
        storage=OverwriteStorage(),
        default="",
        blank=True,
        null=True,
    )

    photo_code = models.UUIDField(
        primary_key=False,
        default=uuid.uuid4,
        blank=True,
        null=True,
        editable=False,
        unique=False,
    )

    users_count = models.IntegerField(
        default=0,
    )
    has_user_limits = models.BooleanField(default=False)

    is_active = models.BooleanField(default=False)
    is_expire = models.BooleanField(default=False)

    class Meta:
        app_label = "configurations"
        verbose_name = "manage_app_settings"
        verbose_name_plural = "ManageAppSettings"
