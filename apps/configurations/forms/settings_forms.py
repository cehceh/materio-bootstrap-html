from django import forms
from ..models import ManageAppSettings


class ManageAppSettingsForm(forms.ModelForm):
    class Meta:
        model = ManageAppSettings
        fields = [
            "company",
            "bussiness",
            "start_date",
            "expire_date",
            "days_count",
            "months_count",
            "years_count",
            "photo",
            "reciept_logo",
            "users_count",
            "has_user_limits",
            "is_active",
            "is_expire",
        ]

    def __init__(self, *args, **kwargs):
        super(ManageAppSettingsForm, self).__init__(*args, **kwargs)

        self.fields["photo"] = forms.FileField(required=False, widget=forms.FileInput())
        self.fields["reciept_logo"] = forms.FileField(
            required=False, widget=forms.FileInput()
        )
