from django.core.exceptions import ValidationError
from decimal import Decimal

from typing import Any
from django import forms
from .models import (
    UnitNames,
    Branches,
    PosStation,
    Departments,
    Bank,
    BankAccount,
    UnitConversions,
    ClientUsers,
    # ?
    DailyTaskUOM,
    DailyTaskUnitPurchase,
    DailyTaskUnitSale,
    WorkType,
    DailyTask,
    Equipments,
    Tools,
    PaymentMethod,
)
from config import choices


class ClientUsersForm(forms.ModelForm):
    class Meta:
        model = ClientUsers
        fields = [
            "name",
            "mobile",
            "balance",
        ]

    # init function is importanat in saving user automatically in create() function
    def clean(self):
        print("client_users_form-CLEAN-DATA>>>***", super().clean())
        return super().clean()

    def clean_name(self):
        FIELD = self.cleaned_data.get("name")
        if FIELD is None or FIELD == "":
            raise ValidationError("Name can not be None or empty")
        # if FIELD == 'None':
        #     raise ValidationError('Mobile must be mobile number')
        return FIELD

    def clean_mobile(self):
        FIELD = self.cleaned_data.get("mobile")
        if FIELD is None or FIELD == "":
            raise ValidationError("Mobile can not be None or empty")
        if FIELD == "None":
            raise ValidationError("Mobile must be a mobile number")
        return FIELD

    def __init__(self, *args, **kwargs):
        super(ClientUsersForm, self).__init__(*args, **kwargs)
        self.fields["name"] = forms.CharField(required=False, widget=forms.TextInput())
        self.fields["mobile"] = forms.CharField(
            required=False, widget=forms.TextInput()
        )


class UnitNamesForm(forms.ModelForm):
    class Meta:
        model = UnitNames
        fields = [
            "name",
            "code",
            "active",
            "is_deleted",
        ]

    # name = forms.CharField(
    #     required=True,
    #     label="Unit Name",
    #     widget=forms.TextInput(
    #         attrs={
    #             "placeholder": "Write the Unit name here ...",
    #         }
    #     ),
    # )
    # init function is importanat in saving user automatically in create() function
    def clean(self):
        print("CLEAN DATA ***", super().clean())
        return super().clean()

    def clean_name(self):
        data = self.cleaned_data
        name = data.get("name")

        if name == "":
            raise ValidationError("Please write UOM name")
        elif name == None:
            raise ValidationError("Please write UOM name")
        return name

    def __init__(self, *args, **kwargs):
        super(UnitNamesForm, self).__init__(*args, **kwargs)
        self.fields["name"] = forms.CharField(required=False, widget=forms.TextInput())
        # self.fields['active'].initial = True
        self.fields["code"].initial = "uom-"
        # unit_names_qs = UnitNames.objects.only("name")
        # self.fields["name"].queryset = unit_names_qs


class UnitConversionsForm(forms.ModelForm):
    class Meta:
        model = UnitConversions
        fields = [
            "unit_1",
            "val_1",
            "unit_2",
            "val_2",
            "unit_3",
            "val_3",
            "unit_4",
            "val_4",
            "unit_5",
            "val_5",
            # "active",
            # "is_deleted",
        ]

    # init function is important in saving user automatically in create() function
    def __init__(self, *args, **kwargs):
        super(UnitConversionsForm, self).__init__(*args, **kwargs)

        blank_choice = [
            ("", "--Select Unit--"),
        ]
        self.fields["unit_1"] = forms.ChoiceField(
            choices=blank_choice
            + [(obj, obj) for obj in UnitNames.objects.values_list("name", flat=True)]
        )


class BranchForm(forms.ModelForm):

    class Meta:
        model = Branches
        fields = [
            "name",
            "description",
            "code",
            "active",
            "is_deleted",
        ]

    def clean(self):
        return super().clean()

    def clean_name(self):
        data = self.cleaned_data
        name = data.get("name")

        if name == "":
            raise ValidationError("Please write Branch name")
        elif name is None:
            raise ValidationError("Please write Branch name")
        return name

    # init function is important in saving user automatically in create() function
    def __init__(self, *args, **kwargs):
        super(BranchForm, self).__init__(*args, **kwargs)
        self.fields["name"] = forms.CharField(required=False, widget=forms.TextInput())

        self.fields["code"].initial = "branch-"


