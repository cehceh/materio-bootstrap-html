from django import forms
from django.core.exceptions import ValidationError

from ..models import DoctorNames, DoctorSpecializations


class DoctorNamesForm(forms.ModelForm):
    class Meta:
        model = DoctorNames
        fields = [
            "code",
            "name",
            "specializations",
            "mobile1",
            "mobile2",
            "phone1",
            "phone2",
            "description",
            "active",
            "is_deleted",
        ]
        widgets = {
            "specializations": forms.SelectMultiple(
                attrs={
                    "class": "form-control form-control-sm select2",
                    "multiple": "multiple",
                    # custom-control custom-switch custom-switch-off-default custom-switch-on-danger
                }
            ),
        }

    class Media:
        css = {
            "all": ("admin/css/widgets.css",),
        }
        js = ("admin/js/core.js", "admin/js/admin/RelatedObjectLookup.js")

    # init function is important in saving user automatically in create() function
    def clean(self):
        print("CLEAN DATA ***", super().clean())
        return super().clean()

    def clean_name(self):
        data = self.cleaned_data
        name = data.get("name")

        if name == "":
            raise ValidationError("Please write doctor name")
        elif name is None:
            raise ValidationError("Please write doctor name")
        return name

    def __init__(self, *args, **kwargs):
        super(DoctorNamesForm, self).__init__(*args, **kwargs)
        self.fields["name"] = forms.CharField(required=True, widget=forms.TextInput())
        # self.fields['active'].initial = True
        self.fields["code"].disabled = True
        # self.fields["code"].initial = "doctor-"

    def save(self, commit=True):
        # * First save the form with commit=False to get the instance without saving it to the database
        instance = super(DoctorNamesForm, self).save(commit=False)

        # * If the instance is new (i.e., it doesn't have an ID yet), we need to save it first to get the ID
        if commit:
            instance.save()  # Save it to generate the ID
        print("CODE-AFTER-SAVE:::", instance.code)

        return instance


class DoctorSpecializationsForm(forms.ModelForm):
    class Meta:
        model = DoctorSpecializations
        fields = [
            "name",
            "name_ar",
            "code",
            "description",
            # "active",
            # "is_deleted",
        ]

    # init function is important in saving user automatically in create() function
    def clean(self):
        print("CLEAN DATA ***", super().clean())
        return super().clean()

    def clean_name(self):
        data = self.cleaned_data
        name = data.get("name")

        if name == "":
            raise ValidationError("Please write specialization name")
        elif name is None:
            raise ValidationError("Please write specialization name")
        return name

    def __init__(self, *args, **kwargs):
        super(DoctorSpecializationsForm, self).__init__(*args, **kwargs)
        # self.fields["name"] = forms.CharField(required=True, widget=forms.TextInput())
        # self.fields['active'].initial = True
        self.fields["code"].disabled = True
        # self.fields["code"].initial = "spec-"

    def save(self, commit=True):
        # * First save the form with commit=False to get the instance without saving it to the database
        instance = super(DoctorSpecializationsForm, self).save(commit=False)

        print("COMMIT--->>>", commit)
        # * If the instance is new (i.e., it doesn't have an ID yet), we need to save it first to get the ID
        if commit:
            instance.save()  # Save it to generate the ID
            print("CODE-BEFORE-SAVE:::", instance.code)
            if instance.code == "spec-None":
                instance.code = "spec-" + str(instance.id)
                instance.save()
        print("CODE-AFTER-SAVE:::", instance.code)

        return instance
