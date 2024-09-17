from django.contrib import admin
from django.apps import apps

# from .models import UnitNames, Branches, PosStation, Departments


# admin.site.register(UnitNames)
# admin.site.register(Branches)
# admin.site.register(PosStation)
# admin.site.register(Departments)


admin.site.register(apps.all_models['configurations'].values())
