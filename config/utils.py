from django.apps import apps
from django.core import exceptions
import datetime
from django.db import models
import os
import re
import uuid
import random
import string
from django.contrib.auth import logout

# from django.contrib.admin.views.decorators import staff_member_required

from django.core.exceptions import PermissionDenied

from django.contrib import messages
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django.shortcuts import redirect, render

# from apps.vendors.models import Vendor


def get_last_month_data(today):
    """
    Simple method to get the datetime objects for the
    start and end of last month.
    """
    this_month_start = datetime.datetime(today.year, today.month, 1)
    last_month_end = this_month_start - datetime.timedelta(days=1)
    last_month_start = datetime.datetime(last_month_end.year, last_month_end.month, 1)
    return (last_month_start, last_month_end)


def get_month_data_range(months_ago=1, include_this_month=False):
    """
    A method that generates a list of dictionaries
    that describe any given amount of monthly data.
    """
    today = datetime.datetime.now().today()
    dates_ = []
    if include_this_month:
        # get next month's data with:
        next_month = today.replace(day=28) + datetime.timedelta(days=4)
        # use next month's data to get this month's data breakdown
        start, end = get_last_month_data(next_month)
        dates_.insert(
            0,
            {
                "start": start.timestamp(),
                "end": end.timestamp(),
                "start_json": start.isoformat(),
                "end": end.timestamp(),
                "end_json": end.isoformat(),
                "timesince": 0,
                "year": start.year,
                "month": str(start.strftime("%B")),
            },
        )
    for x in range(0, months_ago):
        start, end = get_last_month_data(today)
        today = start
        dates_.insert(
            0,
            {
                "start": start.timestamp(),
                "start_json": start.isoformat(),
                "end": end.timestamp(),
                "end_json": end.isoformat(),
                "timesince": int((datetime.datetime.now() - end).total_seconds()),
                "year": start.year,
                "month": str(start.strftime("%B")),
            },
        )
    # dates_.reverse()
    return dates_


def get_filename(path):  # /abc/filename.mp4
    return os.path.basename(path)


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def unique_key_generator(instance):
    """
    This is for a Django project with an key field
    """
    size = random.randint(30, 45)
    key = random_string_generator(size=size)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(key=key).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return key


def unique_order_id_generator(instance):
    """
    This is for a Django project with an order_id field
    """
    order_new_id = random_string_generator()

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(order_id=order_new_id).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return order_new_id


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug, randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


################################
# from functools import wraps

# def require_post_params(params):
#     def decorator(func):
#         @wraps(func, assigned=available_attrs(func))
#         def inner(request, *args, **kwargs):
#             if not all(param in request.POST for param in params):
#                 return HttpResponseBadRequest()
#             return func(request, *args, **kwargs)
#         return inner
#     return decorator


#################
@classmethod
def model_field_exists(cls, field):
    try:
        cls._meta.get_field(field)
        return True
    except exceptions.FieldDoesNotExist:
        return False


models.Model.field_exists = model_field_exists


def pass_query(
    request,
    *args,
    template_path,
    context,
    app_name,
    model_name,
    param=None,
    exclude=None,
    **kwargs
):

    cls = apps.get_model(app_name, model_name)
    qs = []
    # qs = cls.objects.only().filter(**param).exclude(**exclude).order_by('-id')
    # qs = cls.objects.only().filter(**param).order_by('-id')
    # print(exclude)
    return render(
        request,
        template_path,
        context=(
            {
                "qs": qs,
            }
            | context
        ),
    )


def adding(
    request,
    form_class,
    app_name,
    model_name,
    url=None,
    template_path="",
    related_field=None,
    user=None,
    field_1=None,
    field_2=None,
    field_3=None,
    context={},
):

    if request.method == "POST":
        form = form_class(
            request.POST or None,
            request.FILES or None,
            user=user,
            f1=field_1,
            f2=field_2,
        )

        # request.FILES or None ,
        # print(form.is_valid(), form.cleaned_data['quantity'])
        # for field in form: #* for debugging
        #     print("Field Error:", field.name,  field.errors, form.is_valid())
        if form.is_valid():
            save_form = form.save(commit=False)
            cls = apps.get_model(app_name, model_name)

            if cls.field_exists("updated_user"):
                save_form.updated_user = request.user
                # print('User exists  ==>> ', cls.field_exists('user'))
                save_form.save()
            else:
                # user=None
                print("Updated user does not exist <<==>> ")

            messages.success(
                request, "Adding new (" + str(model_name) + ") done successfully"
            )  #
            # return redirect(reverse(url, args=(save_form.id,)))
        else:
            messages.error(request, "Add new (" + str(model_name) + ") failed ")
            return redirect(request.META.get("HTTP_REFERER", ""))
    else:
        form = form_class(user=user, f1=field_1, f2=field_2)

    return render(
        request,
        template_path,
        context=(
            {
                "form": form,
            }
            | context
        ),
    )


