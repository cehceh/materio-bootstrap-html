from django.db import models
from django.utils.translation import gettext_lazy as _

# from posapp.storage import OverwriteStorage
from config import choices

# from apps.products.models import Product
# from apps.management.models import BasicData

# Create your models here.


# * make a generic model with abstract=True
class BasicData(models.Model):
    user = models.ForeignKey(
        "users.CustomUser",
        default="",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        # related_name="user_create_object",
    )

    active = models.BooleanField(default=False, verbose_name=_("Active"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False, verbose_name=_("Deleted"))
    deleted_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        indexes = [
            ##BasicData
            models.Index(fields=["active"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
            models.Index(fields=["is_deleted"]),
            models.Index(fields=["deleted_at"]),
        ]


class ClientUsers(BasicData):
    """
    This model for gathering every Employee, Client and Vendor in one
    table and mark them as client to be shown in the sell service page
    """

    name = models.CharField(max_length=150, verbose_name=_("Client Name"))
    updated_user = models.ForeignKey(
        "users.CustomUser",
        related_name="user_make_client_users_changes",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    name_id = models.IntegerField(verbose_name=_("client code"), blank=True, null=True)
    role = models.IntegerField(
        choices=choices.CLIENT_ROLE, default=0, blank=True, null=True
    )
    is_client = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)

    # client = models.ForeignKey(
    #     "clients.Client",
    #     related_name="client_users_client",
    #     blank=True,
    #     null=True,
    #     on_delete=models.CASCADE,
    # )

    # vendor = models.ForeignKey(
    #     "vendors.Vendor",
    #     related_name="client_users_vendor",
    #     blank=True,
    #     null=True,
    #     on_delete=models.CASCADE,
    # )

    # employee = models.ForeignKey(
    #     "employees.Employee",
    #     related_name="client_users_employee",
    #     blank=True,
    #     null=True,
    #     on_delete=models.CASCADE,
    # )

    mobile = models.CharField(
        max_length=25, blank=True, null=True, unique=True, verbose_name=_("Mobile")
    )

    balance = models.DecimalField(
        decimal_places=3,
        max_digits=15,
        blank=True,
        null=True,
        default=00.00,
        verbose_name=_("User Balance"),
    )

    credit = models.DecimalField(
        decimal_places=3,
        max_digits=15,
        blank=True,
        null=True,
        default=00.00,
        verbose_name=_("Amount The User Have"),
    )

    debit = models.DecimalField(
        decimal_places=3,
        max_digits=15,
        blank=True,
        null=True,
        default=00.00,
        verbose_name=_("Amount To Be Catched From The User"),
    )

    class Meta:
        app_label = "configurations"
        verbose_name = "client_users"
        verbose_name_plural = "Client Users"
        indexes = [
            ##ClientsUsers
            models.Index(fields=["name"]),
            models.Index(fields=["name_id"]),
            models.Index(fields=["role"]),
            models.Index(fields=["balance"]),
            ##BasicData
            models.Index(fields=["active"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
            models.Index(fields=["is_deleted"]),
            models.Index(fields=["deleted_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.name}"


###########################* for settings tab in sidebar
class UnitNames(BasicData):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name=_("Code"),
    )
    updated_user = models.ForeignKey(
        "users.CustomUser",
        related_name="user_make_unit_names_changes",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        app_label = "configurations"
        verbose_name = "unit_names"
        verbose_name_plural = "UnitNames"
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
        return f"{self.name}"  # super().__str__()


class Branches(BasicData):
    name = models.CharField(max_length=100, unique=True, verbose_name="Branch")
    description = models.TextField(blank=True, null=True)
    code = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name=_("Code"),
    )
    updated_user = models.ForeignKey(
        "users.CustomUser",
        related_name="user_make_branches_changes",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        app_label = "configurations"
        verbose_name = "branches"
        verbose_name_plural = "Branches"
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


class PosStation(BasicData):
    branch = models.ForeignKey(
        Branches,
        related_name="pos_branch",
        verbose_name=_("Branch"),
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=100, unique=True, default="Text")
    description = models.TextField(blank=True, null=True, default="Text")
    code = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name=_("Code"),
    )
    updated_user = models.ForeignKey(
        "users.CustomUser",
        related_name="user_make_pos_station_changes",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        app_label = "configurations"
        verbose_name = "pos_station"
        verbose_name_plural = "PosStations"
        ordering = ["-id"]
        indexes = [
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


class Departments(BasicData):
    code = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name=_("Code"),
    )
    name = models.CharField(max_length=100, unique=True)

    updated_user = models.ForeignKey(
        "users.CustomUser",
        related_name="user_make_departments_changes",
        on_delete=models.CASCADE,
    )

    class Meta:
        app_label = "configurations"
        verbose_name = "departments"
        verbose_name_plural = "Departments"
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["active"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
            models.Index(fields=["is_deleted"]),
            models.Index(fields=["deleted_at"]),
        ]

    def __str__(self):
        return f"{self.name}"


class Bank(BasicData):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=100,
        unique=True,
    )
    updated_user = models.ForeignKey(
        "users.CustomUser",
        related_name="user_make_bank_changes",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    code = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name=_("Code"),
    )
    #!!!trail for trying to restore deleted data
    # def restore(self):
    #         # Restore the object by marking it as not deleted
    #         self.is_deleted = False
    #         self.deleted_at = None
    #         self.save()

    class Meta:
        app_label = "configurations"
        verbose_name = "bank"
        verbose_name_plural = "Banks"
        indexes = [
            models.Index(fields=["name"]),
            # models.Index(fields=["type"]),
            # models.Index(fields=["account_no"]),
            models.Index(fields=["code"]),
            models.Index(fields=["active"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
            models.Index(fields=["is_deleted"]),
            models.Index(fields=["deleted_at"]),
        ]

    def __str__(self):
        return f"{self.name}"

    @property
    def get_bank_name(self):
        return self.name


class BankAccount(BasicData):
    account_no = models.CharField(
        max_length=150,
        verbose_name=_("Account No."),
        unique=True,
        # blank=True, null=True
    )
    bank = models.ForeignKey(
        Bank,
        related_name="bank_account",
        verbose_name=_("Bank Name"),
        # unique=True,
        # blank=True, null=True,
        on_delete=models.CASCADE,
    )
    code = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name=_("Code"),
    )
    bank_branch = models.CharField(
        max_length=100,
        # blank=True, null=True,
        verbose_name=_("Bank Branch"),
    )
    total = models.DecimalField(
        decimal_places=5,
        max_digits=15,
        blank=True,
        null=True,
        default=00.00,
        verbose_name=_("Account Balance"),
    )
    # type = models.CharField(verbose_name="Type", max_length=100, choices=OBJECT_TYPE)
    updated_user = models.ForeignKey(
        "users.CustomUser",
        related_name="user_make_bank_account_changes",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    is_client = models.BooleanField(blank=True, null=True, default=False)

    class Meta:
        app_label = "configurations"
        verbose_name = "bank_account"
        verbose_name_plural = "Bank Accounts"
        indexes = [
            models.Index(fields=["account_no"]),
            models.Index(fields=["bank_branch"]),
            models.Index(fields=["code"]),
            models.Index(fields=["is_client"]),
            models.Index(fields=["active"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
            models.Index(fields=["is_deleted"]),
            models.Index(fields=["deleted_at"]),
        ]

    def __str__(self):
        return f"{self.account_no}"
