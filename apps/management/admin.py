from django.contrib import admin
from django.apps import apps
from .models import CreateVisa, CreateWallet


# admin.site.register(CreateVisa)
# admin.site.register(CreateWallet)

# class ManagementAdmin(admin.ModelAdmin):
    
admin.site.register(apps.all_models['management'].values(),)
