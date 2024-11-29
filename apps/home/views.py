from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect

from django.conf import settings
from django.utils import translation

from web_project import TemplateLayout
from apps.configurations.models.settings_models import ManageAppSettings

# from apps.products.models import Product, ProductImage
# from apps.products.forms import ProductImageForm
# from apps.purchases.models import Purchase

# from apps.carts.models import Orders
# from apps.accounts.models import AdminProfile, CustomerProfile
# from apps.treasuries.models import (
#     PaymentReceipt,
#     CatchReceipt,
#     Treasury,
#     TreasuryOpenBalance,
#     TreasuryAdjustment,
#     TreasuryTransfer,
# )
# from apps.carts.models import SellService
# from apps.inventories.models import InventoryStore


def select_app(request, *args, **kwargs):

    data = {}
    # TemplateLayoutObj = TemplateLayout
    context = TemplateLayout.init(
        TemplateLayout, data  # TemplateLayoutObj.get_context_data(**kwargs)
    )
    if request.accepts("*/*") and request.method == "POST":
        company = request.POST.get("company")
        bussiness = request.POST.get("app-type")
        print("BUSSINESS==>>", bussiness)
        if bussiness == "0":
            data["msg"] = "Please enter the bussiness type !"
            data["type"] = "error"
            return JsonResponse(data)

        if company == "":
            data["msg"] = "Please enter the name !"
            data["type"] = "error"
            return JsonResponse(data)

        if (
            not ManageAppSettings.objects.exists()
            or not ManageAppSettings.objects.filter(company=company).exists()
        ):
            ManageAppSettings.objects.create(
                company=company,  #'Mohamed Fathy Khalaf',
                app_type=bussiness,
            )
            data["msg"] = "Save Done"
            data["type"] = "success"
            return JsonResponse(data)
        else:
            print("Please Update The Table .....")
            data["msg"] = "Please Update The Table ....."
            data["type"] = "error"
            return JsonResponse(data)

    # else:
    #     data["msg"] = "An error occurs"
    #     data["type"] = "error"
    #     return JsonResponse(data)

    context["title"] = "Choose you app. "
    return render(request, "home/select_app.html", context)


def change_language(request, language):
    response = HttpResponseRedirect(request.META.get("HTTP_REFERER", ""))

    if language:
        translation.activate(language)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)

    return response


def test_views(request):
    context = {
        "title": "Test Views",
    }
    return render(request, "main_page/cashier_page.html", context)


def error_page(request, type):
    context = {"title": "Error Page ( " + str(type) + " )"}
    if type == "404":
        return render(request, "home/page-404.html", context)
    elif type == "403":
        return render(request, "home/page-403.html", context)
    else:
        return render(request, "home/page-500.html", context)


def main_page(request):

    context = {}
    return render(request, "home/main_page.html", context)


# def add_test_image(request, product_id):
#     data = {}
#     data["error"] = "Error !!!"
#     data["type"] = "error"
#     if request.method == "POST":  # request.accepts('text/html') and
#         img_files = request.FILES.get("photo")
#         img_list = request.FILES.getlist("photo", [])
#         print(
#             "MY-IMAGE-PHOTO-FILES: ",
#             img_files,
#             "MY-IMAGES-PHOTO-LIST: ",
#             img_list,
#             "MY-FORM-DATA:::",
#             request.POST.get("photo"),
#             # json.loads(request.POST.get('formData')),
#         )
#         img_form = ProductImageForm(request.POST or None, request.FILES or None)
#         if img_form.is_valid():
#             img_save_form = img_form.save(commit=False)
#             img_save_form.product_id = product_id
#             # img_save_form.photo = request.FILES['photo']
#             img_save_form.save()
#             print(
#                 "IMAGE FORM IS VALID AND IMAGE SAVED DONE ...",
#                 # request.FILES['photo']
#             )
#             data["error"] = _("IMAGE FORM IS VALID AND IMAGE SAVED DONE")
#             data["type"] = "success"
#             return JsonResponse(data)
#             # return redirect(reverse(
#             #     'test_image_details', args=(product_id,)
#             # ))
#         else:
#             print("IMAGE Form Is Invalid !!!")
#     else:
#         img_form = ProductImageForm()

#     # else:
#     #     data['error'] = 'Product ID does not exist'
#     #     data['type'] = 'error'
#     #     return JsonResponse(data)

#     context = {"img_form": img_form, "product_id": product_id}
#     return render(request, "home/add_test_image.html", context)


# def test_image_details(request, product_id):
#     product_images = ProductImage.objects.select_related("product").filter(
#         product_id=product_id
#     )
#     print("product_images: ", product_images)
#     context = {
#         "product_id": product_id,
#         "images": product_images,
#     }
#     return render(request, "home/test_image_details.html", context)


# Create your views here.
# @admin_only
#!######################################## old code 149 qs
# def dashboard(request):
#     # product = Product.objects.values("id").count()
#     months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

#     ## Query for products
#     products = Product.objects.values('id').count()
#     products_per_month = [
#         (
#             Product.objects.values('id').filter(
#                 created_at__month=i
#             ).count()
#         ) for i in months
#     ]
#     product_month = simplejson.dumps(products_per_month)

