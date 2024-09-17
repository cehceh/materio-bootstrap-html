from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, reverse
from django.db.models.query import QuerySet
from django.db.models import Count, Q, Sum

from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView

from .models import Visits
from .forms import VisitsForm
from apps.patientdata.models import Patients

from apps.presenthistory.models import PresentHistory
from apps.pasthistory.models import PastHistory
from apps.revisits.models import Revisits

from web_project import TemplateLayout

# from .tables import VisitsTable
from apps.visitdrug.models import Medicine
from django.contrib import messages

# from django_tables2.config import RequestConfig
# from django_tables2.export.export import TableExport


class VisitView(CreateView):  # (TemplateView):
    template_name = "visits/add_visit.html"
    form_class = VisitsForm
    queryset = Visits.objects.only()[:100]
    success_url = reverse_lazy("visits:add-visit")

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        data = {}
        diagnosis = self.request.POST.get("diagnosis")
        if diagnosis == "" or diagnosis is None:
            data["msg"] = "Diagnosis must not be empty"
            data["type"] = "error"
            return JsonResponse(data)

        form = self.get_form()
        if form.is_valid():
            # return self.form_valid(form)
            data = {}
            print("I am here in form_valid", request.POST.get("visit-count"))

            save_form = form.save(commit=False)
            save_form.patient_id = self.kwargs["patient_id"]
            save_form.visit_count = request.POST.get("visit-count")
            # self.get_context_data["visits_count"]  #
            save_form.save()

            data["msg"] = "Visit for(" + save_form.patient.name + ") saved done"
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

    def get_queryset(self):
        """overriding this method in order to pass a parameter to your url path"""
        patient = Patients.objects.get(id=self.kwargs["patient_id"])
        print(
            "self.kwargs['patient_id']-FROM-GET_QUERYSET::", self.kwargs["patient_id"]
        )
        return patient  # super().get_queryset()

    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        # context |= {"var": "Amr Amer"}
        visits_count = Visits.objects.filter(
            patient_id=self.kwargs["patient_id"]
        ).aggregate(count=Count("id"))
        if visits_count["count"] == 0:
            count = 1
        else:
            count = visits_count["count"] + 1

        context["save_visits_form"] = self.form_class
        context["visits_count"] = count
        context["qs"] = self.get_queryset()
        print(
            'self.kwargs.get["patient_id"]',
            self.kwargs["patient_id"],
            "visits_count>>>",
            visits_count,
        )
        data = {"patient_id": self.kwargs.get("patient_id")}
        data["title"] = "New Visit for patient:(" + str(self.get_queryset().name) + ")"
        return context | data


class VisitUpdateView(UpdateView):
    model = Visits
    template_name = "visits/edit_visit.html"
    pk_url_kwarg = "visit_id"
    queryset = Visits.objects.only()
    form_class = VisitsForm
    template_name_suffix = "_update_form"
    success_url = reverse_lazy("visits:edit-visit")

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
        print(
            "SELF.OBJECT^^^^^^^",
            self.object,
        )
        data = {}
        diagnosis = self.request.POST.get("diagnosis")
        if diagnosis == "" or diagnosis is None:
            data["msg"] = "Diagnosis must not be empty"
            data["type"] = "error"
            return JsonResponse(data)

        form = self.get_form()
        if form.is_valid():
            # return self.form_valid(form)
            data = {}
            print("I am here in form_valid")

            save_form = form.save(commit=False)
            save_form.patient_id = self.kwargs["patient_id"]
            save_form.visit_count = request.POST.get("visit-count")
            save_form.save()

            data["msg"] = "Patient (" + str(save_form.patient) + ") saved done"
            data["type"] = "success"
            return JsonResponse(data)
        else:
            return self.form_invalid(form)

    def get_queryset(self):
        # visit = Visits.objects.get(id=self.kwargs["visit_id"])
        # patient = Patients.objects.get(id=self.kwargs["patient_id"])
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

        return self.queryset

    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        patient_visits = Visits.objects.filter(patient_id=self.kwargs["patient_id"])
        visits_length = [obj for obj in patient_visits.values_list("id", flat=True)]
        visits_count = patient_visits.aggregate(count=Count("id"))
        # ids_list = [obj for index, obj in enumerate(visits_length)]
        first_id = patient_visits.first().id
        current_id = self.kwargs["visit_id"]
        last_id = patient_visits.last().id

        before_current_id = []
        before_index = []
        next_current_id = []
        next_index = []

        current_index = [i for i, obj in enumerate(visits_length) if obj == current_id][
            0
        ]

        if current_id != first_id:
            before_current_id = [
                obj for i, obj in enumerate(visits_length) if i == current_index - 1
            ][0]
            before_index = [
                i for i, obj in enumerate(visits_length) if i == current_index - 1
            ][0] + 1
        if current_id != last_id:
            next_current_id = [
                obj for i, obj in enumerate(visits_length) if i == current_index + 1
            ][0]
            next_index = [
                i for i, obj in enumerate(visits_length) if i == current_index + 1
            ][0] + 1
        print("first_id", first_id)
        print(
            "last_id",
            last_id,
            "LIST IDS >>>> ",
            [(obj, i) for obj, i in enumerate(visits_length)],
            "current_index",
            current_index,
            "before_current_id",
            before_current_id,
            "next_current_id",
            next_current_id,
            [(i, obj) for i, obj in enumerate(visits_length) if i == current_index - 1],
        )

        context["visits_count"] = len(visits_length)
        #
        context["last_id"] = last_id  # patient_visits.last().id

        context["first_id"] = first_id
        context["before_current_id"] = before_current_id
        context["before_index"] = before_index
        context["current_id"] = current_id
        context["current_index"] = [
            i for i, obj in enumerate(visits_length) if obj == current_id
        ][0] + 1
        context["next_current_id"] = next_current_id
        context["next_index"] = next_index
        context["visit_id"] = self.kwargs["visit_id"]  # self.get_object()[0].id
        context["patient_id"] = self.kwargs["patient_id"]
        # self.get_object()[0].patient.id
        context["save_visits_form"] = self.form_class(instance=self.get_object())
        context["patient"] = patient_visits.first().patient  # self.get_queryset()
        data = {}
        data["visits_length"] = [
            (index + 1, obj) for index, obj in enumerate(visits_length)
        ]
        data["visits_ids"] = [obj for index, obj in enumerate(visits_length)]
        # visit_list_view = VisitListView()
        data["title"] = (
            "Edit visit for patient: (" + str(patient_visits.first().patient) + ")"
        )
        print(
            "self.get_queryset()^^>>",
            self.get_queryset(),
            "self.get_object()^^>>",
            self.get_object(),
            [obj for index, obj in enumerate(visits_length)],  # "visits_length"
        )
        return context | data


