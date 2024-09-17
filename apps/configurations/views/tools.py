from django.shortcuts import render
from django.http import JsonResponse

from config.choices import CURRENT_STATUS

from ..models import Tools
from ..forms import ToolsForm


def add_tools(request):
    data = {}
    data["tools_id"] = None
    if request.accepts("*/*") and request.method == "POST":
        form = ToolsForm(
            request.POST or None,
        )

        for f in form:
            print(f.name, f.errors)
            if not f.errors:
                print(
                    "No errors, from is valid and : ",
                    request.accepts("*/*"),
                    request.method,
                )

        if not form.is_valid():
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

            Tools.objects.filter(id=save_form.id).update(
                code="tool-" + str(save_form.id)
            )

            msg = 'toolswith id "%s" saved successfully' % (save_form.id)
            data["tools_id"] = save_form.id
            data["error"] = msg
            data["type"] = "success"
            return JsonResponse(data)

    else:
        form = ToolsForm()

    context = {"form": form, "title": "Create Tool"}
    return render(request, "configurations/tools/add_tools.html", context)


def edit_tools(request, id):
    data = {}
    data["tools_id"] = id

    qs = Tools.objects.select_related("user").get(id=id)
    form = ToolsForm(
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
        tools_name = request.POST.get("name")

        if not form.is_valid():
            msg = [
                (key + " Error:", value[0]["message"])
                for key, value in (form.errors.get_json_data().items())
            ]
            data["tools_id"] = id
            data["error"] = msg
            data["type"] = "error"
            return JsonResponse(data)
        if form.is_valid():

            save_form = form.save(commit=False)
            save_form.updated_user = request.user

            save_form.save()
            msg = 'toolswith name "%s" saved successfully' % (tools_name)

            data["tools_id"] = id
            data["error"] = msg
            data["type"] = "success"
            return JsonResponse(data)
        else:
            form = ToolsForm()

    tools_code = "tool-" + str(id)

    context = {"form": form, "qs": qs, "tools_code": tools_code, "title": "Edit tools"}
    return render(request, "configurations/tools/edit_tools.html", context)


def tools_table(request):
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
    current_status = [obj[1] for obj in CURRENT_STATUS]
    data["current_status"] = current_status
    if show_main == "true":
        main = (
            Tools.objects.values(
                "id",
                "code",
                "current_status",
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
            Tools.objects.select_related("user")
            .only()
            .values(
                "id",
                "code",
                "current_status",
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
            Tools.objects.values(
                "id",
                "code",
                "current_status",
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
            Tools.objects.values(
                "id",
                "code",
                "current_status",
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
            Tools.objects.values(
                "id",
                "code",
                "current_status",
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
        Tools.objects.select_related("user")
        .values("id")
        .filter(is_deleted=False, active=False)
        .count()
    )
    deleted_total = (
        Tools.objects.select_related("user")
        .values("id")
        .filter(is_deleted=True)
        .count()
    )
    main_log_total = (
        Tools.objects.select_related("user")
        .values("id")
        .filter(is_deleted=False)
        .count()
    )
    active_total = (
        Tools.objects.select_related("user")
        .values("id")
        .filter(is_deleted=False, active=True)
        .count()
    )
    context = {
        "title": "Tools Table",
        "inactive_total": inactive_total,
        "deleted_total": deleted_total,
        "main_log_total": main_log_total,
        "active_total": active_total,
    }
    return render(request, "configurations/tools/tools_table.html", context)
