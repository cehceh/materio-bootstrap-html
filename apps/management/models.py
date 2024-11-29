from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from django.utils.deconstruct import deconstructible
from uuid import uuid4
import os

from .choices import PAYMENT_WALLET, WALLET_TYPE

from config import choices


@deconstructible
class UploadTo(object):

    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        ext = filename.split(".")[-1]
        # file_name = ""
        # get filename
        # client = ""
        # company = ""

        if instance == "Client":
            client = "-".join((instance.name).split())
            photo_path = self.sub_path + "individuals/"
            # if instance.is_individual:
            file_name = "client_{}.{}".format((uuid4().hex)[6], ext)
        elif instance == "CompanyClient":
            photo_path = self.sub_path + "companies/"
            # if instance.is_company:
            company = "-".join(str(instance.company).split())
            file_name = "{}.{}".format(company, ext)
        else:
            file_name = ""
            photo_path = self.sub_path
        # if instance.pk:
        #     filename = '{}.{}'.format(instance.pk, ext)
        # else:
        #     # set filename as random string
        #     filename = '{}.{}'.format(uuid4().hex, ext)
        # photo_path = self.sub_path + str(instance)
        print("PHOTOPATH::", photo_path, self.sub_path, file_name)
        file_path = os.path.join(photo_path, file_name)
        # return the whole path to the file
        return file_path  # os.path.join(self.sub_path, filename)


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


class ClientBasicData(models.Model):
    branch = models.ForeignKey(
        "configurations.Branches",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    phone = models.CharField(max_length=25, blank=True, null=True)
    mobile1 = models.CharField(max_length=25, blank=True, null=True, unique=True)
    mobile2 = models.CharField(max_length=25, blank=True, null=True, unique=True)
    email = models.EmailField(max_length=100, blank=True, null=True, unique=True)

    country = models.CharField(
        max_length=3,
        choices=choices.COUNTRY,
        default=choices.COUNTRY[8][0],
        blank=True,
        null=True,
    )
    city = models.CharField(
        max_length=20,
        choices=choices.CITY,
        default=choices.CITY[0][0],
        blank=True,
        null=True,
    )
    area = models.CharField(max_length=60, default="", blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    postal_code = models.CharField(max_length=15, blank=True, null=True)

    facebook = models.URLField(max_length=100, blank=True, null=True)
    twitter = models.URLField(max_length=100, blank=True, null=True)
    linkedin = models.URLField(max_length=100, blank=True, null=True)
    web_site = models.URLField(max_length=100, blank=True, null=True)

    join_date = models.DateField(default=now, blank=True, null=True)
    end_date = models.DateField(default=now, blank=True, null=True)

    is_individual = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)

    description = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True


class WalletName(BasicData):
    name = models.CharField(max_length=100, unique=True, verbose_name="wallet")
    description = models.TextField(blank=True, null=True)
    code = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name=_("Code"),
    )
    updated_user = models.ForeignKey(
        "users.CustomUser",
        related_name="user_make_wallet_names_changes",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        app_label = "management"
        verbose_name = "wallet_name"
        verbose_name_plural = "Wallet Names"
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


class ServicePayment(models.Model):
    payment_methods = models.IntegerField(
        null=True,
        blank=True,
        choices=choices.PAYMENT_METHODS,
        verbose_name=_("Payment Methods"),
        default=0,
    )

    cash_methods = models.IntegerField(
        default=0,  # choices.CASH_PAYMENT_METHODS[0][0],
        blank=True,
        null=True,
        choices=choices.CASH_PAYMENT_METHODS,
        verbose_name=_("Cash Payment Methods"),
    )

    store = models.ForeignKey(
        "stores.Stores", verbose_name=_("Store Name"), on_delete=models.CASCADE
    )

    treasury = models.ForeignKey(
        "treasuries.Treasury",
        default="",
        null=True,
        blank=True,
        verbose_name=_("Treasury Name"),
        on_delete=models.CASCADE,
    )

    branch = models.ForeignKey(
        "configurations.Branches",
        null=True,
        blank=True,
        verbose_name=_("Branch Name"),
        on_delete=models.CASCADE,
    )

    visa = models.ForeignKey(
        "management.CreateVisa",
        default="",
        null=True,
        blank=True,
        verbose_name=_("Visa"),
        on_delete=models.CASCADE,
    )

    bank = models.ForeignKey(
        "configurations.Bank",
        null=True,
        blank=True,
        verbose_name=_("Bank Account"),
        on_delete=models.CASCADE,
    )
    bank_branch = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Bank Branch"),
    )
    bank_account = models.ForeignKey(
        "configurations.BankAccount",
        null=True,
        blank=True,
        verbose_name=_("Bank Account"),
        on_delete=models.CASCADE,
    )

    wallet_name = models.IntegerField(
        null=True,
        blank=True,
        default=0,
        choices=PAYMENT_WALLET,
        verbose_name=_("Wallet Name"),
    )

    wallet_new_name = models.ForeignKey(
        WalletName,
        default="",
        null=True,
        blank=True,
        verbose_name=_("Wallet"),
        on_delete=models.CASCADE,
    )

    mobile = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_("Mobile"),
    )
    account_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Email "),
    )

    balance = models.DecimalField(
        decimal_places=3,
        max_digits=10,
        default=00.00,
        blank=True,
        null=True,
        verbose_name=_("Balance"),
    )

    amount = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        default=00.00,
        blank=True,
        null=True,
        verbose_name=_("Cash Payment"),
    )

    class Meta:
        abstract = True