class PosStationForm(forms.ModelForm):

    class Meta:
        model = PosStation
        fields = [
            "branch",
            "name",
            "description",
            "code",
            "active",
            "is_deleted",
        ]

    def clean(self):
        print("CLEAN DATA****", super().clean())
        print("formError******", self.errors.get_json_data())
        return super().clean()

    def clean_branch(self):
        data = self.cleaned_data
        branch = data.get("branch")
        if hasattr(self, "_errors") and "name" in self._errors:
            return branch
        if branch is None:
            raise ValidationError("Please choose a branch")
        return branch

    def clean_name(self):
        data = self.cleaned_data
        name = data.get("name")
        if hasattr(self, "_errors") and "branch" in self._errors:
            # Clear errors for 'name' field if 'branch' error exists
            self._errors.pop("name", None)
            return name  # Do not raise 'name' error if 'branch' error exists
        if name == "":
            raise ValidationError("Please write POS name")
        elif name is None:
            raise ValidationError("Please write POS name")
        return name

    # init function is importanat in saving user automatically in create() function
    def __init__(self, *args, **kwargs):
        super(PosStationForm, self).__init__(*args, **kwargs)
        self.fields["name"] = forms.CharField(required=False, widget=forms.TextInput())
        self.fields["branch"] = forms.ModelChoiceField(
            queryset=Branches.objects.only("name"),
            required=False,
            empty_label="--- Select Branch ---",
        )
        self.fields["code"].initial = "pos-"


class DepartmentsForm(forms.ModelForm):
    class Meta:
        model = Departments
        fields = [
            "code",
            "name",
            "active",
            "is_deleted",
            # "updated_user"
        ]

    def clean(self) -> dict[str, Any]:
        print("CLEANED DATAAA>>>>>>>>>>", super().clean())
        return super().clean()

    def __init__(self, *args, **kwargs):
        super(DepartmentsForm, self).__init__(*args, **kwargs)

        self.fields["code"].initial = "department-"


class BankForm(forms.ModelForm):

    class Meta:
        model = Bank
        fields = [
            "name",
            # "type",
            # "account_no",
            # "bank",
            # "bank_branch",
            "code",
            "active",
            "is_deleted",
        ]

    def clean(self):
        print("CLEAN DATA****", super().clean())
        print("formError******", self.errors.get_json_data())
        return super().clean()

    def clean_name(self):
        data = self.cleaned_data
        name = data.get("name")
        if name == None:
            raise ValidationError("Please write Bank name")
        elif name == "":
            raise ValidationError("Please write Bank name")
        return name

    def __init__(self, *args, **kwargs):
        super(BankForm, self).__init__(*args, **kwargs)

        self.fields["name"] = forms.CharField(required=False, widget=forms.TextInput())

        self.fields["code"].initial = "bank-"


class BankAccountForm(forms.ModelForm):

    class Meta:
        model = BankAccount  # "configurations."
        fields = [
            # "name",
            # "type",
            "code",
            "bank",
            "account_no",
            "bank_branch",
            "active",
            "is_deleted",
            "total",
        ]

    def clean(self):
        print("CLEAN DATA****", super().clean())
        print("formError******", self.errors.get_json_data())
        return super().clean()

    def clean_bank(self):
        data = self.cleaned_data
        bank = data.get("bank")
        if hasattr(self, "_errors") and "account_no" in self._errors:
            return bank
        if bank == None:
            raise ValidationError("Please choose Bank")
        return bank

    def clean_account_no(self):
        data = self.cleaned_data
        account_no = data.get("account_no")
        if hasattr(self, "_errors") and "bank" in self._errors:
            # Clear errors for 'name' field if 'branch' error exists
            self._errors.pop("account_no", None)
            return account_no
        if account_no == None:
            raise ValidationError("Please write account number")
        elif account_no == "":
            raise ValidationError("Please write account number")
        return account_no

    def clean_bank_branch(self):
        data = self.cleaned_data
        bank_branch = data.get("bank_branch")
        if hasattr(self, "_errors") and "account_no" in self._errors:
            # Clear errors for 'name' field if 'branch' error exists
            self._errors.pop("bank_branch", None)
            return bank_branch
        if bank_branch == None:
            raise ValidationError("Please write Bank Branch")
        elif bank_branch == None:
            raise ValidationError("Please write Bank Branch")
        return bank_branch

    def __init__(self, *args, **kwargs):
        super(BankAccountForm, self).__init__(*args, **kwargs)
        self.fields["bank"] = forms.ModelChoiceField(
            queryset=Bank.objects.only("name"),
            required=False,
            empty_label="--- Select Bank ---",
        )

        self.fields["account_no"] = forms.CharField(
            required=False, widget=forms.TextInput()
        )

        self.fields["bank_branch"] = forms.CharField(
            required=False, widget=forms.TextInput()
        )
        self.fields["code"].initial = "account-"