#     #? for
#     purchase_bills_count = Purchase.objects.only().count()
#     purchase_bills = [
#         (
#             Purchase.objects \
#                 .only().filter(
#                     created_at__year=date.today().year,
#                     created_at__month=i
#                 ).count()
#         ) for i in months
#     ]
#     purchase_bills_per_month = simplejson.dumps(purchase_bills)

#     sale_bills_count = SellService.objects.only().count()
#     sale_bills = [
#         (
#             SellService.objects \
#                 .only().filter(
#                     created_at__year=date.today().year,
#                     created_at__month=i
#                 ).count()
#         ) for i in months
#     ]
#     sale_bills_per_month = simplejson.dumps(sale_bills)
#     # = [  created_at__year=date.today().year,
#     #     "owner", "client", 'admin', 'vendor', 'manager', 'employee',
#     #     'rep', 'driver', 'guest' ]
#     #? for employees users
#     employees= [
#         (
#             CustomUser.objects \
#                 .only().filter(
#                     role='employee',
#                     date_joined__year=date.today().year,
#                     date_joined__month=i
#                 ).count()
#         ) for i in months
#     ]
#     employees_per_month = simplejson.dumps(employees)

#     #* for admin users
#     admins = [
#         (
#             CustomUser.objects \
#                 .only().filter(
#                     role='admin',
#                     date_joined__year=date.today().year,
#                     date_joined__month=i
#                 ).count()
#         ) for i in months
#     ]
#     admins_per_month = simplejson.dumps(admins)
#     #* for vendors users
#     vendors = [
#         (
#             CustomUser.objects \
#                 .only().filter(
#                     role='vendor',
#                     date_joined__year=date.today().year,
#                     date_joined__month=i
#                 ).count()
#         ) for i in months
#     ]
#     vendors_per_month = simplejson.dumps(vendors)

#     #*
#     order = Orders.objects.values("id").filter()
#     total_orders = order.count()
#     completed_orders = order.filter(status="completed").count()
#     canceled_orders = order.filter(status="canceled").count()

#     print(
#         'PRODUCTS-PER-MONTH:', products_per_month,
#         Product.objects.filter(
#             created_at__year=date.today().year,
#             created_at__month=4
#         ).count()
#     )
#     from django.db.models import Count

#     # Query for accounting
#     payment = PaymentReceipt.objects.values('id').count()
#     payment_per_month = [
#         (
#             PaymentReceipt.objects.values('id').filter(
#                 created_at__year=date.today().year,
#                 created_at__month=i
#             ).count()
#         ) for i in months
#     ]
#     payment_month = simplejson.dumps(payment_per_month)

#     catch = CatchReceipt.objects.values('id').count()
#     catch_per_month = [
#         (
#             CatchReceipt.objects.values('id').filter(
#                 created_at__year=date.today().year,
#                 created_at__month=i
#             ).count()
#         ) for i in months
#     ]
#     catch_month = simplejson.dumps(catch_per_month)

#     # open_bal = CatchReceipt.objects.values('id').count()
#     open_per_month = [
#         (
#             TreasuryOpenBalance.objects.values('id').filter(
#                 created_at__year=date.today().year,
#                 created_at__month=i
#             ).count()
#         ) for i in months
#     ]
#     open_month = simplejson.dumps(open_per_month)

#     adj_per_month = [
#         (
#             TreasuryAdjustment.objects.values('id').filter(
#                 created_at__year=date.today().year,
#                 created_at__month=i
#             ).count()
#         ) for i in months
#     ]
#     adj_month = simplejson.dumps(adj_per_month)


#     main_qs = CustomUser.objects.select_related('address').only().order_by('-id')[:5]


#     context = {
#         "products": products,
#         'main_qs':main_qs,
#         "product_month": product_month,
#         "purchase_month": purchase_bills_per_month,
#         "purchase_bills": purchase_bills_count,
#         "sale_month": sale_bills_per_month,
#         "sale_bills": sale_bills_count,
#         "admins": CustomUser.objects.values('id').filter(role='admin').count(),
#         "employees": CustomUser.objects.values('id').filter(role='employee').count(),
#         "vendors": CustomUser.objects.values('id').filter(role='vendor').count(),
#         "catches":CatchReceipt.objects.values('id').count(),
#         "payment":PaymentReceipt.objects.values('id').count(),
#         "open_bal":TreasuryOpenBalance.objects.values('id').count(),
#         "adjustment":TreasuryAdjustment.objects.values('id').count(),
#         "transfer_visa":TreasuryTransfer.objects.filter(treasury_types=2).values('id').count(),
#         "transfer_wallet":TreasuryTransfer.objects.filter(treasury_types=3).values('id').count(),
#         "transfer_bank":TreasuryTransfer.objects.filter(treasury_types=4).values('id').count(),
#         "transfer_treasury":TreasuryTransfer.objects.filter(treasury_types=1).values('id').count(),
#         # "destination":DestinationTransfer.objects.values('id').count(),
#         "catches_per_month":catch_month,
#         "open_per_month":open_month,
#         "adj_per_month":adj_month,
#         "payment_per_month":payment_month,
#         "admins_per_month": admins_per_month,
#         "employees_per_month": employees_per_month,
#         "vendors_per_month": vendors_per_month,
#         "total_orders": total_orders,
#         "completed_orders": completed_orders,
#         "canceled_orders": canceled_orders,
#         "title": "Dashboard",
#     }
#     return render(request, "home/dashboard.html", context)
# ###########################????????? new code 32 qs but unexpected behavoiur in some queries for accounting
# from django.db.models import Count
# from django.utils import timezone