class DiscountTax(models.Model):
    # * for discount
    discount = models.IntegerField(
        null=True,
        blank=True,
        choices=choices.DISCOUNT_CHOICES,
        # default=choices.DISCOUNT_CHOICES[0][0]
    )
    discount_percentage = models.DecimalField(
        decimal_places=2,
        max_digits=5,
        default=00.00,
        null=True,
        blank=True,
        verbose_name=_("Discount Percentage"),
    )
    discount_value = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        default=00.00,
        null=True,
        blank=True,
        verbose_name=_("Discount Value"),
    )

    # * for tax
    tax = models.IntegerField(
        null=True,
        blank=True,
        choices=choices.TAX_CHOICES,
        # default=choices.TAX_CHOICES[0][0]
    )
    tax_percentage = models.DecimalField(
        decimal_places=2,
        max_digits=5,
        default=00.00,
        null=True,
        blank=True,
        verbose_name=_("Tax Percentage"),
    )
    tax_value = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        default=00.00,
        null=True,
        blank=True,
        verbose_name=_("Tax Value"),
    )

    class Meta:
        abstract = True


class TreasuryPayment(models.Model):
    treasury = models.ForeignKey(
        "treasuries.Treasury",
        default="",
        null=True,
        blank=True,
        verbose_name=_("Treasury Name"),
        # related_name="treasury_payment_treasury",
        on_delete=models.CASCADE,
    )

    branch = models.ForeignKey(
        "configurations.Branches",
        null=True,
        blank=True,
        verbose_name=_("Branch Name"),
        on_delete=models.CASCADE,
    )

    visa = models.ForeignKey(
        "management.CreateVisa",
        default="",
        null=True,
        blank=True,
        verbose_name=_("Visa"),
        on_delete=models.CASCADE,
    )

    bank = models.ForeignKey(
        "configurations.Bank",
        null=True,
        blank=True,
        verbose_name=_("Bank Account"),
        on_delete=models.CASCADE,
    )

    bank_account = models.ForeignKey(
        "configurations.BankAccount",
        null=True,
        blank=True,
        verbose_name=_("Bank Account"),
        on_delete=models.CASCADE,
    )
    wallet_name = models.IntegerField(
        null=True,
        blank=True,
        default=0,
        choices=PAYMENT_WALLET,
        verbose_name=_("Wallet Name"),
    )

    wallet_new_name = models.ForeignKey(
        # 'management.CreateWallet',
        WalletName,
        default="",
        null=True,
        blank=True,
        verbose_name=_("Wallet Name"),
        on_delete=models.CASCADE,
    )

    mobile = models.CharField(
        max_length=50,
        # choices=[],
        blank=True,
        null=True,
        verbose_name=_("Mobile"),
    )
    account_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default="",
        verbose_name=_("Email "),
    )

    class Meta:
        abstract = True


