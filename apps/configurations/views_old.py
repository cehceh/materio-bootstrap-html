from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

from django.db.models import Q
from .models import UnitNames
from .forms import UnitNamesForm
from config.utils import model_id_restriction


# @auth_user_required
def add_unit_names(request):
    data = {}
    data["unit_name_id"] = None
    data["error"] = "ERROR !!!"
    data["type"] = "error"
    if request.accepts("*/*") and request.method == "POST":
        form = UnitNamesForm(request.POST or None)
        unit_name = "any_name_before_saving"
        # save_form = None
        print("formError******", form.errors.get_json_data())
        """
           #? "formError****** {'branch': [{'message': 'Please choose a branch', 'code': ''}]}"
        """
        if not form.is_valid():
            data["unit_name_id"] = None
            # data['pro_id'] = None

            msg = [
                ("UOM " + key + " Error:", value[0]["message"])
                for key, value in (form.errors.get_json_data().items())
            ]
            data["error"] = msg
            data["type"] = "error"
            return JsonResponse(data)

        if form.is_valid():
            save_form = form.save(commit=False)
            save_form.user = request.user
            save_form.updated_user = request.user
            save_form.active = True
            save_form.save()
            UnitNames.objects.filter(id=save_form.id).update(
                code="uom-" + str(save_form.id)
            )

            msg = 'Unit with name "%s" saved successfully' % (unit_name)
            data["unit_name_id"] = save_form.id
            data["error"] = msg
            data["type"] = "success"
            return JsonResponse(data)

            # name = request.POST.get("name")
            # match = UnitNames.objects.filter(name=name).exists()

            # if not match:
            #     save_form.save()
            #     name = save_form.name
            #     unit_name_id = save_form.id
            #     # unit_name = UnitNames.objects.last()
            #     data['unit_name_id'] = unit_name_id
            #     data['last_unit_name'] = name

            # messages.success(request, f"Unit name ({name}) created successfully.")
            # return redirect(request.META.get('HTTP_REFERER', ''))
            # return redirect(
            #     reverse("configurations:edit_unit_names", args=(unit_name_id,))
            # )
            # else:
            #     # unit_name = "None2"
            #     messages.error(
            #         request,
            #         f"Add unit name ({name}) failed, It seems that unit name already exists",
            #     )
            # return redirect(reverse("configurations:add_unit_names"))

            # print('NAME:' , unit_name)
            # msg = f"Unit name ({name}) created successfully."
            # data['error'] = msg
            # data['type'] = 'success'
            # return JsonResponse(data)

        # else:
        # save_form = None
        # messages.error(
        #     request,
        #     "Please fill in the form with valid data.",
        # )
        # form = UnitNamesForm()
    else:
        # unit_name = "None1"
        form = UnitNamesForm()
    # print('UNIT_NAME-FROM-WHERE:::', unit_name)
    table_search = request.GET.get("table_search")
    if table_search == None or table_search == "":
        qs = UnitNames.objects.filter(user=request.user).only()
        # category = Category.objects.values('id', 'name', 'active', 'is_deleted',)
        # qs = Product.objects.only().filter(is_deleted=False).order_by('-created_at')
    elif ("table_search") in request.GET or request.GET["table_search"].strip():
        qs = UnitNames.objects.filter(
            Q(user=request.user, name__icontains=table_search)
        ).only()
    # elif request.GET['table_search'].isnumeric():
    #     qs = Category.objects.filter(
    #         Q(user=request.user, id=table_search)
    #     )
    else:
        qs = UnitNames.objects.filter(Q(user=request.user)).only()
        # category = Category.objects.values('id', 'name', 'active', 'is_deleted',)
        # qs = Product.objects.only().filter(is_deleted=False).order_by('-created_at')

    ## next lines for pagination
    paginator = Paginator(qs, 4)
    page = request.GET.get("page")

    try:
        main_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        main_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        main_page = paginator.page(paginator.num_pages)

    context = {
        "form": form,
        "page": page,
        "main_page": main_page,
        # 'last_unit_name': unit_name, #UnitNames.objects.last(),
        "title": "Create Unit Name",
        # "unit_name_id": unit_name_id,
    }
    return render(request, "configurations/unit_names/add_unit_names.html", context)


