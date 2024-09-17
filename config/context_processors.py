from django.conf import settings
from django.db.models import Count

from apps.patientdata.models import Patients
from apps.configurations.models.doctors_models import DoctorNames


def my_setting(request):
    context = {}
    context["patients_count"] = Patients.objects.aggregate(count=Count("id"))["count"]
    context["doctors_count"] = DoctorNames.objects.aggregate(count=Count("id"))["count"]
    ##
    context["MY_SETTING"] = settings

    return context


# Add the 'ENVIRONMENT' setting to the template context
def environment(request):
    return {"ENVIRONMENT": settings.ENVIRONMENT}