class CreateVisa(BasicData):
    visa_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Visa Owner Name"),
    )
    expire_date = models.DateField(
        default=now, blank=True, null=True, verbose_name=_("Expire Date")
    )
    visa_no = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        unique=True,
        verbose_name=_("Visa Number"),
    )
    bank = models.ForeignKey(
        "configurations.Bank",
        related_name="bank_name",
        blank=True,
        null=True,
        verbose_name="Bank Name",
        on_delete=models.CASCADE,
    )
    bank_branch = models.CharField(
        max_length=100, verbose_name="Bank Branch", blank=True, null=True
    )
    account_no = models.ForeignKey(
        "configurations.BankAccount",
        blank=True,
        null=True,
        verbose_name="Bank Account",
        on_delete=models.CASCADE,
    )

    total = models.DecimalField(
        decimal_places=3,
        max_digits=15,
        blank=True,
        null=True,
        default=00.00,
        verbose_name=_("Visa Balance"),
    )

    updated_user = models.ForeignKey(
        "users.CustomUser",
        related_name="user_make_create_visa_changes",
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

    is_client = models.BooleanField(blank=True, null=True, default=False)

    class Meta:
        app_label = "management"
        verbose_name = "create_visa"
        verbose_name_plural = "Create Visa"
        indexes = [
            models.Index(fields=["visa_name"]),
            models.Index(fields=["expire_date"]),
            models.Index(fields=["visa_no"]),
            models.Index(fields=["active"]),
            models.Index(fields=["is_client"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
            models.Index(fields=["is_deleted"]),
            models.Index(fields=["deleted_at"]),
            models.Index(fields=["code"]),
        ]

    def __str__(self) -> str:
        return self.visa_no  # super().__str__()


# class CreateCheque(BasicData):
#     cheque_name = models.CharField(
#         max_length=100,
#         verbose_name=_("Visa Owner Name"),
#         blank=True, null=True,)
#     cheque_date = models.DateField(
#          default=timezone.now,
#          blank=True, null=True,
#          verbose_name=_("Expire Date")
#     )
#     cheque_no = models.CharField(
#         max_length=100,
#         blank=True, null=True,
#     )

#     class Meta:
#         app_label = "management"
#         verbose_name = "create_cheque"
#         verbose_name_plural = "Create Cheque"

#     def __str__(self) -> str:
#         return super().__str__()


class CreateWallet(BasicData):
    """
    For mobile wallet as(Vodafone cash, ...) and tranfer money from (PayPal, EnstaPay, ...) to your Wallet
    """

    name = models.IntegerField(
        default=0,
        choices=PAYMENT_WALLET,
        verbose_name=_("Wallet Name"),
    )
    wallet_name = models.ForeignKey(
        WalletName,
        related_name="wallet_name",
        verbose_name=_("Wallet"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    wallet_type = models.IntegerField(
        default=0,
        choices=WALLET_TYPE,
        verbose_name=("Wallet Type"),
        blank=True,
        null=True,
    )
    mobile = models.CharField(
        max_length=30,
        default="",
        verbose_name=_("Mobile Number"),
        blank=True,
        null=True,
    )
    account_name = models.CharField(
        max_length=120,
        default="",
        blank=True,
        null=True,
        verbose_name=_("Account Name / Email"),
    )
    total = models.DecimalField(
        decimal_places=3,
        max_digits=15,
        blank=True,
        null=True,
        default=00.00,
        verbose_name=_("Wallet Amount"),
    )

    updated_user = models.ForeignKey(
        "users.CustomUser",
        related_name="user_make_create_wallet_changes",
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

    is_client = models.BooleanField(blank=True, null=True, default=False)

    class Meta:
        app_label = "management"
        verbose_name = "create_wallet"
        verbose_name_plural = "Create Wallets"
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["mobile"]),
            models.Index(fields=["account_name"]),
            models.Index(fields=["code"]),
            models.Index(fields=["is_client"]),
            ##BasicData
            models.Index(fields=["active"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
            models.Index(fields=["is_deleted"]),
            models.Index(fields=["deleted_at"]),
        ]

    def __str__(self) -> str:
        # if self.wallet_type == 1:
        #     return f"{self.mobile}"
        # elif self.wallet_type == 2:
        #     return f"{self.account_name}" # super().__str__()
        # else:
        return f"{self.wallet_name}"
        # return f"{self.id}:: {self.mobile} -- {self.account_name}" # super().__str__()
        # return f"{self.mobile} -- {self.account_name}" # super().__str__()


# class CreateObject(models.Model):
# '''
#     For Creating ('Bank Account', 'Cheque', 'Visa')
# '''
# bank = models.ForeignKey(
#     "configurations.Bank",
#     related_name="bank_name",
#     # blank=True, null=True,
#     verbose_name="Bank Name",
#     on_delete=models.CASCADE
# )
# bank_branch = models.CharField(
#     max_length=100,
#     verbose_name="Bank Branch",
#     blank=True, null=True
# )
# # type = models.IntegerField(verbose_name="Type", choices=OBJECT_TYPE)
# account_no = models.ForeignKey(
#     "configurations.BankAccount",
#     # blank=True, null=True,
#     verbose_name="Bank Account",
#     on_delete=models.CASCADE
# )
# models.CharField(verbose_name="Bank Account No.", max_length=120, blank=True, null=True)
# updated_user = models.ForeignKey(
#     "users.CustomUser",
#     related_name="user_make_create_object_changes",
#     blank=True, null=True, on_delete=models.CASCADE
# )

# class Meta:
#     abstract = True
