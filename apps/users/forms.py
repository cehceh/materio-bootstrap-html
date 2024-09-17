from django import forms

# from django.forms import widgets
# from django.contrib.auth import models
# from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

# from apps.accounts.models import AdminProfile #, CustomUser
from .models import Message, CustomUser

# user = get_user_model()

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# from apps.accounts.models import AdminProfile


# CHOICES = (
#     ('admin', 'Administrator'),
#     ('supplier', 'Supplier'),
#     ('customer', 'Customer'),
# )


class CustomUserCreationForm(UserCreationForm):
    CHOICES = (
        ("", "--Select Role--"),
        ("owner", "Owner"),
        # ('admin', "Admin"),
        ("manager", "Manager"),
        ("employee", "Employee"),
        # for later
        ("vendor", "Vendor"),
        ("client", "Client"),
        ("representative", "Representative"),
        ("driver", "Driver"),
        ("guest", "Guest"),
        ("cashier", "Cashier"),
    )

    role = forms.CharField(
        required=True,
        widget=forms.Select(
            choices=CHOICES,
            attrs={
                "class": "form-control",
                "type": "text",
            },
        ),
    )

    # email = forms.EmailField(
    #     required=True
    # )
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "mobile1",
            "role",
            "password1",
            "password2",
        )

    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     match = CustomUser.objects.filter(email=email).exists()
    #     if match:
    #         raise ValidationError("This email is already exists, Please enter an unique email address ... ")
    #     raise ValidationError("Please enter a valid email address ... ")
    # else:

    # return email

    def clean_username(self):
        username = self.cleaned_data["username"]
        if len(username) > 20:
            raise ValidationError(
                "username must be less than or equal to 20 characters ... "
            )
        else:
            return username
        # return username


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        # fields = ('username', 'email')
        fields = UserChangeForm.Meta.fields


class EmployeeCreationForm(UserCreationForm):
    EMP_CHOICES = (("employee", "Employee"),)
    role = forms.CharField(
        required=True,
        widget=forms.Select(
            choices=EMP_CHOICES,
            attrs={
                "class": "form-control",
                "type": "text",
            },
        ),
    )

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "mobile1",
            "role",
            "password1",
            "password2",
        )

    def clean_username(self):
        username = self.cleaned_data["username"]
        if len(username) > 20:
            raise ValidationError(
                "username must be less than or equal to 20 characters ... "
            )
        else:
            return username


# class UserProfileForm(forms.ModelForm):
#     birth_date = forms.DateField(
#             widget= forms.DateInput(
#                 attrs={
#                     'type': 'date',
#                     'value': date.today(),
#                 }
#             )
#     )
#     class Meta:
#         model  = AdminProfile #UserProfile
#         fields = (
#             'address', 'birth_date',
#             'age', 'city','photo',
#         ) #('__all__') #
#     # widgets = {
#     #     'birth_date': forms.DateInput(
#     #                 attrs={
#     #                     'type': 'date',
#     #                 }
#     #     )
#     # }
#     #
#     # def __init__(self, *args, **kwargs):
#     #     super(UserProfileForm, self).__init__(*args, **kwargs)
#     #     # Add the photo field with the required widget
#     #     self.fields['photo'] = forms.ImageField(
#     #         required=False, widget=forms.FileInput(attrs={'class': 'form-control form-control-sm'})
#     #     )
#     def __init__(self, *args, **kwargs):
#         super(UserProfileForm, self).__init__(*args, **kwargs)


class MessageForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
            }
        ),
    )

    class Meta:
        model = Message
        fields = (
            "receiver",
            "body",
        )

    def __init__(self, *args, user, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.user = user
        # self.sender = user
        # self.sender = kwargs['sender_id']
        # print('user',user, self.sender)
        self.fields["receiver"].widget.attrs["class"] = "form-control"
        self.fields["receiver"].queryset = CustomUser.objects.filter(
            is_staff=True
        ).exclude(id=self.user)

        # self.fields['receiver'] = forms.ModelChoiceField(
        #                             queryset=CustomUser.objects.filter(is_staff=True).exclude(id=self.user),
        #                             required=True,
        #                             widget= forms.Select(
        #                                 attrs={
        #                                     'class': 'form-control',
        #                                 }))