def editing(
    request,
    id_field,
    form_class,
    app_name,
    model_name,
    url=None,
    template_path=None,
    related_field=None,
    user=None,
    field_1=None,
    field_2=None,
    field_3=None,
    context={},
):

    cls = apps.get_model(app_name, model_name)
    qs = cls.objects.select_related(related_field).get(id=id_field)
    if cls.field_exists("user"):
        user = qs.user
        # print('User exists  ==>> ', cls.field_exists('user'))
    else:
        user = None
        # print('User not exists ==>> ', cls.field_exists('user'))

    form = form_class(
        request.POST or None,
        request.FILES or None,
        user=user,
        f1=field_1,
        f2=field_2,
        instance=qs,
    )
    # print('ERRORS when NONE:: ', form.errors)
    if form.is_valid():
        save_form = form.save(commit=False)
        save_form.save()
        messages.success(
            request, "Save changes to (" + str(model_name) + ") done successfully"
        )
        return redirect(reverse(url, args=(save_form.id,)))
    # else:
    #     for field in form: #* for debugging
    #         print("Field Error:", field.name,  field.errors, field.value)
    #     print(form.is_valid(), ' SOMETHING went wrong .... ', form)
    return render(
        request,
        template_path,
        context=(
            {
                "form": form,
            }
            | context
        ),
    )


def switch_active(request, *args, id, app_name, model_name, **kwargs):

    url = request.META.get("HTTP_REFERER", "")
    next_url = redirect(url)
    data = {}

    cls = apps.get_model(app_name, model_name)

    if cls.field_exists("is_active"):
        qs = cls.objects.only()
        check = qs.filter(id=id).exists()
        if check:
            obj = qs.get(id=id)
        else:
            obj = []

        if obj.is_active:
            cls.objects.values(
                "is_active",
            ).filter(
                id=id
            ).update(is_active=False)
        else:
            cls.objects.values(
                "is_active",
            ).filter(
                id=id
            ).update(is_active=True)
    else:
        qs = cls.objects.only(
            "active",
        )
        check = qs.filter(id=id).exists()
        if check:
            obj = qs.get(id=id)
        else:
            obj = []

        if obj.active:
            cls.objects.values(
                "active",
            ).filter(
                id=id
            ).update(active=False)
            # data['url'] = next_url
            # kwargs['id'] = id
            # kwargs['app_name'] = app_name
            # kwargs['model_name'] = model_name
            # kwargs['k_url'] = url
            # data['msg'] = 'Item Disabled successfuly ...'
            # data['type'] = 'info'
            # return JsonResponse(data|kwargs)
        else:
            cls.objects.values(
                "active",
            ).filter(
                id=id
            ).update(active=True)

            # kwargs['id'] = id
            # kwargs['app_name'] = app_name
            # kwargs['model_name'] = model_name
            # kwargs['k_url'] = url
            # data['url'] = url #'/products/table/of/all/products/'
            # data['msg'] = 'Item Activated successfuly ...'
            # data['type'] = 'info'
            # print(
            #     'KAWARGS:::', kwargs,
            #     'kwargs.get(id)***', kwargs.get('id'),# kwargs['id'],
            # )
            # return JsonResponse(data|kwargs)

    return next_url
    # return render(request, 'products/products_table.html', kwargs)


def switch_offer(request, id, app_name, model):
    cls = apps.get_model(app_name, model)
    qs = cls.objects.values(
        "offer",
    ).get(id=id)
    url = request.META.get("HTTP_REFERER", "")
    next_url = redirect(url)
    if qs:
        if qs["offer"]:
            cls.objects.values(
                "offer",
            ).filter(
                id=id
            ).update(offer=False)
        else:
            cls.objects.values(
                "offer",
            ).filter(
                id=id
            ).update(offer=True)

    return next_url


def switch_delete(request, id, app_name, model):
    cls = apps.get_model(app_name, model)
    qs = cls.objects.values(
        "is_deleted",
    ).get(id=id)
    url = request.META.get("HTTP_REFERER", "")
    next_url = redirect(url)

    if qs["is_deleted"]:
        cls.objects.values(
            "is_deleted",
        ).filter(
            id=id
        ).update(is_deleted=False)
    else:
        cls.objects.values(
            "is_deleted",
        ).filter(
            id=id
        ).update(is_deleted=True, deleted_at=timezone.now())

    return next_url