# @auth_user_required
@model_id_restriction(app_name="configurations", model_name="UnitNames")
def edit_unit_names(request, id):
    data = {}
    data["unit_name_id"] = id
    data["error"] = "ERROR !!!"
    data["type"] = "error"
    # table_qs = Category.objects.filter(user=request.user)
    # table = CategoryTable(table_qs)
    # table.paginate(page=request.GET.get("page", 1), per_page=25)
    qs = UnitNames.objects.select_related("user").get(id=id)  # get the category name
    print(
        " request.accepts(*/*) ",
        request.accepts("*/*"),
        "request.method******",
        request.method,
    )
    form = UnitNamesForm(request.POST or None, request.FILES or None, instance=qs)

    if request.accepts("*/*") and request.method == "POST":
        unit_name = request.POST.get("name")

        for f in form:
            print(f.name, f.errors)
        if not form.is_valid():
            msg = [
                (key + " Error:", value[0]["message"])
                for key, value in (form.errors.get_json_data().items())
            ]
            data["unit_name_id"] = id
            data["error"] = msg
            data["type"] = "error"
            return JsonResponse(data)

        if form.is_valid():
            save_form = form.save(commit=False)
            save_form.updated_user = request.user
            # save_form.code = 'uom-' + str(id)
            print("EDIT-CODE-----", save_form.code)
            save_form.save()

            error = 'Unit with name "%s" saved successfully' % (unit_name)

            data["unit_name_id"] = id
            data["error"] = error
            data["type"] = "success"
            return JsonResponse(data)

    # else:
    #     form = UnitNamesForm(instance=qs)

    uom_code = "uom-" + str(id)
    context = {
        "form": form,
        "uom_code": uom_code,
        "title": "Edit Unit Name",
        "qs": qs,
    }
    return render(request, "configurations/unit_names/edit_unit_names.html", context)


# def create_ajax_branch_message(request):
#     data = {}
#     data['unit_name_id'] = None
#     data['error'] = 'ERROR !!!'
#     data['type'] = 'error'
#     if request.is_ajax() and request.method == "POST":
#         form = UnitNamesForm(request.POST or None)
#         unit_name = request.POST.get("unit_name")
#         match = UnitNames.objects.select_related('user').filter(name=unit_name).exists()
#         if not match:
#             if form.is_valid():

#                 save_form = form.save(commit=False)
#                 save_form.name = unit_name
#                 save_form.user = request.user
#                 save_form.updated_user = request.user

#                 save_form.save()
#                 error = ('Unit with name "%s" saved successfully' % (unit_name))
#                 data['unit_name_id'] = save_form.id
#                 data['error'] = error
#                 data['type'] = 'success'
#             else:
#                 for f in form:
#                     print('error from is not valid: ', f.name, f.errors)
#                 data['error'] = 'error from is not valid'
#         else:
#             print('name already exists and we must deal with it ...')
#             error = ('Unit with name "%s" already exists !!!' % (unit_name))
#             data['unit_name_id'] = None
#             data['error'] = error
#             data['type'] = 'error'
#     else:
#         form = UnitNamesForm()

#     return JsonResponse(data)


