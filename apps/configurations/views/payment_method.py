from django.shortcuts import render
from django.http import JsonResponse

from ..models import PaymentMethod
from ..forms import PaymentMethodForm


def add_payment_method(request):
    data = {}
    data["payment_method_id"] = None
    if request.accepts("*/*") and request.method == "POST":
        form = PaymentMethodForm(
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

        payment_method_name = request.POST.get("name")
        print(
            "payment_method_name**",
            payment_method_name,
        )
        if not form.is_valid():
            data["payment_method_id"] = None
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

            PaymentMethod.objects.filter(id=save_form.id).update(
                code="PaymentMethod-" + str(save_form.id)
            )

            msg = 'Payment Method with name "%s" saved successfully' % (
                payment_method_name
            )
            data["payment_method_id"] = save_form.id
            data["payment_method_name"] = save_form.name
            data["error"] = msg
            data["type"] = "success"
            return JsonResponse(data)

    else:
        form = PaymentMethodForm()

    context = {"form": form, "title": "Create Payment Method"}
    return render(
        request, "configurations/payment_method/add_payment_method.html", context
    )


def edit_payment_method(request, id):
    data = {}
    data["payment_method_id"] = id

    qs = PaymentMethod.objects.select_related("user").get(id=id)
    form = PaymentMethodForm(
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
        payment_method_name = request.POST.get("name")

        if not form.is_valid():
            msg = [
                (key + " Error:", value[0]["message"])
                for key, value in (form.errors.get_json_data().items())
            ]
            data["payment_method_id"] = id
            data["error"] = msg
            data["type"] = "error"
            return JsonResponse(data)
        if form.is_valid():

            save_form = form.save(commit=False)
            save_form.updated_user = request.user

            save_form.save()
            msg = 'Payment Method with name "%s" saved successfully' % (
                payment_method_name
            )

            data["payment_method_id"] = id
            data["error"] = msg
            data["type"] = "success"
            return JsonResponse(data)
        else:
            form = PaymentMethodForm()

    payment_method_code = "PaymentMethod-" + str(id)

    context = {
        "form": form,
        "qs": qs,
        "payment_method_code": payment_method_code,
        "title": "Edit payment_method",
    }
    return render(
        request, "configurations/payment_method/edit_payment_method.html", context
    )


def create_ajax_payment_method_message(request):
    data = {}
    data["payment_method_id"] = None
    data["error"] = "ERROR !!!"
    data["type"] = "error"
    if request.is_ajax() and request.method == "POST":
        form = PaymentMethodForm(request.POST or None)
        payment_method_name = request.POST.get("payment_method_name")
        match = (
            PaymentMethod.objects.select_related("user")
            .filter(name=payment_method_name)
            .exists()
        )
        if not match:
            if form.is_valid():

                save_form = form.save(commit=False)
                save_form.name = payment_method_name
                save_form.user = request.user
                save_form.updated_user = request.user

                save_form.save()
                msg = 'Payment Method with name "%s" saved successfully' % (
                    payment_method_name
                )
                data["payment_method_id"] = save_form.id
                data["error"] = msg
                data["type"] = "success"
            else:
                for f in form:
                    print("error from is not valid: ", f.name, f.errors)
                data["error"] = "error from is not valid"
        else:
            print("name already exists and we must deal with it ...")
            error = 'Payment Method with name "%s" already exists !!!' % (
                payment_method_name
            )
            data["payment_method_id"] = None
            data["error"] = error
            data["type"] = "error"
    else:
        form = PaymentMethodForm()

    return JsonResponse(data)


def payment_method_table(request):
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
            PaymentMethod.objects.values(
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
            PaymentMethod.objects.select_related("user")
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
            PaymentMethod.objects.values(
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
            PaymentMethod.objects.values(
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
            PaymentMethod.objects.values(
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
        PaymentMethod.objects.select_related("user")
        .values("id")
        .filter(is_deleted=False, active=False)
        .count()
    )
    deleted_total = (
        PaymentMethod.objects.select_related("user")
        .values("id")
        .filter(is_deleted=True)
        .count()
    )
    main_log_total = (
        PaymentMethod.objects.select_related("user")
        .values("id")
        .filter(is_deleted=False)
        .count()
    )
    active_total = (
        PaymentMethod.objects.select_related("user")
        .values("id")
        .filter(is_deleted=False, active=True)
        .count()
    )
    context = {
        "title": "Payment Methods",
        "inactive_total": inactive_total,
        "deleted_total": deleted_total,
        "main_log_total": main_log_total,
        "active_total": active_total,
    }
    return render(
        request, "configurations/payment_method/payment_method_table.html", context
    )
