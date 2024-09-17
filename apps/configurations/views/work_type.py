from django.shortcuts import render
from django.http import JsonResponse

from ..models import WorkType
from ..forms import WorkTypeForm


def add_work_type(request):
    data = {}
    data["work_type_id"] = None
    if request.accepts("*/*") and request.method == "POST":
        form = WorkTypeForm(
            request.POST or None,
        )
        active = request.POST.get("active")

        print("ACTIVE@@@************", active)

        for f in form:
            print(f.name, f.errors)
            if not f.errors:
                print(
                    "No errors, from is valid and : ",
                    request.accepts("*/*"),
                    request.method,
                )

        work_type_name = request.POST.get("name")
        print(
            "work_type_name**",
            work_type_name,
        )
        if not form.is_valid():
            data["work_type_id"] = None
            msg = [
                (key + " Error:", value[0]["message"])
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

            WorkType.objects.filter(id=save_form.id).update(
                code="worktype-" + str(save_form.id)
            )

            msg = 'Work Type with name "%s" saved successfully' % (work_type_name)
            data["work_type_id"] = save_form.id
            data["work_type_name"] = save_form.name
            data["error"] = msg
            data["type"] = "success"
            return JsonResponse(data)

    else:
        form = WorkTypeForm()

    context = {"form": form, "title": "Create Work Type"}
    return render(request, "configurations/work_type/add_work_type.html", context)


def edit_work_type(request, id):
    data = {}
    data["work_type_id"] = id

    qs = WorkType.objects.select_related("user").get(id=id)
    form = WorkTypeForm(
        request.POST or None,
        request.FILES or None,
        instance=qs,
    )

    for f in form:
        print(f.name, f.errors)
        if not f.errors:
            print(
                "No errors, from is valid and : ",
                request.accepts("*/*"),
                request.method,
            )

    if request.accepts("*/*") and request.method == "POST":
        work_type_name = request.POST.get("name")

        if not form.is_valid():
            msg = [
                (key + " Error:", value[0]["message"])
                for key, value in (form.errors.get_json_data().items())
            ]
            data["work_type_id"] = id
            data["error"] = msg
            data["type"] = "error"
            return JsonResponse(data)
        if form.is_valid():

            save_form = form.save(commit=False)
            save_form.updated_user = request.user

            save_form.save()
            msg = 'Work Type with name "%s" saved successfully' % (work_type_name)

            data["work_type_id"] = id
            data["error"] = msg
            data["type"] = "success"
            return JsonResponse(data)
        else:
            form = WorkTypeForm()

    work_type_code = "worktype-" + str(id)

    context = {
        "form": form,
        "qs": qs,
        "work_type_code": work_type_code,
        "title": "Edit work_type",
    }
    return render(request, "configurations/work_type/edit_work_type.html", context)


def create_ajax_work_type_message(request):
    data = {}
    data["work_type_id"] = None
    data["error"] = "ERROR !!!"
    data["type"] = "error"
    if request.is_ajax() and request.method == "POST":
        form = WorkTypeForm(request.POST or None)
        work_type_name = request.POST.get("work_type_name")
        match = (
            WorkType.objects.select_related("user").filter(name=work_type_name).exists()
        )
        if not match:
            if form.is_valid():

                save_form = form.save(commit=False)
                save_form.name = work_type_name
                save_form.user = request.user
                save_form.updated_user = request.user

                save_form.save()
                msg = 'Work Type with name "%s" saved successfully' % (work_type_name)
                data["work_type_id"] = save_form.id
                data["error"] = msg
                data["type"] = "success"
            else:
                for f in form:
                    print("error from is not valid: ", f.name, f.errors)
                data["error"] = "error from is not valid"
        else:
            print("name already exists and we must deal with it ...")
            error = 'work_type with name "%s" already exists !!!' % (work_type_name)
            data["work_type_id"] = None
            data["error"] = error
            data["type"] = "error"
    else:
        form = WorkTypeForm()

    return JsonResponse(data)


def work_type_table(request):
    show_log = request.GET.get("show-log")
    show_deleted = request.GET.get("show-deleted")
    in_active = request.GET.get("in-active")
    is_active = request.GET.get("is-active")
    show_main = request.GET.get("show-main")
    print(
        "show_log===",
        show_log,
        "show_deleted===",
        show_deleted,
        "in_active===",
        in_active,
        "active===",
        is_active,
        "show_main===",
        show_main,
    )
    data = {}
    main = []
    log = []
    active = []
    inactive = []
    delete = []
    if show_main == "true":
        main = (
            WorkType.objects.values(
                "id",
                "code",
                "name",
            )
            .filter(is_deleted=False)
            .order_by("-id")
        )

        data["main-list"] = [obj for obj in main]

        print(
            "data['main-list'] ***", data["main-list"], "main.query******>", main.query
        )
        return JsonResponse(data, safe=False)
    elif show_log == "true":
        log = (
            WorkType.objects.select_related("user")
            .only()
            .values(
                "id",
                "code",
                "name",
                "created_at",
                "updated_at",
                "updated_user__username",
                "user__username",
            )
            .filter(is_deleted=False)
            .order_by("-id")
        )

        # inactive = []
        data["log-list"] = [obj for obj in log]
        print("data['log-list'] ***", data["log-list"], "log.query******>", log.query)
        return JsonResponse(data, safe=False)
    elif in_active == "true":
        inactive = (
            WorkType.objects.values(
                "id",
                "code",
                "name",
            )
            .filter(is_deleted=False, active=False)
            .order_by("-id")
        )

        data["inactive-list"] = [obj for obj in inactive]
        print(
            "data['inactive-list'] ***",
            data["inactive-list"],
            "inactive.query******>",
            inactive.query,
        )
        return JsonResponse(data, safe=False)
    elif is_active == "true":
        active = (
            WorkType.objects.values(
                "id",
                "code",
                "name",
            )
            .filter(is_deleted=False, active=True)
            .order_by("-id")
        )

        data["active-list"] = [obj for obj in active]
        print(
            "data['active-list'] ***",
            data["active-list"],
            "active.query******>",
            active.query,
        )
        return JsonResponse(data, safe=False)
    elif show_deleted == "true":
        delete = (
            WorkType.objects.values(
                "id",
                "code",
                "name",
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

    inactive_total = (
        WorkType.objects.select_related("user")
        .values("id")
        .filter(is_deleted=False, active=False)
        .count()
    )
    deleted_total = (
        WorkType.objects.select_related("user")
        .values("id")
        .filter(is_deleted=True)
        .count()
    )
    main_log_total = (
        WorkType.objects.select_related("user")
        .values("id")
        .filter(is_deleted=False)
        .count()
    )
    active_total = (
        WorkType.objects.select_related("user")
        .values("id")
        .filter(is_deleted=False, active=True)
        .count()
    )
    context = {
        "title": "Work Types",
        "inactive_total": inactive_total,
        "deleted_total": deleted_total,
        "main_log_total": main_log_total,
        "active_total": active_total,
    }
    return render(request, "configurations/work_type/work_type_table.html", context)