##################################*
# ?For Project settings
class WorkTypeForm(forms.ModelForm):

    class Meta:
        model = WorkType
        fields = [
            "name",
            "code",
            "active",
            "is_deleted",
        ]

    def clean(self):
        print("CLEAN DATA****", super().clean())
        print("formError******", self.errors.get_json_data())
        return super().clean()

    def clean_name(self):
        data = self.cleaned_data
        name = data.get("name")
        if name == None:
            raise ValidationError("Please write Work Type name")
        elif name == "":
            raise ValidationError("Please write Work Type name")
        return name

    def __init__(self, *args, **kwargs):
        super(WorkTypeForm, self).__init__(*args, **kwargs)

        self.fields["name"] = forms.CharField(required=False, widget=forms.TextInput())

        self.fields["code"].initial = "worktype-"


# ?For Project settings
class PaymentMethodForm(forms.ModelForm):

    class Meta:
        model = PaymentMethod
        fields = [
            "name",
            "code",
            "active",
            "is_deleted",
        ]

    def clean(self):
        print("CLEAN DATA****", super().clean())
        print("formError******", self.errors.get_json_data())
        return super().clean()

    def clean_name(self):
        data = self.cleaned_data
        name = data.get("name")
        if name == None:
            raise ValidationError("Please write Payment Method name")
        elif name == "":
            raise ValidationError("Please write Payment Method name")
        return name

    def __init__(self, *args, **kwargs):
        super(PaymentMethodForm, self).__init__(*args, **kwargs)

        self.fields["name"] = forms.CharField(required=False, widget=forms.TextInput())

        self.fields["code"].initial = "paymentmethod-"


# ?For Project settings
class DailyTaskForm(forms.ModelForm):

    class Meta:
        model = DailyTask
        fields = [
            "name",
            "code",
            "work_type",
            "description",
            "active",
            "is_deleted",
        ]

    def clean(self):
        print("CLEAN DATA****", super().clean())
        print("formError******", self.errors.get_json_data())
        return super().clean()

    def clean_name(self):
        data = self.cleaned_data
        name = data.get("name")
        if name == None:
            raise ValidationError("Please write Daily Task name")
        elif name == "":
            raise ValidationError("Please write Daily Task name")
        return name

    def __init__(self, *args, **kwargs):
        super(DailyTaskForm, self).__init__(*args, **kwargs)

        self.fields["name"] = forms.CharField(required=False, widget=forms.TextInput())

        self.fields["code"].initial = "dailytask-"


