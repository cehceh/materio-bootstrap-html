from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# from django.db.models.signals import post_save # signal for profile creation
# from django.contrib.auth.models import AbstractUser # import base user model for profile
# from django.dispatch import receiver
# from allauth.account.signals import user_signed_up

from config import choices

# Create your models here.

# def get_user(instance):
#     return CustomUser.objects.get(id=instance.user.id)


class CustomUser(AbstractUser):
    """
    Handling Users for authentication
    """

    # * add additional fields in here
    # is_client = models.BooleanField(default=True) # < == remove it if u didn't use it
    mobile1 = models.CharField(max_length=30, unique=True)
    mobile2 = models.CharField(max_length=30, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)

    role = models.CharField(
        max_length=75, choices=choices.USER_TYPES, default=choices.CLIENT
    )

    def __str__(self):
        return "{}".format(self.username)

    class Meta:
        indexes = [
            models.Index(fields=["mobile1"]),
            models.Index(fields=["mobile2"]),
            models.Index(fields=["phone"]),
            models.Index(fields=["role"]),
        ]


# class UserProfile(models.Model):   # 'users.CustomUser'
#     user         = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     mobile1      = models.CharField(max_length=30, blank=True, null=True)
#     mobile2      = models.CharField(max_length=30, blank=True, null=True)
#     birth_date   = models.DateField(default=now, blank=True, null=True)
#     age          = models.CharField(max_length=150, blank=True, null=True)
#     address      = models.CharField(max_length=150, blank=True, null=True)
#     city         = models.CharField(max_length=60, default="",  blank=True, null=True)
#     photo        = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
#     profile_uuid = models.UUIDField(
#         primary_key=False,
#         default=uuid.uuid4,
#         editable=False,
#         unique=True
#     ) # to use as a "slug" for profiles
#     bio = models.TextField(default='', blank=True, null=True)
#     def __str__(self):
#         return '{}'.format(self.user.username)


class Message(models.Model):
    sender = models.ForeignKey(
        CustomUser, related_name="sender", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        CustomUser, related_name="receiver", on_delete=models.CASCADE, verbose_name="To"
    )
    body = models.TextField(verbose_name="Message")
    is_read = models.BooleanField(default=False)
    active = models.BooleanField(default=False, verbose_name=_("Active"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False, verbose_name=_("Deleted"))
    deleted_at = models.DateTimeField(auto_now=True)

    # created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "users"
        # abstract = False
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        indexes = [
            models.Index(fields=["is_read"]),
            models.Index(fields=["active"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
            models.Index(fields=["is_deleted"]),
            models.Index(fields=["deleted_at"]),
            # models.Index(fields=["created"]),
            # models.Index(fields=["updated"]),
        ]

    def __str__(self):
        return "{}".format(self.sender.username)