class VisitListView(ListView):
    """
    Displaying visits card for every patient and visits table
    """

    model = Visits
    # context_object_name = ""
    template_name = "visits/visits_table.html"
    queryset = Visits.objects.only()  # [:100]
    visits_url = "/visits/table/list/every/visits/"

    def get_queryset(self):
        # return super().get_queryset()
        if self.request.path == self.visits_url:
            patient = []
            # ? for the all visits table for all patients
            all_patient_visits = Visits.objects.select_related("patient").order_by(
                "-id"
            )
        else:
            patient = Patients.objects.get(id=self.kwargs["patient_id"])
            # ? All visits for one spcefic patient
            all_patient_visits = Visits.objects.filter(
                patient_id=self.kwargs["patient_id"]
            ).order_by("-id")
        print(
            # "self.kwargs['patient_id']-FROM-GET_QUERYSET::",
            "all_patient_visits>>!!!",
            all_patient_visits,
        )
        return patient, all_patient_visits

    def get_context_data(self, **kwargs):
        data = {}
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        # print("self.get_queryset()[1]>>>", self.get_queryset()[1])

        # patient_search not in [
        #     Visits.objects.filter(patient_id=self.kwargs["patient_id"])
        # ]:
        #     search_result = self.get_queryset()[1]
        #     print("I-AM-ALL-VISITS-ALSO>>>", search_result)
        # ?
        if self.request.path == self.visits_url:
            patient_visits = Visits.objects.select_related("patient")
            main_page = patient_visits
            page = ""
        else:
            patient_visits = Visits.objects.filter(patient_id=self.kwargs["patient_id"])
            # * next code for searching in one input in all patient's visits
            patient_search = self.request.GET.get("pat")
            print("PAT-INPUT::::", patient_search)
            if (
                patient_search is not None
                and patient_search != ""
                and (patient_search)
                in [
                    str(obj)
                    for obj in Visits.objects.filter(
                        patient_id=self.kwargs["patient_id"]
                    ).values_list("id", flat=True)
                ]
                or (patient_search)
                in [
                    str(obj)
                    for obj in Visits.objects.filter(
                        patient_id=self.kwargs["patient_id"]
                    ).values_list("visit_count", flat=True)
                ]
            ):
                search_result = Visits.objects.filter(
                    Q(id=int(patient_search)) | Q(visit_count=int(patient_search))
                ).filter(patient_id=self.kwargs["patient_id"])
                print(
                    "I-AM-INT>>>",
                    search_result,
                )
            elif (
                patient_search is not None
                and patient_search != ""
                and ("pat" in self.request.GET)
                and self.request.GET["pat"].strip()
            ):
                search_result = Visits.objects.filter(
                    Q(patient__name__icontains=patient_search)
                    | Q(visitdate__icontains=patient_search)
                    | Q(diagnosis__icontains=patient_search)
                    | Q(intervention__icontains=patient_search)
                ).filter(patient_id=self.kwargs["patient_id"])
                print("I-AM-STR>>>", search_result)
            else:
                search_result = Visits.objects.filter(
                    patient_id=self.kwargs["patient_id"]
                )
                print("I-AM-ALL-VISITS>>>", search_result)

            # * next lines for pagination
            paginator = Paginator(search_result, 5)
            page = self.request.GET.get("page")

            try:
                main_page = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer deliver the first page
                main_page = paginator.page(1)
            except EmptyPage:
                # If page is out of range deliver last page of results
                main_page = paginator.page(paginator.num_pages)

        visits_count = patient_visits.aggregate(count=Count("id"))
        total_visits_amount = patient_visits.aggregate(sum_amount=Sum("amount"))
        visits_length = [obj for obj in patient_visits.values_list("id", flat=True)]
        print(
            # "SELF.QUERYSET>>>",
            # self.queryset,
            # "INDEX::::",
            # # len(visits_length),
            # [(index + 1, obj) for index, obj in enumerate(visits_length)],
            # [(index + 1) for index in range(len(visits_length))],
        )

        data["main_page"] = main_page
        data["patient_visits"] = patient_visits
        data["page"] = page
        data["visits_count"] = visits_count["count"]
        data["total_amount"] = total_visits_amount["sum_amount"]

        data["visits_length"] = [
            (index + 1, obj) for index, obj in enumerate(visits_length)
        ]
        path = self.request.path
        # print("GET-QUERYSET:>>>", self.get_queryset()[1])
        data["patient_id"] = (
            self.get_queryset()[0].id if path != self.visits_url else None
        )
        data["patient"] = self.get_queryset()[0] if path != self.visits_url else None
        data["qs"] = self.queryset
        data["title"] = (
            "All visits of: " + self.get_queryset()[0].name
            if path != self.visits_url
            else "All Visits In The Clinic"
        )
        print(
            # "PATIENT>>>", self.get_queryset()[0], "VISITS>>>", self.get_queryset()[1]
            "VALUES-LIST-IDS>>>>",
            # [
            #     obj
            #     for obj in Visits.objects.filter(
            #         patient_id=self.kwargs["patient_id"]
            #     ).values_list("id", flat=True)
            #     if path != self.visits_url
            # ],
        )
        return context | data


