from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser   #, UserProfile
from django.apps import apps
from django.db.models import fields
# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    # list_display = ('username', 'email', 'is_staff', 'is_active', 'mobile1', 'mobile2', 'role',)
    # list_filter = ('username', 'email', 'is_staff', 'is_active', 'mobile1', 'mobile2', 'role',)
    # fieldsets = (
    #     (None, {
    #         'fields': ('email', 'password')
    #     }),(
    #         'Permissions', {
    #         'fields': (
    #             'is_staff', 'is_active', 
    #             'mobile1', 'mobile2', 'role',
    #             )
    #         }),
    # )
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active', 'mobile1', 'mobile2', 'role')}
    #     ),
    # )
    # search_fields = ('username', 'email',)
    # ordering = ('username', 'email',)


# admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(UserProfile)
admin.site.register(apps.all_models['users'].values())