def unit_names_table(request):
    show_log = request.GET.get("show-log")
    show_deleted = request.GET.get("show-deleted")
    in_active = request.GET.get("in-active")
    is_active = request.GET.get("active")
    show_main = request.GET.get("show-main")

    print(
        # 'TYPE****', type,
        "show_log@@@@@@@@@@@",
        show_log,
        "SHOW DELETEDDDDDD",
        show_deleted,
        "INACTIVEEEEE",
        in_active,
        "ACTIVEEEEE",
        is_active,
        "SHOWMAINNNNNN",
        show_main,
    )

    data = {}
    main = []
    log = []

    active = []
    inactive = []
    delete = []
    total_main = 0
    if show_main == "true":

        main = UnitNames.objects.values(
            "id",
            "code",
            "name",
        ).filter(is_deleted=False)

        data["main-list"] = [obj for obj in main]

        print(
            "data['main-list'] ***", data["main-list"], "main.query******>", main.query
        )
        return JsonResponse(data, safe=False)
    elif show_log == "true":
        log_qs = UnitNames.objects.values(
            "id",
            "code",
            "name",
            "user__username",
            "updated_user__username",
            "created_at",
            "updated_at",
            "active",
        ).filter(is_deleted=False)
        log = log_qs
        data["log-list"] = [obj for obj in log]
        print("data['log-list'] ***", data["log-list"], "main.query******>", log.query)
        return JsonResponse(data, safe=False)
    elif in_active == "true":
        inactive = (
            UnitNames.objects.values(
                "id",
                "code",
                "name",
            )
            .filter(active=False, is_deleted=False)
            .order_by("-id")
        )
        # main = []
        data["inactive-list"] = [obj for obj in inactive]
        return JsonResponse(data, safe=False)
    elif is_active == "true":
        active = (
            UnitNames.objects.values(
                "id",
                "code",
                "name",
            )
            .filter(active=True, is_deleted=False)
            .order_by("-id")
        )
        data["active-list"] = [obj for obj in active]
        print(
            "data['active-list'] ***",
            data["active-list"],
            "main.query******>",
            active.query,
        )
        return JsonResponse(data, safe=False)
    elif show_deleted:
        delete = (
            UnitNames.objects.values(
                "id", "code", "name", "updated_user__username", "deleted_at", "active"
            )
            .filter(is_deleted=True)
            .order_by("-id")
        )

        data["delete-list"] = [obj for obj in delete]
        print(
            "data['delete-list'] ***",
            data["delete-list"],
            "delete.query******>",
            delete.query,
        )
        return JsonResponse(data, safe=False)

    # main_qs = UnitNames.objects.select_related('user').only().order_by('-id')
    # table_qs = UnitNames.objects.select_related('user').filter(active=True).order_by('-id')
    # inactive_qs = UnitNames.objects.select_related('user').filter(is_deleted=False, active=False).order_by('-id')
    # deleted_qs = UnitNames.objects.select_related('user').filter(is_deleted=True, active=False).order_by('-id')
    # combined_qs = list(chain(table_qs, inactive_qs))

    # #?Esraa
    # table_total_qs = UnitNames.objects.select_related('user').filter(is_deleted=False).order_by('-id')
    # deleted_total_qs = UnitNames.objects.select_related('user').filter(is_deleted=True).order_by('-id')
    # active_qs = UnitNames.objects.select_related('user').filter(is_deleted=False, active=True).order_by('-id')
    table_total = (
        UnitNames.objects.select_related("user").filter(is_deleted=False).count()
    )
    active_total = (
        UnitNames.objects.select_related("user")
        .filter(is_deleted=False, active=True)
        .count()
    )
    inactive_total = (
        UnitNames.objects.select_related("user")
        .filter(is_deleted=False, active=False)
        .count()
    )
    deleted_total = (
        UnitNames.objects.select_related("user").filter(is_deleted=True).count()
    )
    # next lines for pagination
    # paginator = Paginator(qs, 10)
    # page = request.GET.get("page")

    # try:
    #     main_page = paginator.page(page)
    # except PageNotAnInteger:
    #     # If page is not an integer deliver the first page
    #     main_page = paginator.page(1)
    # except EmptyPage:
    #     # If page is out of range deliver last page of results
    #     main_page = paginator.page(paginator.num_pages)

    context = {
        # "table_qs": table_qs,
        # "page": page,
        # "main_page": main_page,
        "title": "Unit Names",
        # 'main_qs': main_qs,
        # 'inactive_qs': inactive_qs,
        # 'deleted_qs': deleted_qs,
        # 'combined_qs': combined_qs,
        # 'table_total_qs':table_total_qs ,
        # 'deleted_total_qs':deleted_total_qs ,
        # 'active_qs':active_qs,
        "table_total": table_total,
        "active_total": active_total,
        "inactive_total": inactive_total,
        "deleted_total": deleted_total,
    }
    return render(request, "configurations/unit_names/unit_names_table.html", context)