####################################################################################################
def export_table(request):
    table = VisitsTable(Visits.objects.all())

    RequestConfig(request).configure(table)

    export_format = request.GET.get("csv, json", None)
    if TableExport.is_valid_format(export_format):
        # exclude columns while creating the TableExport instance:
        # exporter = TableExport("csv", table, exclude_columns=("image", "buttons"))
        exporter = TableExport(
            export_format, table, dataset_kwargs={"title": "My Custom Sheet Name"}
        )
        # exporter = TableExport(export_format, table)
        return exporter.response("table.{}".format(export_format))

    return render(
        request,
        "tables.html",
        {
            "export_table": table,
        },
    )


# old save visit
# def save_visits(request): # save without
#     ''' Method for saving patient's visits '''
#     if request.method == 'POST':
#         form = VisitsForm(request.POST or None)
#         if form.is_valid():
#             # patient_id = form.cleaned_data['patient_id']
#             form.save()
#             return redirect('/clinic/table/visits/')
#     else:
#         form = VisitsForm()
#     context = {
#         'save_visits_form': form,
#     }
#     return render(request, 'clinic/forms.html', context)


# new save visit
def pass_patient_id(request, id):  # Making save to new visits
    patient = Patients.objects.get(id=id)  # out put is the patient name
    patient_id = (
        Patients.objects.values("id").filter(id=id).first()
    )  # This is out put of without .first()=> <QuerySet [{'id': 36}]>
    var = patient_id["id"]
    # var1 = Patients.objects.values('mobile').filter(id=id).first()
    # var11 = var1['mobile']
    # print(patient, patient_id)
    match_pasthist = PastHistory.objects.filter(patient=id).exists()

    bound_form = VisitsForm(data={"patient": patient})

    if request.method == "POST":
        form = VisitsForm(request.POST or None)
        if form.is_valid():
            save_form = form.save(commit=False)
            save_form.patient_id = var
            save_form.save()
            visit_id = save_form.id
            # name = save_form.patient
            messages.success(
                request, "Saving new visit for (" + str(patient) + ") done"
            )
            return redirect(
                reverse(
                    "visits:visits_patient_id", args=(visit_id, save_form.patient_id)
                )
            )  # ('visits:table_visits')
    else:
        form = VisitsForm()
    context = {
        "pat_id": var,
        "patient": patient,
        "match_pasthist": match_pasthist,
        "save_visits_form": form,
        "bound_form": bound_form,
    }
    return render(request, "visits/add_visit.html", context)


