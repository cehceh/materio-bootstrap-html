from django import forms
from ..models import PatientReservation

# from ..models import Patients

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_none(value):
    if value is None:
        raise ValidationError(
            _("%(value)s must be not NONE"),
            params={"value": "0"},
        )


# you will write your class forms to be appear to the users
class ReservationsForm(forms.ModelForm):
    start_date = forms.DateTimeField(
        required=True,
        widget=forms.TextInput(),
    )

    class Meta:
        model = PatientReservation
        fields = [
            "start_date",
            # "addres",
            "end_date",
        ]

    def clean(self) -> dict[str]:
        print("CLEANED-DATA::::", super().clean())
        return super().clean()

    def __init__(self, *args, **kwargs):
        super(ReservationsForm, self).__init__(*args, **kwargs)

        # self.fields["age"].disabled = True
