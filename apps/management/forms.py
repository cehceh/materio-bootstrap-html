from django import forms
from .models import CreateVisa, CreateWallet, WalletName
from django.core.exceptions import ValidationError
from . import choices 


class CreateVisaForm(forms.ModelForm):


    class Meta:
        model = CreateVisa
        fields = [
            'visa_name', 
            'expire_date', 
            'visa_no', 
            'bank', 
            'bank_branch', 
            'account_no',
            "active",
            "is_deleted",
            "total",
            "code",
        ]
        
    def __init__(self, *args, **kwargs):
        super(CreateVisaForm, self).__init__(*args, **kwargs)
        self.fields['code'].initial = 'visa-'

class WalletNameForm(forms.ModelForm):
    
    class Meta:
        model = WalletName
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
        name = data.get('name')

        if name == '' or name == None :
            raise ValidationError('Please write wallet name')
        return name
    # init function is important in saving user automatically in create() function
    def __init__(self, *args, **kwargs):
        super(WalletNameForm, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField(
            required=False,
            widget=forms.TextInput()
        )
        
        self.fields['code'].initial = 'walname-'

class CreateWalletForm(forms.ModelForm):
    name = forms.IntegerField(
            required=False,
            widget=forms.Select(
                choices=choices.PAYMENT_WALLET
            )
        )


    class Meta:
        model = CreateWallet
        fields = [
            'name', 
            'wallet_name',
            'wallet_type',
            'code',
            'mobile', 
            'account_name', 
            'total', 
            "active",
            "is_deleted",
        ]
        
    def __init__(self, *args, **kwargs):
        super(CreateWalletForm, self).__init__(*args, **kwargs)
        self.fields['code'].initial = 'wal-'
        # self.fields['name'] = forms.IntegerField(
        #     required=False,
        #     widget=forms.Select(
        #         choices=choices.PAYMENT_WALLET
        #     )
        # )
        # wallet = [(""), ("")]
        # self.fields['name'] = choices.PAYMENT_WALLET[1]

