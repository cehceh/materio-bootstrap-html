from django import forms
from django.core.exceptions import ValidationError

from ..models import DoctorNames


class DoctorNamesForm(forms.ModelForm):
    class Meta:
        model = DoctorNames
        fields = [
            "name",
            "description",
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
            raise ValidationError("Please write doctor name")
        elif name is None:
            raise ValidationError("Please write doctor name")
        return name

    def __init__(self, *args, **kwargs):
        super(DoctorNamesForm, self).__init__(*args, **kwargs)
        self.fields["name"] = forms.CharField(required=True, widget=forms.TextInput())
        # self.fields['active'].initial = True
        self.fields["code"].initial = "uom-"
        # unit_names_qs = UnitNames.objects.only("name")
        # self.fields["name"].queryset = unit_names_qs