# def dashboard(request):
#     current_year = timezone.now().year
#     months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

#     # Query for products
#     products = Product.objects.count()
#     products_per_month = Product.objects.values('created_at__month').annotate(count=Count('id')).order_by('created_at__month')
#     product_month = [p['count'] for p in products_per_month]

#     # Query for purchase bills
#     purchase_bills_count = Purchase.objects.count()
#     purchase_bills_per_month = Purchase.objects.values('created_at__month').annotate(count=Count('id')).order_by('created_at__month')
#     purchase_bills_month = [p['count'] for p in purchase_bills_per_month]

#     # Query for sale bills
#     sale_bills_count = SellService.objects.count()
#     sale_bills_per_month = SellService.objects.values('created_at__month').annotate(count=Count('id')).order_by('created_at__month')
#     sale_bills_month = [p['count'] for p in sale_bills_per_month]

#     # Query for users
#     roles = ['admin', 'employee', 'vendor']
#     users_per_month = {}
#     for role in roles:
#         users_per_month[role] = CustomUser.objects.filter(role=role, date_joined__year=current_year).values('date_joined__month').annotate(count=Count('id')).order_by('date_joined__month')
#         users_per_month[role] = [u['count'] for u in users_per_month[role]]

#     # Query for accounting
#     catches = CatchReceipt.objects.count()
#     catches_per_month = CatchReceipt.objects.values('created_at__month').annotate(count=Count('id')).order_by('created_at__month')
#     catches_month = [c['count'] for c in catches_per_month]

#     payment = PaymentReceipt.objects.count()
#     payment_per_month = PaymentReceipt.objects.values('created_at__month').annotate(count=Count('id')).order_by('created_at__month')
#     payment_month = [p['count'] for p in payment_per_month]

#     open_bal = TreasuryOpenBalance.objects.count()
#     open_per_month = TreasuryOpenBalance.objects.values('created_at__month').annotate(count=Count('id')).order_by('created_at__month')
#     open_month = [o['count'] for o in open_per_month]

#     adjustment = TreasuryAdjustment.objects.count()
#     adj_per_month = TreasuryAdjustment.objects.values('created_at__month').annotate(count=Count('id')).order_by('created_at__month')
#     adj_month = [a['count'] for a in adj_per_month]

#     transfer_visa = TreasuryTransfer.objects.filter(treasury_types=2).count()
#     transfer_wallet = TreasuryTransfer.objects.filter(treasury_types=3).count()
#     transfer_bank = TreasuryTransfer.objects.filter(treasury_types=4).count()
#     transfer_treasury = TreasuryTransfer.objects.filter(treasury_types=1).count()

#     main_qs = CustomUser.objects.select_related('address').only().order_by('-id')[:5]

#     context = {
#         "products": products,
#         'main_qs': main_qs,
#         "product_month": product_month,
#         "purchase_month": purchase_bills_month,
#         "purchase_bills": purchase_bills_count,
#         "sale_month": sale_bills_month,
#         "sale_bills": sale_bills_count,
#         "admins": CustomUser.objects.filter(role='admin').count(),
#         "employees": CustomUser.objects.filter(role='employee').count(),
#         "vendors": CustomUser.objects.filter(role='vendor').count(),
#         "catches": catches,
#         "catches_per_month": catches_month,
#         "payment": payment,
#         "payment_per_month": payment_month,
#         "admins_per_month": users_per_month['admin'],
#         "employees_per_month": users_per_month['employee'],
#         "vendors_per_month": users_per_month['vendor'],
#         "open_bal": open_bal,
#         "open_per_month": open_month,
#         "adjustment": adjustment,
#         "adj_per_month": adj_month,
#         "transfer_visa": transfer_visa,
#         "transfer_wallet": transfer_wallet,
#         "transfer_bank": transfer_bank,
#         "transfer_treasury": transfer_treasury,
#         "title": "Dashboard",
#     }
#     return render(request, "home/dashboard.html", context)

###################################################################?another trial 86 qs


# @admin_only
# def dashboard(request):
#     # trans_data = requests.post()
#     current_year = timezone.now().year
#     months = range(1, 13)
#     roles = ["admin", "employee", "vendor", "client"]  # Define roles here

#     # *Client Card
#     result = ClientUsers.objects.filter(role=1).aggregate(
#         total_clients=Count("id"), total_balance=Sum("balance")
#     )

#     clients = result["total_clients"]
#     total_balance = result["total_balance"]

#     # *Purchase Card
#     purchases_bill_summary = PurchasePayments.objects.select_related(
#         "purchase"
#     ).aggregate(
#         total_purchases_bill=Count("id"),
#         total_amount=Sum(
#             "purchase__grand_total"
#         ),  # Assuming 'amount' is the field holding the amount value
#     )

#     total_purchases_bill = purchases_bill_summary["total_purchases_bill"]
#     purchase_total_amount = purchases_bill_summary["total_amount"]

#     # *Vendor Card
#     result = ClientUsers.objects.filter(role=3).aggregate(
#         total_vendors=Count("id"), total_balance=Sum("balance")
#     )

