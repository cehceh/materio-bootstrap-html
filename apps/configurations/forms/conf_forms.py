from django import forms
from django.core.exceptions import ValidationError

from ..models import ClientUsers, UnitNames, Branches, Departments


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

    # init function is important in saving user automatically in create() function
    def clean(self):
        print("CLEAN DATA ***", super().clean())
        return super().clean()

    def clean_name(self):
        data = self.cleaned_data
        name = data.get("name")

        if name == "":
            raise ValidationError("Please write UOM name")
        elif name is None:
            raise ValidationError("Please write UOM name")
        return name

    def __init__(self, *args, **kwargs):
        super(UnitNamesForm, self).__init__(*args, **kwargs)
        self.fields["name"] = forms.CharField(required=False, widget=forms.TextInput())
        # self.fields['active'].initial = True
        self.fields["code"].initial = "uom-"
        # unit_names_qs = UnitNames.objects.only("name")
        # self.fields["name"].queryset = unit_names_qs


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

    def clean(self) -> dict:
        print("CLEANED DATAAA>>>>>>>>>>", super().clean())
        return super().clean()

    def __init__(self, *args, **kwargs):
        super(DepartmentsForm, self).__init__(*args, **kwargs)

        self.fields["code"].initial = "department-"
