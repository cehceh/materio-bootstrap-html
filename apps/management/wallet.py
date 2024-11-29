from django.shortcuts import render
from django.http import JsonResponse
from itertools import chain

from .models import CreateWallet
from .forms import CreateWalletForm
from config.utils import model_id_restriction


def add_wallet(request):
    data = {}
    data["wallet_id"] = None
    data["msg"] = "ERROR !!!"
    data["type"] = "error"
    if request.accepts("*/*") and request.method == "POST":
        form = CreateWalletForm(
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

        wallet_name = request.POST.get("name")
        wallet_new_name = request.POST.get("wallet_name")
        wallet_type = request.POST.get("wallet_type")
        mobile = request.POST.get("mobile")
        account_name = request.POST.get("account_name")

        print("wallet_name", wallet_name)
        print("wallet_new_name", wallet_new_name)
        if wallet_name == "0" and (wallet_new_name == "0" or wallet_new_name == ""):
            data["msg"] = (
                "Please Choose From the Wallet Name or From the Wallet New Name"
            )
            data["type"] = "error"
            return JsonResponse(data)

        if wallet_type == "" or wallet_type == None or wallet_type == "0":
            data["msg"] = "Please select a wallet type"
            data["type"] = "error"
            return JsonResponse(data)

        if wallet_type == 2:
            # Wallet names 4 or 5 require an account name, and mobile validation is not needed
            if account_name == "" or account_name == None:
                data["msg"] = "Please enter an account name"
                data["type"] = "error"
                return JsonResponse(data)
        elif wallet_type == "1":
            # Wallet name 1 requires the mobile number to start with "010"
            if not mobile:
                data["msg"] = "Please enter a mobile number"
                data["type"] = "error"
                return JsonResponse(data)
            # # Wallet name 2 requires the mobile number to start with "011"
            # if not mobile.startswith("011"):
            #     data['msg'] = "Mobile number for Wallet Etisalat should start with '011'"
            #     data['type'] = "error"
            #     return JsonResponse(data)
            # # Wallet name 3 requires the mobile number to start with "012"
            # if not mobile.startswith("015"):
            #     data['msg'] = "Mobile number for Wallet We should start with '015'"
            #     data['type'] = "error"
            #     return JsonResponse(data)
            # # Wallet name 3 requires the mobile number to start with "012"
            # if not mobile.startswith("012"):
            #     data['msg'] = "Mobile number for Wallet Orange should start with '012'"
            #     data['type'] = "error"
            #     return JsonResponse(data)

        if (account_name == "" and mobile == "0") or (
            account_name == "" and mobile == ""
        ):
            data["msg"] = "Please enter either an account name or a mobile number"
            data["type"] = "error"
            return JsonResponse(data)

        if mobile and len(str(mobile)) != 11:
            data["msg"] = "Please enter a valid mobile number"
            data["type"] = "error"
            return JsonResponse(data)

        if CreateWallet.objects.filter(mobile=mobile, user=request.user).exists():
            data["msg"] = "Wallet with this Mobile number  already exists."
            data["type"] = "error"
            return JsonResponse(data)

        # if CreateWallet.objects.filter(account_name=account_name, user=request.user).exists():
        #     data['msg'] = "Wallet with this name already exists."
        #     data['type'] = "error"
        #     return JsonResponse(data)
        # if account_name == '':
        #     data['msg'] = "Please enter a account  name"
        #     data['type'] = "error"
        #     return JsonResponse(data)

        # if balance == '' or balance == '0' or balance == None:
        #     data['msg'] = "Please enter a balance"
        #     data['type'] = "error"
        #     return JsonResponse(data)

        if not form.is_valid():
            data["wallet_id"] = None
            msg = [
                (key + " Error:", value[0]["message"])
                for key, value in (form.errors.get_json_data().items())
            ]
            data["msg"] = msg
            data["type"] = "error"
            return JsonResponse(data)

        if form.is_valid():
            save_form = form.save(commit=False)
            # save_form.full_name = full_name
            save_form.user = request.user
            save_form.updated_user = request.user
            save_form.active = True
            save_form.save()

            CreateWallet.objects.filter(id=save_form.id).update(
                code="wal-" + str(save_form.id)
            )

            msg = "Wallet  saved successfully"
            data["wallet_id"] = save_form.id
            data["wallet_name"] = save_form.name
            data["msg"] = msg
            data["type"] = "success"
            return JsonResponse(data)

    else:
        form = CreateWalletForm()

    context = {"form": form, "title": "Create Wallet"}
    return render(request, "management/create_wallet/add_wallet.html", context)


@model_id_restriction(app_name="management", model_name="CreateWallet")
def edit_wallet(request, id):
    data = {}
    data["wallet_id"] = id
    data["msg"] = "ERROR !!!"
    data["type"] = "error"

    qs = CreateWallet.objects.select_related("user").get(id=id)
    form = CreateWalletForm(
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

        wallet_name = request.POST.get("name")
        # wallet_name = request.POST.get("name")
        mobile = request.POST.get("mobile")
        account_name = request.POST.get("account_name")

        if wallet_name == "" or wallet_name == None or wallet_name == "0":
            data["msg"] = "Please select a wallet  name"
            data["type"] = "error"
            return JsonResponse(data)

        if wallet_name in ["4", "5"]:
            # Wallet names 4 or 5 require an account name, and mobile validation is not needed
            if account_name == "" or account_name == None:
                data["msg"] = (
                    "Please enter an account name for Wallets Instapay or Paymob"
                )
                data["type"] = "error"
                return JsonResponse(data)
        elif wallet_name == "1":
            # Wallet name 1 requires the mobile number to start with "010"
            if not mobile.startswith("010"):
                data["msg"] = (
                    "Mobile number for Wallet Vodafone should start with '010'"
                )
                data["type"] = "error"
                return JsonResponse(data)
        elif wallet_name == "2":
            # Wallet name 2 requires the mobile number to start with "011"
            if not mobile.startswith("011"):
                data["msg"] = (
                    "Mobile number for Wallet Etisalat should start with '011'"
                )
                data["type"] = "error"
                return JsonResponse(data)
        elif wallet_name == "3":
            # Wallet name 3 requires the mobile number to start with "012"
            if not mobile.startswith("015"):
                data["msg"] = "Mobile number for Wallet We should start with '015'"
                data["type"] = "error"
                return JsonResponse(data)
        elif wallet_name == "6":
            # Wallet name 3 requires the mobile number to start with "012"
            if not mobile.startswith("012"):
                data["msg"] = "Mobile number for Wallet Orange should start with '012'"
                data["type"] = "error"
                return JsonResponse(data)

        if (account_name == "" and mobile == "0") or (
            account_name == "" and mobile == ""
        ):
            data["msg"] = "Please enter either an account name or a mobile number"
            data["type"] = "error"
            return JsonResponse(data)

        if mobile and len(str(mobile)) != 11:
            data["msg"] = "Please enter a valid mobile number"
            data["type"] = "error"
            return JsonResponse(data)

        # if CreateWallet.objects.filter(mobile=mobile, user=request.user).exists():
        #     data['msg'] = "Wallet with this Mobile number  already exists."
        #     data['type'] = "error"
        #     return JsonResponse(data)

        # if CreateWallet.objects.filter(account_name=account_name, user=request.user).exists():
        #     data['msg'] = "Wallet with this name already exists."
        #     data['type'] = "error"
        #     return JsonResponse(data)

        if not form.is_valid():
            msg = [
                (key + " Error:", value[0]["message"])
                for key, value in (form.errors.get_json_data().items())
            ]
            data["wallet_id"] = id
            data["msg"] = msg
            data["type"] = "error"
            return JsonResponse(data)

        if form.is_valid():

            save_form = form.save(commit=False)
            # save_form.full_name = full_name
            save_form.updated_user = request.user

            save_form.save()
            error = 'Wallet with name "%s" saved successfully' % (wallet_name)

            data["wallet_id"] = id
            data["msg"] = error
            data["type"] = "success"
            return JsonResponse(data)
        else:
            form = CreateWalletForm()

    wallet_code = "wal-" + str(id)
    context = {
        "form": form,
        "qs": qs,
        "wallet_code": wallet_code,
        "title": "Edit Wallet",
    }
    return render(request, "management/create_wallet/edit_wallet.html", context)


def wallet_table(request):
    table_qs = (
        CreateWallet.objects.select_related("user")
        .filter(is_deleted=False, active=True)
        .order_by("-id")
    )
    mobile_qs = (
        CreateWallet.objects.values()
        .filter(is_deleted=False)
        .exclude(mobile="")
        .exclude(mobile=None)
        .order_by("-id")
    )
    account_qs = (
        CreateWallet.objects.values()
        .filter(is_deleted=False)
        .exclude(account_name="")
        .exclude(account_name=None)
        .order_by("-id")
    )
    inactive_qs = (
        CreateWallet.objects.select_related("user")
        .filter(is_deleted=False, active=False)
        .order_by("-id")
    )
    deleted_qs = (
        CreateWallet.objects.select_related("user")
        .filter(
            is_deleted=True,
        )
        .order_by("-id")
    )
    main_qs = (
        CreateWallet.objects.select_related("user").only().filter().order_by("-id")
    )
    combined_qs = list(chain(table_qs, inactive_qs))

    table_total = table_qs.count()
    mobile_total = mobile_qs.count()
    account_total = account_qs.count()
    inactive_total = inactive_qs.count()
    deleted_total = deleted_qs.count()
    main_total = main_qs.count()
    context = {
        "table_qs": table_qs,
        "mobile_qs": mobile_qs,
        "account_qs": account_qs,
        "inactive_qs": inactive_qs,
        "deleted_qs": deleted_qs,
        "combined_qs": combined_qs,
        "main_qs": main_qs,
        "table_total": table_total,
        "mobile_total": mobile_total,
        "account_total": account_total,
        "inactive_total": inactive_total,
        "deleted_total": deleted_total,
        "main_total": main_total,
        "title": " Wallet",
    }
    return render(request, "management/create_wallet/wallet_table.html", context)


# def create_ajax_wallet_message(request):
#     data = {}
#     data['wallet_id'] = None
#     data['msg'] = 'ERROR !!!'
#     data['type'] = 'error'
#     if request.is_ajax() and request.method == "POST":
#         form = CreateWalletForm(request.POST or None)
#         mobile = request.POST.get("mobile")
#         match = CreateWallet.objects.select_related('user').filter(mobile=mobile).exists()
#         if not match:
#             if form.is_valid():

#                 save_form = form.save(commit=False)
#                 save_form.name = mobile
#                 save_form.user = request.user
#                 save_form.updated_user = request.user

#                 save_form.save()
#                 error = ('Wallet with name "%s" saved successfully' % (mobile))
#                 data['wallet_id'] = save_form.id
#                 data['msg'] = error
#                 data['type'] = 'success'
#             else:
#                 for f in form:
#                     print('error from is not valid: ', f.name, f.errors)
#                 data['error'] = 'error from is not valid'
#         else:
#             print('name already exists and we must deal with it ...')
#             error = ('Wallet with number "%s" already exists !!!' % (mobile))
#             data['wallet_id'] = None
#             data['msg'] = error
#             data['type'] = 'error'
#     else:
#         form = CreateWalletForm()

#     return JsonResponse(data)