#     vendors = result["total_vendors"]
#     vendor_total_balance = result["total_balance"]

#     # *Expenses Card
#     result = ExpensesBill.objects.aggregate(
#         total_expenses=Count("id"), total_amount=Sum("amount")
#     )
#     total_expenses = result["total_expenses"]
#     expenses_total_amount = result["total_amount"]

#     # product_count = InventoryStore.objects.filter(
#     #     available_quantity__gt=0).values(
#     #         'inventory__product_id').distinct().count()

#     # *Product Card
#     result = Product.objects.aggregate(
#         total_products=Count("id"),
#         total_active=Count(
#             Case(When(active=True, then=1), output_field=IntegerField())
#         ),
#         total_inactive=Count(
#             Case(When(active=False, then=1), output_field=IntegerField())
#         ),
#     )
#     total_products = result["total_products"]
#     total_active = result["total_active"]
#     total_inactive = result["total_inactive"]

#     # *Inventory Card
#     product_count = InventoryStore.objects.filter(available_quantity__gt=0).aggregate(
#         product_count=Count("inventory__product_id", distinct=True)
#     )["product_count"]

#     if SellService.objects.only() is not None and SellService.objects.count() > 0:

#         # *Sales Card
#         sales_bill_summary = SellServicePayments.objects.select_related(
#             "service"
#         ).aggregate(
#             total_sales_bill=Count("id"),
#             total_amount=Sum(
#                 "service__grand_total"
#             ),  # Assuming 'amount' is the field holding the amount value
#             paied_sales_bill=Count(
#                 Case(When(payment_methods=1, then=1), output_field=IntegerField())
#             ),
#             paied_sales_amount=Sum(
#                 Case(
#                     When(payment_methods=1, then="service__grand_total"),
#                     output_field=IntegerField(),
#                 )
#             ),
#             unpaied_sales_bill=Count(
#                 Case(When(payment_methods=2, then=1), output_field=IntegerField())
#             ),
#             unpaied_sales_amount=Sum(
#                 Case(
#                     When(payment_methods=2, then="service__grand_total"),
#                     output_field=IntegerField(),
#                 )
#             ),
#         )

#         total_sales_bill = sales_bill_summary["total_sales_bill"]
#         total_amount = sales_bill_summary["total_amount"]
#         paied_sales_bill = sales_bill_summary["paied_sales_bill"]
#         paied_sales_amount = sales_bill_summary["paied_sales_amount"]
#         unpaied_sales_bill = sales_bill_summary["unpaied_sales_bill"]
#         unpaied_sales_amount = sales_bill_summary["unpaied_sales_amount"]

#         # *Most Sold Product Card
#         # First, find the maximum number of unique services a product occurs in
#         max_service_count = (
#             ServiceProduct.objects.values("product")
#             .annotate(service_count=Count("service", distinct=True))
#             .order_by("-service_count")
#             .values("service_count")[:1]
#         )

#         # Fetch the product(s) with that maximum service count
#         most_frequent_product = (
#             ServiceProduct.objects.values("product")
#             .annotate(service_count=Count("service", distinct=True))
#             .filter(service_count=Subquery(max_service_count))
#             .order_by("-service_count")
#             .first()
#         )

#         # Query for sale bills
#         sale_bills_month_query = (
#             SellService.objects.filter(created_at__year=current_year)
#             .annotate(month=ExtractMonth("created_at"))
#             .values("month")
#             .annotate(count=Count("id"))
#             .order_by("month")
#         )
#         sale_bills_month = [p["count"] for p in sale_bills_month_query]

#         # To get the product object itself
#         if most_frequent_product:
#             most_frequent_product_id = most_frequent_product["product"]
#             most_frequent_product_instance = Product.objects.get(
#                 id=most_frequent_product["product"]
#             )
#             number_of_services = most_frequent_product["service_count"]
#             print(
#                 "most_frequent_product_instance",
#                 most_frequent_product_instance,
#                 "number_of_services",
#                 number_of_services,
#             )

#         # *Least Sold Product Card
#         # First, find the minimum number of unique services a product occurs in
#         min_service_count = (
#             ServiceProduct.objects.values("product")
#             .annotate(service_count=Count("service", distinct=True))
#             .order_by("service_count")
#             .values("service_count")[:1]
#         )

#         # Fetch the product(s) with that minimum service count
#         least_frequent_product = (
#             ServiceProduct.objects.values("product")
#             .annotate(service_count=Count("service", distinct=True))
#             .filter(service_count=Subquery(min_service_count))
#             .order_by("service_count")
#             .first()
#         )

#         # To get the product object itself
#         if least_frequent_product:
#             least_frequent_product_id = least_frequent_product["product"]
#             least_frequent_product_instance = Product.objects.get(
#                 id=least_frequent_product["product"]
#             )
#             least_number_of_services = least_frequent_product["service_count"]
#             print(
#                 "least_frequent_product_instance",
#                 least_frequent_product_instance,
#                 "least_number_of_services",
#                 least_number_of_services,
#             )

#     else:
#         total_sales_bill = 0
#         total_amount = 0
#         paied_sales_bill = 0
#         paied_sales_amount = 0
#         unpaied_sales_bill = 0
#         unpaied_sales_amount = 0

#         most_frequent_product_id = 0
#         most_frequent_product_instance = 0
#         number_of_services = 0

