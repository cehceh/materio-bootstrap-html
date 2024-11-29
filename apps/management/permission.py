from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView

from django.db.models.query import QuerySet

from web_project import TemplateLayout
from apps.users.models import CustomUser
from apps.management.forms import UserPermissionsForm


class PermissionView(CreateView):  # (TemplateView):
    template_name = "configurations/doctors/add_doctors.html"
    form_class = UserPermissionsForm
    queryset = CustomUser.objects.values(
        "id",
        "username",
        "role",
        "mobile1",
        "is_active",
        "user_permissions__codename",
        "groups__name",
        "groups__permissions__name",
        "groups__permissions__content_type",
        "groups__permissions__codename",
    )
    # CustomUser.objects.only()  # DoctorNames.objects.only()[:100]
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
        # lastid = DoctorNames.objects.values("id").last()
        # doctorid = lastid["id"] + 1 if lastid else 1
        # context["lastid"] = doctorid
        # doctor_count = DoctorNames.objects.aggregate(count=Count("id") + 1)
        # context["doctor_count"] = str(doctor_count["count"])

        if self.request.path == "/patients/add/new/patient/":
            title = "Add New Patient"
        elif self.request.path == "/management/users/permissions/table/":
            title = "List Permissions"

        context["title"] = title
        context["form"] = self.form_class
        # context["savepatform"] = form.form_valid
        context["qs"] = self.queryset  # self.get_queryset()

        data = {"var": "Amr Ali Amer"}
        return context | data


