from django.shortcuts import render
from django.http import JsonResponse

from config.choices import CURRENT_STATUS

from ..models import Equipments
from ..forms import EquipmentsForm


def add_equipments(request):
    data = {}
    data["equipments_id"] = None
    if request.accepts("*/*") and request.method == "POST":
        form = EquipmentsForm(
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

            Equipments.objects.filter(id=save_form.id).update(
                code="equip-" + str(save_form.id)
            )

            msg = 'Equipment with id "%s" saved successfully' % (save_form.id)
            data["equipments_id"] = save_form.id
            data["error"] = msg
            data["type"] = "success"
            return JsonResponse(data)

    else:
        form = EquipmentsForm()

    context = {"form": form, "title": "Create Equipments"}
    return render(request, "configurations/equipments/add_equipments.html", context)


def edit_equipments(request, id):
    data = {}
    data["equipments_id"] = id

    qs = Equipments.objects.select_related("user").get(id=id)
    form = EquipmentsForm(
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
        equipments_name = request.POST.get("name")

        if not form.is_valid():
            msg = [
                (key + " Error:", value[0]["message"])
                for key, value in (form.errors.get_json_data().items())
            ]
            data["equipments_id"] = id
            data["error"] = msg
            data["type"] = "error"
            return JsonResponse(data)
        if form.is_valid():

            save_form = form.save(commit=False)
            save_form.updated_user = request.user

            save_form.save()
            msg = 'Equipment with name "%s" saved successfully' % (equipments_name)

            data["equipments_id"] = id
            data["error"] = msg
            data["type"] = "success"
            return JsonResponse(data)
        else:
            form = EquipmentsForm()

    equipments_code = "equip-" + str(id)

    context = {
        "form": form,
        "qs": qs,
        "equipments_code": equipments_code,
        "title": "Edit Equipments",
    }
    return render(request, "configurations/equipments/edit_equipments.html", context)


def create_ajax_equipments_message(request):
    data = {}
    data["equipments_id"] = None
    data["error"] = "ERROR !!!"
    data["type"] = "error"
    if request.is_ajax() and request.method == "POST":
        form = EquipmentsForm(request.POST or None)
        equipments_name = request.POST.get("equipments_name")
        match = (
            Equipments.objects.select_related("user")
            .filter(name=equipments_name)
            .exists()
        )
        if not match:
            if form.is_valid():

                save_form = form.save(commit=False)
                save_form.name = equipments_name
                save_form.user = request.user
                save_form.updated_user = request.user

                save_form.save()
                msg = 'Work Type with name "%s" saved successfully' % (equipments_name)
                data["equipments_id"] = save_form.id
                data["error"] = msg
                data["type"] = "success"
            else:
                for f in form:
                    print("error from is not valid: ", f.name, f.errors)
                data["error"] = "error from is not valid"
        else:
            print("name already exists and we must deal with it ...")
            error = 'equipments with name "%s" already exists !!!' % (equipments_name)
            data["equipments_id"] = None
            data["error"] = error
            data["type"] = "error"
    else:
        form = EquipmentsForm()

    return JsonResponse(data)


def equipments_table(request):
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
            Equipments.objects.values(
                "id",
                "code",
                "equip_type",
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
            Equipments.objects.select_related("user")
            .only()
            .values(
                "id",
                "code",
                "equip_type",
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
            Equipments.objects.values(
                "id",
                "code",
                "equip_type",
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
            Equipments.objects.values(
                "id",
                "code",
                "equip_type",
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
            Equipments.objects.values(
                "id",
                "code",
                "equip_type",
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
        Equipments.objects.select_related("user")
        .values("id")
        .filter(is_deleted=False, active=False)
        .count()
    )
    deleted_total = (
        Equipments.objects.select_related("user")
        .values("id")
        .filter(is_deleted=True)
        .count()
    )
    main_log_total = (
        Equipments.objects.select_related("user")
        .values("id")
        .filter(is_deleted=False)
        .count()
    )
    active_total = (
        Equipments.objects.select_related("user")
        .values("id")
        .filter(is_deleted=False, active=True)
        .count()
    )
    context = {
        "title": "Equipments Table",
        "inactive_total": inactive_total,
        "deleted_total": deleted_total,
        "main_log_total": main_log_total,
        "active_total": active_total,
    }
    return render(request, "configurations/equipments/equipments_table.html", context)