#         least_frequent_product_id = 0
#         least_frequent_product_instance = 0
#         least_number_of_services = 0

#         sale_bills_month = 0

#     # *Payment Receipt Card
#     result = PaymentReceipt.objects.aggregate(
#         total_payment_receipts=Count("id"), total_payment_receipts_amount=Sum("amount")
#     )
#     total_payment_receipts = result["total_payment_receipts"]
#     total_payment_receipts_amount = result["total_payment_receipts_amount"]

#     # *Catch Receipt Card
#     result = CatchReceipt.objects.aggregate(
#         total_catch_receipts=Count("id"), total_catch_receipts_amount=Sum("amount")
#     )
#     total_catch_receipts = result["total_catch_receipts"]
#     total_catch_receipts_amount = result["total_catch_receipts_amount"]

#     # *Treasuries Card
#     result = Treasury.objects.aggregate(
#         total_treasuries=Count("id"), total_treasuries_balance=Sum("total")
#     )
#     total_treasuries = result["total_treasuries"]
#     total_treasuries_balance = result["total_treasuries_balance"]

#     # *Visas Card
#     result = CreateVisa.objects.aggregate(
#         total_visa=Count("id"), total_visa_balance=Sum("total")
#     )
#     total_visa = result["total_visa"]
#     total_visa_balance = result["total_visa_balance"]

#     # *Wallets Card
#     result = CreateWallet.objects.aggregate(
#         total_wallet=Count("id"), total_wallet_balance=Sum("total")
#     )
#     total_wallet = result["total_wallet"]
#     total_wallet_balance = result["total_wallet_balance"]

#     # *Wallets Card
#     result = BankAccount.objects.aggregate(
#         total_accounts=Count("id"), total_accounts_balance=Sum("total")
#     )
#     total_accounts = result["total_accounts"]
#     total_accounts_balance = result["total_accounts_balance"]
#     # total_purchase = InventoryStore.objects.filter(available_quantity__gt=0).values('inventory__product_id').distinct().aggregate(
#     #     total_purchase=Sum('inventory__product_id')
#     # )
#     # Query for products
#     product_month_query = (
#         Product.objects.filter(created_at__year=current_year)
#         .annotate(month=ExtractMonth("created_at"))
#         .values("month")
#         .annotate(count=Count("id"))
#         .order_by("month")
#     )
#     product_month = [p["count"] for p in product_month_query]

#     # Query for purchase bills
#     purchase_bills_month_query = (
#         Purchase.objects.filter(created_at__year=current_year)
#         .annotate(month=ExtractMonth("created_at"))
#         .values("month")
#         .annotate(count=Count("id"))
#         .order_by("month")
#     )
#     purchase_bills_month = [p["count"] for p in purchase_bills_month_query]

#     # Query for users
#     users_per_month_query = (
#         CustomUser.objects.filter(date_joined__year=current_year)
#         .annotate(month=ExtractMonth("date_joined"))
#         .values("month", "role")
#         .annotate(count=Count("id"))
#         .order_by("month")
#     )
#     users_per_month = {month: {role: 0 for role in roles} for month in months}
#     for user in users_per_month_query:
#         users_per_month[user["month"]][user["role"]] = user["count"]

#     # Query for accounting
#     catch_per_month = [
#         CatchReceipt.objects.filter(
#             created_at__year=current_year, created_at__month=i
#         ).count()
#         for i in months
#     ]
#     catch_month = simplejson.dumps(catch_per_month)

#     payment_per_month = [
#         PaymentReceipt.objects.filter(
#             created_at__year=current_year, created_at__month=i
#         ).count()
#         for i in months
#     ]
#     payment_month = simplejson.dumps(payment_per_month)

#     open_per_month = [
#         TreasuryOpenBalance.objects.filter(
#             created_at__year=current_year, created_at__month=i
#         ).count()
#         for i in months
#     ]
#     open_month = simplejson.dumps(open_per_month)

#     adj_per_month = [
#         TreasuryAdjustment.objects.filter(
#             created_at__year=current_year, created_at__month=i
#         ).count()
#         for i in months
#     ]
#     adj_month = simplejson.dumps(adj_per_month)

#     transfer_per_month = [
#         TreasuryTransfer.objects.filter(
#             created_at__year=current_year,
#             created_at__month=i,
#             treasury_types__in=[1, 2, 3, 4],
#         ).count()
#         for i in months
#     ]
#     transfer_month = transfer_per_month

#     main_qs = CustomUser.objects.select_related("address").only().order_by("-id")[:5]