# new edit visit
def visits_patient_id(
    request, id, patient_id
):  # Making Update to a visit with knowing the patient id
    query = Visits.objects.get(id=id)  # out put Visit ID
    qs = (
        Visits.objects.values("id", "patient_id")
        .filter(id=id, patient_id=patient_id)
        .first()
    )  # {'patient_id': 2}
    # for get_url() to redirect to -save present history- form
    visid = (
        Visits.objects.values("id").filter(id=id).first()
    )  # {'id': 136, 'patient': 15}
    vis_id = visid["id"]

    match_medicine = Medicine.objects.filter(visit=id).exists()
    # if match_medicine:
    #     medicine = Medicine.objects.get(visit=id)
    # else:
    #     medicine = None

    match_present = PresentHistory.objects.filter(visit=id).exists()
    # if not match_present:
    #     present = None #PresentHistory.objects.all()
    # else:

    present = PresentHistory.objects.values("id").filter(visit=id).first()
    if present != None:
        presentid = present["id"]
    else:
        presentid = 0
    # print(present, presentid)
    if presentid == 0:
        present_qs = 0
    else:
        present_qs = PresentHistory.objects.get(id=presentid)

    match_revisit = Revisits.objects.filter(visit=id).exists()

    patient = Patients.objects.get(id=patient_id)  # Use it with get_absolute_url()
    patientid = qs["patient_id"]  # out put is Patient ID
    form = VisitsForm(request.POST or None, instance=query)
    if form.is_valid():
        # patid = request.POST.get('patient')
        # # print('patid : ' + str(patid))
        # match = Visits.objects.filter(patient_id=patid, id=id).exists()
        # if match:
        save_form = form.save(commit=False)
        save_form.patient_id = patient_id
        # save_form.visit_id = id
        save_form.save()
        messages.success(
            request, "Update visit no. (" + str(vis_id) + ") done successfully"
        )
        return redirect(
            reverse("visits:visits_patient_id", args=(vis_id, patientid))
        )  # ('/clinic/table/')
        #  HTTPResponseRedirect(reverse('clinic:edit_patient', kwargs={'id': id}))
        # else:
        #     messages.success(request, 'The Patient Name Must Be : ' + \
        #     str(patient) + ', With Patient ID : ' + str(patient_id) + ' Not Ptient ID : ' + str(patid))

    context = {
        # 'saveDone': match,
        "patient": patient,
        "patient_id": patientid,
        "visit": query,
        "vis_id": vis_id,
        "qs": qs,
        "medicine": match_medicine,
        # 'medicine_id': medicine,
        "match_present": match_present,
        "present_id": present_qs,
        "match_revisit": match_revisit,
        # 'revisit': revisit,
        "edit_visits_form": form,
    }
    return render(request, "visits/edit_visit.html", context)


def table_visits(request):
    qs = Visits.objects.select_related("patient").order_by(
        "-id"
    )  # the next lines are the result of this query ORM
    # qs = Medicine.objects.select_related('patient').order_by('-id')
    # ''' SELECT "clinic_visits"."id", "clinic_visits"."patient_id", "clinic_visits"."visitdate",
    # "clinic_visits"."complain", "clinic_visits"."sign", "clinic_visits"."diagnosis", "clinic_visits"."intervention",
    # "clinic_visits"."amount", "clinic_patients"."id", "clinic_patients"."name", "clinic_patients"."address",
    # "clinic_patients"."birth_date", "clinic_patients"."age", "clinic_patients"."phone", "clinic_patients"."mobile",
    # "clinic_patients"."cardid" FROM "clinic_visits"
    # LEFT OUTER JOIN "clinic_patients"
    # ON ("clinic_visits"."patient_id" = "clinic_patients"."id")
    # ORDER BY "clinic_visits"."id" DESC '''

    # qs = Visits.objects.all().order_by('-id')
    page_no = request.GET.get("pageno")
    if page_no == None or int(page_no) == 0 or page_no == "":
        table = VisitsTable(qs, exclude="addpresent")
        table.paginate(page=request.GET.get("page", 1), per_page=100)
    else:
        table = VisitsTable(qs, exclude="addpresent")
        table.paginate(page=request.GET.get("page", 1), per_page=page_no)

    print(qs.query)
    context = {
        "qs_table": qs,
        "visits_table": table,
    }
    return render(request, "visits/tables.html", context)


# HttpResponse for http direct write
