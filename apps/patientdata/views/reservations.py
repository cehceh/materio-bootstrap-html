from django.db.models.query import QuerySet
from django.db.models import Count
from django.urls import reverse_lazy
from django.http import JsonResponse

from ..forms import PatientsForm, ReservationsForm
from ..models import Patients, PatientReservation

# from apps.patientdata.models import


from django.views.generic.edit import CreateView, UpdateView
from web_project import TemplateLayout

import logging

logger = logging.getLogger("myapp")


class ReservationsView(CreateView):  # (TemplateView):
    template_name = "reservations/reservations.html"
    form_class = ReservationsForm
    queryset = PatientReservation.objects.only()[:100]
    success_url = reverse_lazy("patientdata:reservations")
    reservation_dashboard_url = reverse_lazy("patientdata:reservation-dashboard")

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            # return self.form_valid(form)
            data = {}
            print("I am here in form_valid")

            save_form = form.save(commit=False)
            save_form.age = request.POST.get("age")
            save_form.save()

            data["msg"] = "Patient (" + save_form.name + ") saved done"
            data["type"] = "success"
            return JsonResponse(data)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        data = {}
        print("FORM-IS-INVALID FROM-->FORM_INVALID")
        # for f in form:
        #     print("F.NAME>>", f.name, "F.ERRORS>>", f.errors)
        if not form.is_valid():
            msg = [
                ("(" + key + "-Error):", value[0]["message"] + " \n")
                for key, value in (form.errors.get_json_data().items())
            ]
            data["msg"] = msg
            data["type"] = "error"
            return JsonResponse(data)
        return self.render_to_response(self.get_context_data(form=form))

    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        title = ""
        # context |= {"var": "Amr Amer"}
        lastid = Patients.objects.values("id").last()
        patid = lastid["id"] + 1 if lastid else 1
        context["lastid"] = patid
        patient_count = Patients.objects.aggregate(count=Count("id") + 1)
        context["patient_count"] = str(patient_count["count"])
        if (
            self.request.path == self.reservation_dashboard_url
        ):  # "/patients/reservation/dashboard/":
            title = "Reservstion Dashboard"
            # print(self.reservation_dashboard_url, "<<===")
        elif self.request.path == "/patients/reservation/area/":
            title = "Reservations"

        ##
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")

        context["title"] = title
        # context["savepatform"] = self.form_class
        # context["savepatform"] = form.form_valid
        context["qs"] = self.get_queryset()
        context["reservation_dashboard_url"] = self.reservation_dashboard_url
        data = {
            "var": "Amr Ali Amer",
            "show_hour": self.request.GET.get("show_hour"),
            "show_day": self.request.GET.get("show_day"),
        }
        return context | data


class PatientUpdateView(UpdateView):
    model = Patients
    template_name = "edit_patient.html"
    pk_url_kwarg = "patient_id"
    queryset = Patients.objects.all()
    form_class = PatientsForm
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("patientdata:edit-patient")

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        data = {}
        print("FORM-IS-INVALID FROM-->FORM_INVALID")
        # for f in form:
        #     print("F.NAME>>", f.name, "F.ERRORS>>", f.errors)
        if not form.is_valid():
            msg = [
                ("(" + key + "-Error):", value[0]["message"] + " \n")
                for key, value in (form.errors.get_json_data().items())
            ]
            data["msg"] = msg
            data["type"] = "error"
            return JsonResponse(data)
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.object = self.get_object()
        print("SELF.OBJECT", self.object, "REQUEST.COPY>>>", request.POST.copy())
        form = self.get_form()  # (self.form_class(instance=self.object))
        if form.is_valid():
            # return self.form_valid(form)
            data = {}
            print("I am here in form_valid-IN-POST()>>")

            save_form = form.save(commit=False)
            save_form.age = request.POST.get("age")
            save_form.save()

            data["msg"] = "Patient (" + save_form.name + ") saved done"
            data["type"] = "success"
            return JsonResponse(data)
        else:
            return self.form_invalid(form)

    def get_queryset(self):
        data = {}
        msg = ""
        if self.queryset is not None:
            queryset = self.queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.all()
        elif self.model is not None:
            queryset = self.model._default_manager.all()
        else:
            # raise ImproperlyConfigured
            msg = (
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {"cls": self.__class__.__name__}
            )
            data["msg"] = msg
            data["type"] = "info"
            return JsonResponse(data)

        return self.queryset  # .all()

    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Data for the QR code
        qr_data = f"""
            Patient ID: {self.get_object().id},
            Patient Name: {self.get_object().name}, 
            Card ID: {self.get_object().cardid}, 
            Phone: {self.get_object().phone},
            Mobile: {self.get_object().mobile},
            Birth Date: {self.get_object().birth_date},
            Age: {self.get_object().age},
        """

        # QR code options
        # * qr_options = QRCodeOptions(size="L", border=6, error_correction="L")

        context["qr_data"] = qr_data
        # context["qr_options"] = qr_options

        context["patient_id"] = self.get_object().id
        context["savepatform"] = self.form_class(instance=self.get_object())
        context["patient"] = self.get_object()
        print("QUERYSET>>>", self.get_queryset())
        data = {"var": "Amr Ali Amer"}
        data["title"] = "Edit patient: (" + str(self.get_object().name) + ")"
        return context | data