#     context = {
#         "total_sales_bill": total_sales_bill,
#         "total_amount": total_amount,
#         "paied_sales_bill": paied_sales_bill,
#         "unpaied_sales_bill": unpaied_sales_bill,
#         "clients_total": clients,
#         "client_total_balance": total_balance,
#         "total_purchases_bill": total_purchases_bill,
#         "purchase_total_amount": purchase_total_amount,
#         "vendors_total": vendors,
#         "vendor_total_balance": vendor_total_balance,
#         "total_expenses": total_expenses,
#         "expenses_total_amount": expenses_total_amount,
#         "product_count": product_count,
#         "total_products": total_products,
#         "total_active": total_active,
#         "total_inactive": total_inactive,
#         "most_frequent_product_id": most_frequent_product_id,
#         "most_frequent_product_instance": most_frequent_product_instance,
#         "number_of_services": number_of_services,
#         "least_frequent_product_id": least_frequent_product_id,
#         "least_frequent_product_instance": least_frequent_product_instance,
#         "least_number_of_services": least_number_of_services,
#         "total_payment_receipts": total_payment_receipts,
#         "total_payment_receipts_amount": total_payment_receipts_amount,
#         "total_catch_receipts": total_catch_receipts,
#         "total_catch_receipts_amount": total_catch_receipts_amount,
#         "total_treasuries": total_treasuries,
#         "total_treasuries_balance": total_treasuries_balance,
#         "total_visa": total_visa,
#         "total_visa_balance": total_visa_balance,
#         "total_wallet": total_wallet,
#         "total_wallet_balance": total_wallet_balance,
#         "total_accounts": total_accounts,
#         "total_accounts_balance": total_accounts_balance,
#         "products": Product.objects.count(),
#         "main_qs": main_qs,
#         "product_month": product_month,
#         "purchase_month": purchase_bills_month,
#         "purchase_bills": Purchase.objects.count(),
#         "sale_month": sale_bills_month,
#         "sale_bills": SellService.objects.count(),
#         "admins": CustomUser.objects.filter(role="admin").count(),
#         "employees": CustomUser.objects.filter(role="employee").count(),
#         "vendors": CustomUser.objects.filter(role="vendor").count(),
#         "client": CustomUser.objects.filter(role="client").count(),
#         "catches": CatchReceipt.objects.count(),
#         "catches_per_month": catch_month,
#         "payment": PaymentReceipt.objects.count(),
#         "payment_per_month": payment_month,
#         "admins_per_month": [users_per_month[month]["admin"] for month in months],
#         "employees_per_month": [users_per_month[month]["employee"] for month in months],
#         "vendors_per_month": [users_per_month[month]["vendor"] for month in months],
#         "client_per_month": [users_per_month[month]["client"] for month in months],
#         "open_bal": TreasuryOpenBalance.objects.count(),
#         "open_per_month": open_month,
#         "adjustment": TreasuryAdjustment.objects.count(),
#         "adj_per_month": adj_month,
#         "transfer_visa": transfer_per_month.count(2),
#         "transfer_wallet": transfer_per_month.count(3),
#         "transfer_bank": transfer_per_month.count(4),
#         "transfer_treasury": transfer_per_month.count(1),
#         "title": "Dashboard",
#     }
#     return render(request, "home/dashboard.html", context)


# from django.db.models import Count
# from django.utils import timezone

# def dashboard(request):
#     current_year = timezone.now().year
#     months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

#     # Query for products
#     products = Product.objects.count()
#     products_per_month = Product.objects.values('created_at__month').annotate(count=Count('id')).order_by('created_at__month')
#     product_month = [p['count'] for p in products_per_month]

#     # Query for purchase bills
#     purchase_bills_count = Purchase.objects.count()
#     purchase_bills_per_month = Purchase.objects.values('created_at__month').annotate(count=Count('id')).order_by('created_at__month')
#     purchase_bills_month = [p['count'] for p in purchase_bills_per_month]

#     # Query for sale bills
#     sale_bills_count = SellService.objects.count()
#     sale_bills_per_month = SellService.objects.values('created_at__month').annotate(count=Count('id')).order_by('created_at__month')
#     sale_bills_month = [p['count'] for p in sale_bills_per_month]

#     # Query for users
#     roles = ['admin', 'employee', 'vendor']
#     users_per_month = {}
#     for role in roles:
#         users_per_month[role] = CustomUser.objects.filter(role=role, date_joined__year=current_year).values('date_joined__month').annotate(count=Count('id')).order_by('date_joined__month')
#         users_per_month[role] = [u['count'] for u in users_per_month[role]]

#     # Query for accounting
#     catches_count = CatchReceipt.objects.count()
#     catches_per_month = CatchReceipt.objects.values('created_at__month').annotate(count=Count('id')).order_by('created_at__month')
#     catch_month = [c['count'] for c in catches_per_month]

#     payment_count = PaymentReceipt.objects.count()
#     payment_per_month = PaymentReceipt.objects.values('created_at__month').annotate(count=Count('id')).order_by('created_at__month')
#     payment_month = [p['count'] for p in payment_per_month]

#     open_bal_count = TreasuryOpenBalance.objects.count()
#     open_per_month = TreasuryOpenBalance.objects.values('created_at__month').annotate(count=Count('id')).order_by('created_at__month')
#     open_month = [o['count'] for o in open_per_month]

#     adj_count = TreasuryAdjustment.objects.count()
#     adj_per_month = TreasuryAdjustment.objects.values('created_at__month').annotate(count=Count('id')).order_by('created_at__month')
#     adj_month = [a['count'] for a in adj_per_month]

#     transfer_visa_count = TreasuryTransfer.objects.filter(treasury_types=2).count()
#     transfer_wallet_count = TreasuryTransfer.objects.filter(treasury_types=3).count()
#     transfer_bank_count = TreasuryTransfer.objects.filter(treasury_types=4).count()
#     transfer_treasury_count = TreasuryTransfer.objects.filter(treasury_types=1).count()

