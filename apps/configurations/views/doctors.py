from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.query import QuerySet
from django.db.models import Q, Count
from django.urls import reverse_lazy
from django.http import JsonResponse

from ..models import DoctorNames  # noqa: F811
from ..forms import DoctorNamesForm

from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView

from web_project import TemplateLayout


"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to tables/urls.py file for more pages.
"""


class DoctorView(CreateView):  # (TemplateView):
    template_name = "configurations/doctors/add_doctors.html"
    form_class = DoctorNamesForm
    queryset = DoctorNames.objects.only()[:100]
    success_url = reverse_lazy("configurations:add-doctor")

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
            # save_form.age = request.POST.get("age")
            save_form.save()

            data["doctor_name_id"] = save_form.id
            data["msg"] = "Doctor (" + save_form.name + ") saved done"
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
            return JsonResponse(data, safe=False)
        return self.render_to_response(self.get_context_data(form=form))

    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        title = ""  # noqa: F841
        # context |= {"var": "Amr Amer"}
        lastid = DoctorNames.objects.values("id").last()
        doctorid = lastid["id"] + 1 if lastid else 1
        context["lastid"] = doctorid
        doctor_count = DoctorNames.objects.aggregate(count=Count("id") + 1)
        context["doctor_count"] = str(doctor_count["count"])
        # if self.request.path == "/patients/add/new/patient/":
        #     title = "Add New Patient"
        # elif self.request.path == "/patients/reservation/area/":
        #     title = "Reservations"

        context["title"] = "Add New Doctor"
        context["form"] = self.form_class
        # context["savepatform"] = form.form_valid
        context["qs"] = self.get_queryset()

        data = {"var": "Amr Ali Amer"}
        return context | data


class DoctorUpdateView(UpdateView):
    model = DoctorNames
    template_name = "configurations/doctors/edit_doctors.html"
    pk_url_kwarg = "id"
    queryset = DoctorNames.objects.all()
    form_class = DoctorNamesForm
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("configurations:edit-doctor-names")

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
            # save_form.updated = request.user
            if form.has_changed():
                save_form.save()
            else:
                data["msg"] = "No changes made ..."
                data["type"] = "info"
                return JsonResponse(data, safe=False)

            data["msg"] = "Doctor (" + save_form.name + ") updated done"
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
        # doctor_instance = DoctorView()
        # print("DOCTOR-INSTANCE>>>>", doctor_instance.get_context_data())

        # Data for the QR code
        qr_data = f"""
            Doctor ID: {self.get_object().id},
            Doctor Name: {self.get_object().name}, 
            Description: {self.get_object().description}, 
            
        """

        # QR code options
        # * qr_options = QRCodeOptions(size="L", border=6, error_correction="L")

        context["qr_data"] = qr_data
        # context["qr_options"] = qr_options

        context["doctor_id"] = self.get_object().id
        context["form"] = self.form_class(instance=self.get_object())
        context["doctor"] = self.get_object()
        print("QUERYSET>>>", self.get_queryset())
        data = {}
        data["title"] = "Edit doctor: (" + str(self.get_object().name) + ")"
        return context | data


class DoctorListView(ListView):
    """
    for patient-table, patient-cards and search patients in patient cards
    """

    model = DoctorNames

    template_name = "doctors/doctors_table.html"
    queryset = DoctorNames.objects.only().order_by("-id")  # [:100]

    # def get(self, request, *args, **kwargs):
    #     patient_search = request.GET.get("pat")
    #     if patient_search is not None and patient_search != "":
    #         search_result = Patients.objects.filter(id=patient_search)
    #     else:
    #         search_result = Patients.objects.only()

    #     print("SELF>OBJECT-FROM-->GET()::::", search_result)
    #     return super().get(request, *args, **kwargs)

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

        return super().get_queryset()

    def get_context_data(self, **kwargs):
        data = {}
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        # visits = Visits.objects.values_list("patient_id", flat=True).distinct()

        # * For searching on the search input in page-nav.html
        doctor_search = self.request.GET.get("doctor")
        if (
            doctor_search is not None
            and doctor_search != ""
            and (doctor_search)
            in [str(obj) for obj in DoctorNames.objects.values_list("id", flat=True)]
        ):
            search_result = DoctorNames.objects.filter(Q(id=int(doctor_search)))
        elif (
            doctor_search is not None
            and doctor_search != ""
            and ("doctor" in self.request.GET)
            and self.request.GET["doctor"].strip()
        ):
            search_result = DoctorNames.objects.filter(
                Q(name__icontains=doctor_search)
                # | Q(cardid__icontains=patient_search)
                # | Q(phone__icontains=patient_search)
                # | Q(mobile__icontains=patient_search)
                # | Q(id=int(patient_search))
            )
        else:
            search_result = self.queryset

        # * next lines for pagination
        paginator = Paginator(search_result, 4)
        page = self.request.GET.get("page")

        try:
            main_page = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            main_page = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            main_page = paginator.page(paginator.num_pages)

        print()

        # print("patient_id>>^^^", self.kwargs["patient_id"]) -- .aggregate(count=Count('id')
        data["main_page"] = main_page
        data["page"] = page
        # data["visits"] = visits
        # data["visits_count"] = [
        #     (
        #         Visits.objects.values_list("id", flat=True)
        #         .filter(patient_id=obj)
        #         .count(),
        #         obj,
        #     )
        #     for obj in visits
        # ]

        if self.request.path == "/patients/list/all/patients/":
            data["doctor_id"] = 0
            data["title"] = "All Patients Cards"
        else:
            data["title"] = ""
            data["doctor_id"] = self.kwargs["id"]

        data["qs"] = self.queryset  # .order_by("-id")
        return context | data