class PermissionListView(ListView):
    """
    for permission-table, permission-cards
    """

    model = CustomUser
    template_name = "management/permission/patients_table.html"
    # template_name = "management/permission/permission_table.html"
    queryset = CustomUser.objects.only().order_by("-id")

    # CustomUser.objects.values(
    #     "id",
    #     "username",
    #     "role",
    #     "mobile1",
    #     "is_active",
    #     "user_permissions__codename",
    #     "groups__name",
    #     "groups__permissions__name",
    #     "groups__permissions__content_type",
    #     "groups__permissions__codename",
    # )
    # .annotate(cus_id="id", distinct=True)
    # .distinct("id")
    # CustomUser.objects.only().order_by("-id")  # [:100]

    # def get(self, request, *args, **kwargs):
    #     data = {}
    #     show_main = request.GET.get("main")
    #     if show_main == "true":
    #         permission = Permission.objects.values("name", "codename", "content_type")
    #         main = CustomUser.objects.values(
    #             "id",
    #             "username",
    #             "role",
    #             "mobile1",
    #             "is_active",
    #             "user_permissions__codename",
    #             "groups__name",
    #             "groups__permissions__name",
    #             "groups__permissions__content_type",
    #             "groups__permissions__codename",
    #         )
    #         # .annotate("id", distinct=True)
    #         # main = CustomUser.objects.prefetch_related(
    #         #     'groups__permissions'  # Prefetch groups and related permissions
    #         # ).values("username")
    #         # "groups__permissions__name", "groups__permissions__content_type", "groups__permissions__codename"
    #         # main = Permission.objects.values(
    #         #     'id', 'name', 'content_type', 'codename'
    #         # )

    #         data["main-list"] = [obj for obj in main]
    #         data["codename"] = [obj for obj in permission]

    #         print(
    #             "data['main-list'] ***",
    #             data["main-list"],
    #             "main.query******>",
    #             main.query,
    #         )
    #         return JsonResponse(data, safe=False)

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

        # * For searching on the search input in page-nav.html
        # search = self.request.GET.get("search")
        # if (
        #     search is not None
        #     and search != ""
        #     and (search)
        #     in [str(obj) for obj in CustomUser.objects.values_list("id", flat=True)]
        # ):
        #     search_result = CustomUser.objects.filter(Q(id=int(search)))
        # elif (
        #     search is not None
        #     and search != ""
        #     and ("search" in self.request.GET)
        #     and self.request.GET["search"].strip()
        # ):
        #     search_result = CustomUser.objects.filter(
        #         Q(name__icontains=search)
        #         # | Q(cardid__icontains=patient_search)
        #         # | Q(phone__icontains=patient_search)
        #         # | Q(mobile__icontains=patient_search)
        #         # | Q(id=int(patient_search))
        #     )
        # else:
        #     search_result = self.queryset

        # # * next lines for pagination
        # paginator = Paginator(search_result, 4)
        # page = self.request.GET.get("page")

        # try:
        #     main_page = paginator.page(page)
        # except PageNotAnInteger:
        #     # If page is not an integer deliver the first page
        #     main_page = paginator.page(1)
        # except EmptyPage:
        #     # If page is out of range deliver last page of results
        #     main_page = paginator.page(paginator.num_pages)

        print("WHAT-IS-GOING-ON-HERE>>>>>>>>>>>>>>>")

        # print("patient_id>>^^^", self.kwargs["patient_id"]) -- .aggregate(count=Count('id')
        # data["main_page"] = main_page
        # data["page"] = page

        # if self.request.path == "/patients/list/all/patients/":
        #     data["doctor_id"] = 0
        #     data["title"] = "All Patients Cards"
        # else:
        #     data["title"] = ""
        #     data["doctor_id"] = self.kwargs["id"]
        context["title"] = "PERMISSION TABLE"
        data["qs"] = self.queryset  # .order_by("-id")
        return context | data

    # ?????????????????????????????????????????????????????????????????????????????????????????????????????????????
    ###############################################################################################################
    # def permission_table(request):
    #     permission = Permission.objects.values("id", "name", "codename", "content_type")
    #     # values_list('codename', flat=True)
    #     # print('permisssion',[obj for obj in permission])
    #     show_log = request.GET.get("show-log")
    #     show_deleted = request.GET.get("show-deleted")
    #     in_active = request.GET.get("in-active")
    #     is_active = request.GET.get("is-active")
    #     show_main = request.GET.get("show-main")

    #     print(
    #         # 'TYPE****', type,
    #         "show_log@@@@@@@@@@@",
    #         show_log,
    #         "SHOW DELETEDDDDDD",
    #         show_deleted,
    #         "INACTIVEEEEE",
    #         in_active,
    #         "ACTIVEEEEE",
    #         is_active,
    #         "SHOWMAINNNNNN",
    #         show_main,
    #         "permission>>>>::::",
    #         permission,
    #     )

    #     data = {}
    #     main = []
    #     log = []

    #     active = []
    #     inactive = []
    #     delete = []
    #     total_main = 0
    #     if show_main == "true":
    #         # permission = Permission.objects.values('name', 'codename', 'content_type')
    #         main = CustomUser.objects.values(
    #             "id",
    #             "username",
    #             "role",
    #             "mobile1",
    #             "is_active",
    #             "user_permissions__codename",
    #             "groups__name",
    #             "groups__permissions__name",
    #             "groups__permissions__content_type",
    #             "groups__permissions__codename",
    #         )
    #         # .annotate("id", distinct=True)
    #         # main = CustomUser.objects.prefetch_related(
    #         #     'groups__permissions'  # Prefetch groups and related permissions
    #         # ).values("username")
    #         # "groups__permissions__name", "groups__permissions__content_type", "groups__permissions__codename"
    #         # main = Permission.objects.values(
    #         #     'id', 'name', 'content_type', 'codename'
    #         # )

    #         data["main-list"] = [obj for obj in main]
    #         data["codename"] = [obj for obj in permission]

    #         print(
    #             "data['main-list'] ***", data["main-list"], "main.query******>", main.query
    #         )
    #         return JsonResponse(data, safe=False)
    #     elif show_log == "true":
    #         log_qs = CustomUser.objects.values(
    #             "id",
    #             "username",
    #             "role",
    #             "mobile1",
    #             "is_active",
    #             "date_joined",
    #             "last_login",
    #         )
    #         log = log_qs
    #         data["log-list"] = [obj for obj in log]
    #         print("data['log-list'] ***", data["log-list"], "main.query******>", log.query)
    #         return JsonResponse(data, safe=False)
    #     elif in_active == "true":
    #         inactive = (
    #             CustomUser.objects.values(
    #                 "id",
    #                 "username",
    #                 "role",
    #                 "mobile1",
    #                 "is_active",
    #             )
    #             .filter(is_active=False)
    #             .order_by("-id")
    #         )
    #         # main = []
    #         data["inactive-list"] = [obj for obj in inactive]
    #         return JsonResponse(data, safe=False)
    #     elif is_active == "true":
    #         active = (
    #             CustomUser.objects.values("id", "username", "role", "mobile1", "is_active")
    #             .filter(is_active=True)
    #             .order_by("-id")
    #         )
    #         data["active-list"] = [obj for obj in active]
    #         print(
    #             "data['active-list'] ***",
    #             data["active-list"],
    #             "main.query******>",
    #             active.query,
    #         )
    #         return JsonResponse(data, safe=False)

    #     total_inv = CustomUser.objects.values("id").filter().count()
    #     total_active = CustomUser.objects.values("id").filter(is_active=True).count()
    #     total_inactive = CustomUser.objects.values("id").filter(is_active=False).count()

    #     context = {
    #         "total_inv": total_inv,
    #         "total_active": total_active,
    #         "total_inactive": total_inactive,
    #         "title": "Permission Table",
    #     }
    #     return render(request, "management/permission/permission_table.html", context)

    """?
        data['main-list'] *** [
            {'id': 2, 'password': 'pbkdf2_sha256$600000$Z9AVWjTqlEw1cE5WQXhk3q$ZlX//qTrHzXONpcO31OlZaId156Qv9XbtPO2hCBsV/A=', 'last_login': None, 'is_superuser': False, 'username': 'user-1', 'first_name': '', 'last_name': '', 'email': '', 'is_staff': False, 'is_active': True, 'date_joined': datetime.datetime(2024, 8, 29, 7, 46, 20, 951195, tzinfo=datetime.timezone.utc), 'mobile1': '010000', 'mobile2': None, 'phone': None, 'role': 'employee'}, 
            {'id': 3, 'password': 'pbkdf2_sha256$600000$kJ8MWcRT1Up7p2qPTtveAb$xASZ7Pp1q+yhpl5T9VSiSl/Ke0j8dqyCj5aDUwMT9Es=', 'last_login': None, 'is_superuser': False, 'username': 'user', 'first_name': '', 'last_name': '', 'email': '', 'is_staff': False, 'is_active': True, 'date_joined': datetime.datetime(2024, 8, 29, 7, 48, 25, 229408, tzinfo=datetime.timezone.utc), 'mobile1': '010', 'mobile2': None, 'phone': None, 'role': 'employee'}, 
            {'id': 4, 'password': 'pbkdf2_sha256$600000$5ZJFwmp1QiTWLHwNDbQF6F$6UwA5q3/Sry9n5+iHtuEsWZGiFYM5jBfu2Rbzzl/k7M=', 'last_login': None, 'is_superuser': False, 'username': 'cashier1', 'first_name': '', 'last_name': '', 'email': '', 'is_staff': False, 'is_active': True, 'date_joined': datetime.datetime(2024, 8, 30, 4, 43, 20, 127850, tzinfo=datetime.timezone.utc), 'mobile1': '010999', 'mobile2': None, 'phone': None, 'role': 'cashier'}, 
            {'id': 5, 'password': 'pbkdf2_sha256$600000$9eAIVuSHZsT2LTTVjLI3G1$wsoA7SKSUU28qwcU5/g9whhDAHlBAKdNk3U1C74HZbA=', 'last_login': datetime.datetime(2024, 9, 1, 7, 42, 49, 128791, tzinfo=datetime.timezone.utc), 'is_superuser': False, 'username': 'cashier2', 'first_name': '', 'last_name': '', 'email': '', 'is_staff': False, 'is_active': True, 'date_joined': datetime.datetime(2024, 8, 30, 4, 50, 38, 293250, tzinfo=datetime.timezone.utc), 'mobile1': '0109992', 'mobile2': None, 'phone': None, 'role': 'cashier'}, 
            {'id': 1, 'password': 'pbkdf2_sha256$600000$sQaPoZm93xHJsAueZmldUm$m2y6DFvAsj5btliJw5WARyinPwYuiLtlm/yZHLooCu4=', 'last_login': datetime.datetime(2024, 9, 19, 7, 28, 5, 418295, tzinfo=datetime.timezone.utc), 'is_superuser': True, 'username': 'gold', 'first_name': '', 'last_name': '', 'email': '', 'is_staff': True, 'is_active': True, 'date_joined': datetime.datetime(2024, 8, 16, 13, 2, 58, 398116, tzinfo=datetime.timezone.utc), 'mobile1': '01067174141', 'mobile2': None, 'phone': None, 'role': 'admin'}] 
    """