#     main_qs = CustomUser.objects.select_related('address').only().order_by('-id')[:5]

#     context = {
#         "products": products,
#         'main_qs': main_qs,
#         "product_month": product_month,
#         "purchase_month": purchase_bills_month,
#         "purchase_bills": purchase_bills_count,
#         "sale_month": sale_bills_month,
#         "sale_bills": sale_bills_count,
#         "admins": CustomUser.objects.filter(role='admin').count(),
#         "employees": CustomUser.objects.filter(role='employee').count(),
#         "vendors": CustomUser.objects.filter(role='vendor').count(),
#         "catches": catches_count,
#         "catches_per_month": catch_month,
#         "payment": payment_count,
#         "payment_per_month": payment_month,
#         "open_bal": open_bal_count,
#         "open_per_month": open_month,
#         "adjustment": adj_count,
#         "adj_per_month": adj_month,
#         "transfer_visa": transfer_visa_count,
#         "transfer_wallet": transfer_wallet_count,
#         "transfer_bank": transfer_bank_count,
#         "transfer_treasury": transfer_treasury_count,
#         "title": "Dashboard",
#     }
#     return render(request, "home/dashboard.html", context)


######################?????trying to tune
# from django.db.models import Count

# def dashboard(request):
#     # Query for products
#     products = Product.objects.count()
#     products_per_month = Product.objects.values('created_at__month').annotate(count=Count('id')).order_by('created_at__month')
#     product_month = simplejson.dumps([p['count'] for p in products_per_month])

#     # Query for purchase bills
#     purchase_bills_count = Purchase.objects.count()
#     purchase_bills_per_month = Purchase.objects.values('created_at__month').annotate(count=Count('id')).order_by('created_at__month')
#     purchase_bills_month = simplejson.dumps([p['count'] for p in purchase_bills_per_month])

#     # Query for users
#     roles = ['admin', 'employee', 'vendor']
#     users_per_month = {}
#     for role in roles:
#         users_per_month[role] = CustomUser.objects.filter(role=role).values('date_joined__month').annotate(count=Count('id')).order_by('date_joined__month')
#         users_per_month[role] = simplejson.dumps([u['count'] for u in users_per_month[role]])

#     # Query for orders
#     total_orders = Orders.objects.count()
#     completed_orders = Orders.objects.filter(status="completed").count()
#     canceled_orders = Orders.objects.filter(status="canceled").count()


#     main_qs = CustomUser.objects.select_related('address').only().order_by('-id')[:5]

#     context = {
#         "products": products,
#         'main_qs': main_qs,
#         "product_month": product_month,
#         "purchase_month": purchase_bills_month,
#         "purchase_bills": purchase_bills_count,
#         "admins": CustomUser.objects.filter(role='admin').count(),
#         "employees": CustomUser.objects.filter(role='employee').count(),
#         "vendors": CustomUser.objects.filter(role='vendor').count(),
#         # "catches": catch_count,
#         # "catch_per_month": catch_month,
#         # "payment": PaymentReceipt.objects.count(),
#         # "catches_per_month":catch_month,
#         # "payment_per_month":payment_per_month,
#         "admins_per_month": users_per_month['admin'],
#         "employees_per_month": users_per_month['employee'],
#         "vendors_per_month": users_per_month['vendor'],
#         "total_orders": total_orders,
#         "completed_orders": completed_orders,
#         "canceled_orders": canceled_orders,
#         "title": "Dashboard",
#     }
#     return render(request, "home/dashboard.html", context)


# from django.db.models import Count

# def dashboard(request):
#     # Query for products
#     products = Product.objects.count()
#     products_per_month = Product.objects.values('created_at__month').annotate(count=Count('id')).order_by('created_at__month')
#     product_month = simplejson.dumps([p['count'] for p in products_per_month])

#     # Query for purchase bills
#     purchase_bills_count = Purchase.objects.count()
#     purchase_bills_per_month = Purchase.objects.values('created_at__month').annotate(count=Count('id')).order_by('created_at__month')
#     purchase_bills_month = simplejson.dumps([p['count'] for p in purchase_bills_per_month])

#     # Query for users
#     roles = ['admin', 'employee', 'vendor']
#     users_per_month = {}
#     for role in roles:
#         users_per_month[role] = CustomUser.objects.filter(role=role).values('date_joined__month').annotate(count=Count('id')).order_by('date_joined__month')
#         users_per_month[role] = simplejson.dumps([u['count'] for u in users_per_month[role]])

#     # Query for orders
#     total_orders = Orders.objects.count()
#     completed_orders = Orders.objects.filter(status="completed").count()
#     canceled_orders = Orders.objects.filter(status="canceled").count()

#     # Query for main_qs
#     main_qs = CustomUser.objects.select_related('address').only().order_by('-id')[:5]

#     context = {
#         "products": products,
#         'main_qs': main_qs,
#         "product_month": product_month,
#         "purchase_month": purchase_bills_month,
#         "purchase_bills": purchase_bills_count,
#         "admins": CustomUser.objects.filter(role='admin').count(),
#         "employees": CustomUser.objects.filter(role='employee').count(),
#         "vendors": CustomUser.objects.filter(role='vendor').count(),
#         "catches": CatchReceipt.objects.count(),
#         "payment": PaymentReceipt.objects.count(),
#         "admins_per_month": users_per_month['admin'],
#         "employees_per_month": users_per_month['employee'],
#         "vendors_per_month": users_per_month['vendor'],
#         "total_orders": total_orders,
#         "completed_orders": completed_orders,
#         "canceled_orders": canceled_orders,
#         "title": "Dashboard",
#     }
#     return render(request, "home/dashboard.html", context)