def auth_required(function):
    def wrap(request, *args, **kwargs):
        # joins elements of getnode() after each 2 digits.
        # using regex expression
        label = os.environ.get("SERIAL")
        # print (label)
        mac = ":".join(re.findall("..", "%012x" % uuid.getnode()))
        # print (mac)
        if mac == label:
            # messages.success(request, 'you are authorized')
            return function(request, *args, **kwargs)
        else:
            # messages.success(request, 'you are not authorized')
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


# Check if client or auth_user login
def auth_user_required(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_staff:
            # messages.success(request, 'you are authorized')
            return function(request, *args, **kwargs)
        else:
            # messages.success(request, 'you are not authorized')
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


# Prevent user from changing the user id in this url(localhost:8000/accounts/profile/<user_id>/)
def prevent_changing_id(function):
    def wrap(request, *args, **kwargs):
        from apps.users.models import UserProfile

        # if request.LANGUAGE_CODE == 'en-us':
        #     lang = 'en'
        # else:
        #     lang = (request.LANGUAGE_CODE)
        # print(lang)
        user = request.user
        user_id = request.user.id
        match = UserProfile.objects.filter(user_id=user_id).exists()
        if match:
            uuid = UserProfile.objects.get(user_id=user_id)
            url_path = (
                "/users/profile/user/id/"
                + str(user_id)
                + "/unique/id/"
                + str(uuid.profile_uuid)
                + "/"
            )
        else:
            uuid = None
            url_path = (
                "/users/profile/user/id/" + str(user_id) + "/"
            )  # +'/unique/id/'+ str(uuid.profile_uuid) +'/'

        # url_path = ''  #'/'+ lang +'/users/profile/user/id/'+ str(user_id) +'/unique/id/'+ str(uuid.profile_uuid) +'/'
        # print(request.path, url_path)
        if user_id is not None:
            if request.path != url_path:
                # print(url_path)
                from django.http import HttpResponseRedirect

                return HttpResponseRedirect(url_path)
            else:
                return function(request, *args, **kwargs)

        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def admin_only(function):
    def wrap(request, *args, **kwargs):
        # user = request.user
        if request.user.is_authenticated:
            if request.user.role == "client":
                logout(request)
                return redirect("error_page")
            elif request.user.role == "employee":
                return redirect("error_page")
            elif request.user.role == "admin" or request.user.role == "owner":
                return function(request, *args, **kwargs)
        else:
            return redirect("/accounts/login/")

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


# def changing_url_to_en(function):
#     def wrap(request, *args, **kwargs):
#         lang = (request.LANGUAGE_CODE)
#         print(lang)
#         if lang == 'en-us'
#             lang = 'en'
#             return function(request, *args, **kwargs)
#         else:
#             raise PermissionDenied

#     wrap.__doc__ = function.__doc__
#     wrap.__name__ = function.__name__
#     return wrap


# from django.db.models import Aggregate, CharField, OuterRef
# from apps.products.models import Product
# from apps.purchases.models import Purchase

# # From https://stackoverflow.com/questions/10340684/group-concat-equivalent-in-django
# class GroupConcat(Aggregate):
#     function = 'GROUP_CONCAT'
#     template = '%(function)s(%(distinct)s%(expressions)s%(ordering)s%(separator)s)'

#     def __init__(self, expression, distinct=False, ordering=None, separator=',', **extra):
#         super().__init__(
#             expression,
#             distinct='DISTINCT ' if distinct else '',
#             ordering=' ORDER BY %s' % ordering if ordering is not None else '',
#             separator=' SEPARATOR "%s"' % separator,
#             output_field=CharField(),
#             **extra
#         )

# query = Purchase.objects.values(
#     "field1",
#     comma_sep_field=Product.objects.values("field12").filter(
#         field12=OuterRef("field12")
#     ).values(value=GroupConcat("commaSeparatedField"))
# )

# print('QUERY_FROM_UTILS', query)


##*********## Very important **********##
def model_id_restriction(app_name, model_name):
    def wrap(function):
        def wrapped(request, *args, **kwargs):
            if request.user.is_authenticated:
                print("KWARGS-FROM-DECORATOR***", kwargs, app_name, model_name)
                check = False
                # check_pro_id = 'product_id'
                if model_name == "Product":
                    kwargs_var = kwargs["product_id"]
                    cls = apps.get_model(app_name, model_name)
                    check = cls.objects.filter(id=kwargs_var).exists()
                elif (
                    model_name == "Vendor"
                    or model_name == "Treasury"
                    or model_name == "TreasuryTransfer"
                    or model_name == "TreasuryOpenBalance"
                    or model_name == "TreasuryAdjustment"
                    or model_name == "PaymentReceipt"
                    or model_name == "CatchReceipt"
                    or model_name == "Stores"
                    or model_name == "StoreAdjustment"
                    or model_name == "OpenBalance"
                    or model_name == "Purchase"
                    or model_name == "ReturnPurchase"
                    or model_name == "Product"
                    or model_name == "CreateWallet"
                    or model_name == "CreateVisa"
                    or model_name == "Expenses"
                    or model_name == "ExpensesBill"
                    or model_name == "UnitNames"
                    or model_name == "PosStation"
                    or model_name == "Departments"
                    or model_name == "Branches"
                    or model_name == "Bank"
                    or model_name == "BankAccount"
                    or model_name == "Client"
                    or model_name == "PurchaseRequest"
                    or model_name == "SellService"
                    or model_name == "ReturnSellService"
                ):

                    kwargs_var = kwargs["id"]
                    cls = apps.get_model(app_name, model_name)
                    check = cls.objects.filter(id=kwargs_var).exists()

                elif model_name == "ParentCategory":
                    kwargs_var = kwargs["category_id"]
                    cls = apps.get_model(app_name, model_name)
                    check = cls.objects.filter(id=kwargs_var).exists()

                elif model_name == "Items":
                    kwargs_var = kwargs["order_id"]
                    cls = apps.get_model(app_name, model_name)
                    check = cls.objects.filter(id=kwargs_var).exists()

                elif model_name == "CustomUser":
                    kwargs_var = kwargs["user_id"]
                    cls = apps.get_model(app_name, model_name)
                    check = cls.objects.filter(id=kwargs_var).exists()

                if check:
                    return function(request, *args, **kwargs)
                else:
                    # from django.http import HttpResponse
                    # return redirect('/home/page/not/found/404/')
                    return redirect(reverse("home:error_page", args=("404",)))
                    # return HttpResponse(str([f'Error ID: {value}' for key, value in kwargs.items()][0]))
            else:
                return redirect("/accounts/login/")

        wrap.__doc__ = function.__doc__
        wrap.__name__ = function.__name__
        return wrapped

    return wrap


def user_owner_only(function):
    def wrap(request, *args, **kwargs):
        if request.user.role == "supplier":
            if kwargs["user_id"] != None:
                if kwargs["user_id"] == request.user.id:
                    return function(request, *args, **kwargs)
                else:
                    return redirect("/dashboard/for/supplier/")
            else:
                return redirect("/dashboard/for/supplier/")
        elif request.user.role == "admin":
            return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


##
from functools import wraps
from apps.configurations.models.settings_models import ManageAppSettings


def test_function_works(*args, **kwargs):
    if args[0]:
        return True
    return False


def some_decorator(*decorator_args, **decorator_kwargs):
    def decorator(view_function):
        @wraps(view_function)
        def _wrapped_view(request, *args, **kwargs):
            print(
                "The required actions will be taken here ! Well, \
            actually inside the _wrapped_view function"
            )

            if not test_function_works():
                print(
                    "The necessary operation that will be taken if \
                        the test case fails !"
                )

            return view_function(request, *args, **kwargs)

        return _wrapped_view

    return decorator


## ---------------------   ------------------------------ ##
# def check_app_settings(app_name, model_name):
def single_clinic_app(function):
    def wrap(request, *args, **kwargs):
        if ManageAppSettings.objects.exists():
            app_type = ManageAppSettings.objects.first().app_type
        else:
            app_type = 0
        if app_type == 1 or app_type == 2 or app_type == 3:
            return redirect(
                reverse(
                    "index",
                )
            )
        elif app_type == 0:
            # return redirect("/")
            return function(request, *args, **kwargs)
        # else:
        #     return redirect(reverse("home:error_page", args=("404",)))

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__

    return wrap


def multi_clinics_app(function):
    def wrap(request, *args, **kwargs):
        url = "/"
        app_type = 0
        if ManageAppSettings.objects.exists():
            app_type = ManageAppSettings.objects.first().app_type
        else:
            redirect(url)
        # if url:

        if app_type == 2:
            return function(request, *args, **kwargs)
        else:
            return redirect(reverse("home:error_page", args=("404",)))
        # else:
        #     return redirect("/accounts/login/")

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__

    return wrap