class DailyTaskUOMForm(forms.ModelForm):
    value = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"value": Decimal("0.00")})
    )

    uom_value = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"value": Decimal("0.00")})
    )

    unit_price = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"value": Decimal("0.00")})
    )

    class Meta:
        model = DailyTaskUOM
        fields = [
            "unit",
            "value",
            "uom_options",
            "uom_unit",
            "main_uom",
            "uom_value",
            "unit_conversion",
            "unit_price",
        ]

    def clean(self):
        # uom_options = self.cleaned_data.get('uom_options')
        # main_uom = self.cleaned_data.get('main_uom')
        # unit = self.cleaned_data.get('unit')
        # value = self.cleaned_data.get('value')
        print(
            "UOMFORM-from-clean-method: ",
            [obj for obj in super().clean()],
            # 'CLEAN-uom_options::', uom_options,
            # 'CLEAN-main_uom::', main_uom,
            # 'CLEAN-unit::', unit,
            # 'CLEAN-value::', value,
        )
        return super().clean()

    def clean_value(self):
        data = self.cleaned_data
        FIELD = data.get("value")
        if FIELD == None:
            FIELD = Decimal("0.00")
        if FIELD == "":
            FIELD = Decimal("0.00")
        if FIELD == "undefined":
            FIELD = Decimal("0.00")

        return FIELD

    def clean_uom_value(self):
        data = self.cleaned_data
        FIELD = data.get("uom_value")
        if FIELD == None:
            FIELD = Decimal("0.00")
        if FIELD == "":
            FIELD = Decimal("0.00")
        if FIELD == "undefined":
            FIELD = Decimal("0.00")

        return FIELD

    def clean_unit_price(self):
        data = self.cleaned_data
        FIELD = data.get("unit_price")
        if FIELD == None:
            FIELD = Decimal("0.00")
        if FIELD == "":
            FIELD = Decimal("0.00")
        if FIELD == "undefined":
            FIELD = Decimal("0.00")

        return FIELD

    # init function is important in saving user automatically in create() function
    def __init__(self, *args, **kwargs):
        super(DailyTaskUOMForm, self).__init__(*args, **kwargs)

        unit_blank_choice = [
            ("", "--Select Type--"),
        ]
        self.fields["uom_options"] = forms.ChoiceField(
            required=False, choices=unit_blank_choice + list(choices.UNITS)
        )
        self.fields["unit"].empty_label = "--Unit Name--"
        self.fields["unit"] = forms.ModelChoiceField(
            queryset=UnitNames.objects.only(),
            required=False,
        )

        uom_unit_choice = [
            ("", "--- Unit Label ---"),
        ]
        self.fields["uom_unit"] = forms.ChoiceField(
            required=False,
            choices=uom_unit_choice
            + [(obj, obj) for obj in UnitNames.objects.values_list("name", flat=True)],
        )


class DailyTaskUnitPurchaseForm(forms.ModelForm):

    # init function is important in saving user automatically in create() function
    def __init__(self, *args, **kwargs):
        super(DailyTaskUnitPurchaseForm, self).__init__(*args, **kwargs)

    class Meta:
        model = DailyTaskUnitPurchase
        fields = ["unit_price"]


class DailyTaskUnitSaleForm(forms.ModelForm):

    # init function is important in saving user automatically in create() function
    def __init__(self, *args, **kwargs):
        super(DailyTaskUnitSaleForm, self).__init__(*args, **kwargs)

    class Meta:
        model = DailyTaskUnitSale
        fields = [
            "value",
            "percentage",
            "unit_price",
        ]


class EquipmentsForm(forms.ModelForm):
    class Meta:
        model = Equipments
        fields = [
            "code",
            "equip_type",
            "brand",
            "model",
            "manufacturing_year",
            "current_status",
            "vehicle_type",
            "governorate",
            "traffic_unit",
            "license_plate_number",
            "owner",
            "exp_date",
            "reference_code",
            "active",
            "is_deleted",
        ]

    def clean(self):
        data = super().clean()
        print("CLEANeD DATA::::::", data)
        return super().clean()

    def __init__(self, *args, **kwargs):
        super(EquipmentsForm, self).__init__(*args, **kwargs)

        self.fields["equip_type"] = forms.IntegerField(
            required=False,
            widget=forms.Select(
                choices=choices.EQUIPMENT_TYPE,
            ),
        )
        self.fields["current_status"] = forms.IntegerField(
            required=False,
            widget=forms.Select(
                choices=choices.CURRENT_STATUS,
            ),
        )
        self.fields["governorate"] = forms.IntegerField(
            required=False,
            widget=forms.Select(
                choices=choices.EGYPT_GOVERNORATES,
            ),
        )
        self.fields["vehicle_type"] = forms.IntegerField(
            required=False,
            widget=forms.Select(
                choices=choices.VEHICLE_TYPES,
            ),
        )

        self.fields["reference_code"].widget.attrs["value"] = uuid.uuid1()
        self.fields["code"].initial = "equip-"


class ToolsForm(forms.ModelForm):
    class Meta:
        model = Tools
        fields = [
            "code",
            "name",
            "brand",
            "model",
            "manufacturing_year",
            "current_status",
            "owner",
            "reference_code",
            "active",
            "is_deleted",
        ]

    def clean(self):
        data = super().clean()
        print("CLEANeD DATA::::::", data)
        return super().clean()

    def __init__(self, *args, **kwargs):
        super(ToolsForm, self).__init__(*args, **kwargs)

        self.fields["current_status"] = forms.IntegerField(
            required=False,
            widget=forms.Select(
                choices=choices.CURRENT_STATUS,
            ),
        )
        self.fields["reference_code"].widget.attrs["value"] = uuid.uuid1()
        self.fields["code"].initial = "tool-"
