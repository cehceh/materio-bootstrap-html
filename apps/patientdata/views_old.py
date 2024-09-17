from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.query import QuerySet
from django.db.models import Q, Count
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.http import JsonResponse


# from django.shortcuts import

from django.contrib import messages
from datetime import date

#
from .forms import PatientsForm
from .models import Patients

# from .tables import PatientsTable

# from apps.pasthistory.models import PastHistory
from apps.visits.models import Visits

# from apps.visits.tables import VisitsTable
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView

from web_project import TemplateLayout


"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to tables/urls.py file for more pages.
"""


class PatientView(CreateView):  # (TemplateView):
    template_name = "save_patient.html"
    form_class = PatientsForm
    queryset = Patients.objects.only()[:100]
    success_url = reverse_lazy("patientdata:save-patient")

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
        if self.request.path == "/patients/add/new/patient/":
            title = "Add New Patient"
        elif self.request.path == "/patients/reservation/area/":
            title = "Reservations"

        context["title"] = title
        context["savepatform"] = self.form_class
        # context["savepatform"] = form.form_valid
        context["qs"] = self.get_queryset()

        data = {"var": "Amr Ali Amer"}
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


class PatientListView(ListView):
    """
    for patient-table, patient-cards and search patients in patient cards
    """

    model = Patients
    # context_object_name = ""
    template_name = "patients_cards/patient_card.html"
    queryset = Patients.objects.only().order_by("-id")  # [:100]

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
        visits = Visits.objects.values_list("patient_id", flat=True).distinct()

        # * For searching on the search input in page-nav.html
        patient_search = self.request.GET.get("pat")
        if (
            patient_search is not None
            and patient_search != ""
            and (patient_search)
            in [str(obj) for obj in Patients.objects.values_list("id", flat=True)]
        ):
            search_result = Patients.objects.filter(Q(id=int(patient_search)))
        elif (
            patient_search is not None
            and patient_search != ""
            and ("pat" in self.request.GET)
            and self.request.GET["pat"].strip()
        ):
            search_result = Patients.objects.filter(
                Q(name__icontains=patient_search)
                | Q(cardid__icontains=patient_search)
                | Q(phone__icontains=patient_search)
                | Q(mobile__icontains=patient_search)
                # | Q(id=int(patient_search))
            )
        else:
            search_result = self.queryset  # Patients.objects.only()

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

        print(
            "SELF>OBJECT-FROM-->GET()::::",
            search_result,
            "\n" "search_result^^^^^^^^",
            search_result,
            "All-PATIENTS-VISITS-COUNT:::::",
            visits,
        )

        # print("patient_id>>^^^", self.kwargs["patient_id"]) -- .aggregate(count=Count('id')
        data["main_page"] = main_page
        data["page"] = page
        data["visits"] = visits
        data["visits_count"] = [
            (
                Visits.objects.values_list("id", flat=True)
                .filter(patient_id=obj)
                .count(),
                obj,
            )
            for obj in visits
        ]

        print()

        if self.request.path == "/patients/list/all/patients/":
            data["patient_id"] = 0
            data["title"] = "All Patients Cards"
        else:
            data["title"] = ""
            data["patient_id"] = self.kwargs["patient_id"]

        data["qs"] = self.queryset  # .order_by("-id")
        return context | data


################################################################################
def save_patient(request):
    """Collecting data for patients function to save patient data to database"""
    if request.method == "POST":
        form = PatientsForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            barcode_value = request.POST.get("barurl")
            if barcode_value is None or barcode_value == "":
                messages.success(request, "Create barcode without value is not valid")
            elif barcode_value is not None:
                # url = pyqrcode.create('anything')
                # url.svg('uca-url.svg', scale=8)
                # url.eps('uca-url.eps', scale=2)

                # qr = pyqrcode.create(barcode_value)
                name = request.POST.get("name")
                # file_path = 'media_root/patients/' + str(name) + '.png'
                # print(file_path)
                # match = Patients.objects.filter(name=name).exists()
                # if not os.path.exists(file_path) and not match:
                #     qr.png('media_root/patients/' + str(name) + '.png', scale=10)
                save_form = form.save(commit=False)
                save_form.barimg = "patients/" + str(name) + ".png"
                save_form.barurl = barcode_value
                save_form.save()
                pat_id = save_form.id
                Visits.objects.create(
                    patient_id=pat_id,
                    visitdate=date.today(),
                    complain="any comp",
                    sign="any sign",
                    amount=0,
                    intervention="any intervention",
                )
                messages.success(request, "Saving process done ... ")
                return redirect("patientdata:table_patient")
                # else:
                #     messages.success(request, 'Barcode is already exists or Patient name is repeated')
                #     return redirect(reverse('patientdata:save_patient'))
    else:
        form = PatientsForm()

    lastid = Patients.objects.values("id").last()
    if lastid is not None:
        patid = lastid["id"] + 1
    else:
        patid = 1
    # print(patid)
    label2 = "Save"
    context = {
        "savepatform": form,
        "lastid": patid,
        # 'button_lable': label,
        "lable2": label2,
    }
    return render(request, "patientdata/save_patient.html", context)


def edit_patient(request, id):  # Making Update to a Patient
    qs = Visits.objects.filter(patient=id).order_by("-id")
    # print('qs = '+str(qs))
    # match_presenthist = PresentHistory.objects.filter(patient=id, visit=1).exists()
    table = VisitsTable(qs, exclude="patient, addpresent")
    table.paginate(page=request.GET.get("page", 1), per_page=10)

    query = Patients.objects.get(id=id)  # get(birth_date=birth_date)
    patient = Patients.objects.values("id").filter(id=id).first()
    barcode = Patients.objects.values("barcode").filter(id=id).first()
    # patient = Patients.objects.filter(id=id)
    patient_id = patient["id"]
    bar = barcode["barcode"]
    # print(query, patient)
    match_pasthist = PastHistory.objects.filter(patient=id).exists()
    # if match_pasthist:
    #     pasthist = PastHistory.objects.values('id').filter(patient=patient_id).first()

    form = PatientsForm(request.POST or None, request.FILES or None, instance=query)
    if form.is_valid():
        save_form = form.save(commit=False)
        save_form.save()
        name = save_form.name
        card = save_form.cardid
        dup_name = (
            Patients.objects.values("name")
            .annotate(ncount=Count("name"))
            .filter(name=name, ncount__gt=1)
        )
        records = Patients.objects.filter(name__in=[item["name"] for item in dup_name])
        # print('rec_edit = '+ str(records) + str(name))#(dup_name, records)
        rec = [item.name for item in records]
        reco = any(rec.count(element) > 1 for element in rec)
        print(
            "patname= " + str(name),
            "rec_edit= " + str(rec),
            "dupname_edit= " + str(dup_name),
            reco,
        )

        # check duplicate for cardid
        dup_num = (
            Patients.objects.values("cardid")
            .annotate(bcount=Count("cardid"))
            .filter(cardid=card, bcount__gt=1)
        )
        records_num = Patients.objects.filter(
            cardid__in=[item["cardid"] for item in dup_num]
        )
        # print('recnum_edit = '+ str(records_num) + str(num))#(dup_name, records)
        rec_num = [item.cardid for item in records_num]
        reco_num = any(rec_num.count(element) > 1 for element in rec_num)
        # print(rec_num, 'reco_num= ' + str(reco_num))

        if reco or reco_num:
            if reco:
                messages.success(
                    request,
                    "Patient (" + str(name) + ") is already exists change the name ..!",
                )
                return redirect(reverse("patientdata:edit_patient", kwargs={"id": id}))
            elif reco_num:
                messages.success(
                    request, "Card ID is already exists !, It must not be duplicated"
                )
                return redirect(reverse("patientdata:edit_patient", kwargs={"id": id}))
        else:
            return redirect(reverse("patientdata:table_patient"))

    # lastid = Patients.objects.values('id').last()
    # patid = lastid['id'] + 1
    context = {
        "patient": patient,
        "patient_id": patient_id,
        "editpatform": form,
        "query": query,
        "barcode": bar,
        "match_pasthist": match_pasthist,
        "patient_visits_table": table,
    }
    return render(request, "patientdata/edit_patient.html", context)


def table_patient(request):
    qs = Patients.objects.all().order_by("-id")

    # search_name = request.GET.get('patname')
    # search_id = request.GET.get('patid')
    # result = Patients.objects.filter(Q(name__icontains=search_name))
    # result_id = Patients.objects.filter(Q(id=search_id))

    page_no = request.GET.get("pageno")
    # if search_name != '':
    #     table = PatientsTable(result)
    #     table.paginate(page=request.GET.get("page", 1), per_page=10)
    # elif search_id != None or search_id != '' or int(search_id) != 0:
    #     table = PatientsTable(result_id)
    # elif search_id == None or search_id == '' or int(search_id) == 0:
    #     table = PatientsTable(qs)
    #     table.paginate(page=request.GET.get("page", 1), per_page=10)
    # elif page_no == None or page_no == '' or int(page_no) == 0:
    #     table = PatientsTable(qs)
    #     table.paginate(page=request.GET.get("page", 1), per_page=10)

    # elif search_name == '':
    #     table = PatientsTable(qs)
    #     table.paginate(page=request.GET.get("page", 1), per_page=10)
    # elif search_name == '' and  page_no == '' and search_id == '':
    #     table = PatientsTable(result)
    #     table.paginate(page=request.GET.get("page", 1), per_page=2)
    if page_no == None or page_no == "" or int(page_no) == 0:
        table = PatientsTable(qs)
        table.paginate(page=request.GET.get("page", 1), per_page=10)
    elif page_no != None or page_no != "" or int(page_no) != 0:
        table = PatientsTable(qs)
        table.paginate(page=request.GET.get("page", 1), per_page=page_no)
    else:
        table = PatientsTable(qs)
        table.paginate(page=request.GET.get("page", 1), per_page=10)

    context = {"table_patient": table}
    return render(request, "patientdata/tables.html", context)


def patient_details(request, barcode):
    qs = Patients.objects.get(barcode=barcode)
    patient = Patients.objects.get(id=qs.id)

    context = {
        "qs": qs,
    }
    return render(request, "patientdata/patient_details.html", context)


def barcode_redirect(request, barcode):
    qs = Patients.objects.get(barcode=barcode)

    return redirect(reverse("patientdata:edit_patient", args=(qs.id)))