# @admin_only
# def admin_dashboard(request, role):
#     ##
#     name = request.user.username
#     customers = (
#         CustomerProfile.objects.select_related("user")
#         .filter(user__role="customer")
#         .count()
#     )

#     # suppliers = VendorProfile.objects.select_related(
#     #     'user').filter(user__role='supplier').count()

#     admins = (
#         AdminProfile.objects.select_related("user").filter(user__role="admin").count()
#     )
#     # print(customers)

#     # start_date = datetime.strptime(str(date.today()), "%Y-%m-%d") #date.today().year
#     # end_date = start_date - timedelta(days=365)
#     # customers_time = UserProfile.objects \
#     #                             .select_related(
#     #                                 'user'
#     #                             ).filter(
#     #                                 user__date_joined__range=[start_date, end_date]
#     #                             )
#     months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

#     customer_per_month = [
#         (
#             CustomerProfile.objects.select_related("user")
#             .filter(
#                 user__role="customer",
#                 user__date_joined__year=date.today().year,
#                 user__date_joined__month=i,
#             )
#             .count()
#         )
#         for i in months
#     ]
#     customer_month = simplejson.dumps(customer_per_month)

#     # supplier_per_month = [
#     #     (
#     #         VendorProfile.objects \
#     #         .select_related(
#     #             'user'
#     #         ).filter(
#     #             user__role='supplier',
#     #             user__date_joined__year=date.today().year,
#     #             user__date_joined__month=i
#     #         ).count()
#     #     ) for i in months
#     # ]
#     # supplier_month = simplejson.dumps(supplier_per_month)

#     ## Query for products
#     products = Product.objects.filter(
#         created_at__year=date.today().year,
#     ).count()
#     products_per_month = [
#         (
#             Product.objects.filter(
#                 created_at__year=date.today().year, created_at__month=i
#             ).count()
#         )
#         for i in months
#     ]
#     product_month = simplejson.dumps(products_per_month)
#     # print('products= ', products, products_per_month, start_date.year, date.today().year)

#     ## Query for order
#     # orders = (
#     #     Orders.objects.select_related("customer")
#     #     .filter(
#     #         created_at__year=date.today().year,
#     #     )
#     #     .count()
#     # )

#     # orders_per_month = [
#     #     (
#     #         Orders.objects.filter(
#     #             created_at__year=date.today().year,
#     #             created_at__month=i,
#     #         ).count()
#     #     )
#     #     for i in months
#     # ]
#     # orders_month = (orders_per_month)
#     # orders_month = simplejson.dumps(orders_per_month)

#     # print('order month:: ', orders_month)
#     context = {
#         "name": name,
#         "customers": customers,
#         # 'suppliers': suppliers,
#         "admins": admins,
#         "products": products,
#         # "orders": orders,
#         "role": role,
#         "customer_month": customer_month,
#         # 'supplier_month': supplier_month,
#         "products_month": product_month,
#         # 'products_per_month': products_per_month,
#         # "orders_month": orders_month,
#         "title": "Admin Dashboard",
#     }
#     return render(request, "dashboard/user_dashboard.html", context)


def frontpage(request):
    """Home page before user sign in"""
    # response = HttpResponseRedirect('hello')
    # if request.path == '/':
    #     request.LANGUAGE_CODE = 'en'
    #     language = 'en'
    # else:
    #     request.LANGUAGE_CODE = language
    # language = request.GET.get('language')
    # language = request.POST.get('language')
    # response = HttpResponse('hello')
    # lang_path = request.path #.split('/')[1]
    # # print('language: '+str(language), lang_path, 'frontpage_LANG_CODE: '+ str(request.LANGUAGE_CODE))
    # print(lang_path, 'frontpage_LANG_CODE: '+ str(request.LANGUAGE_CODE))

    # translation.activate(language)
    # response = HttpResponseRedirect(redirect_path)
    # response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    # return response
    # match = UserProfile.objects.filter(user_id=request.user.id).exists()
    # if match:
    #     profile = UserProfile.objects.get(user_id=request.user.id)
    # else:
    #     profile = None

    # print(match, request.user.id, profile)
    # key = request.session.session_key
    # # print(dir(request.session), key)
    # print(request.session.get('username'))
    context = {
        "title": "Frontpage",
        # 'match_user': match,
        # 'profile': profile,
    }
    # return response
    # return render(request, "", context)
    return render(request, "home/frontpage.html", context)


# def change_language(request):
#     response = HttpResponseRedirect('/en/')
#     if request.method == 'POST':
#         language = request.POST.get('language')
#         if language:
#             if language != settings.LANGUAGE_CODE and [lang for lang in settings.LANGUAGES if lang[0] == language]:
#                 redirect_path = f'/{language}/'
#             elif language == settings.LANGUAGE_CODE:
#                 redirect_path = '/en/'
#             else:
#                 return response
#             translation.activate(language)
#             response = HttpResponseRedirect(redirect_path)
#             response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
#     return response
