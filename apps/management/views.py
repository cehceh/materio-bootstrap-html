from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse_lazy
from .models import CreateVisa, CreateWallet #CreateObject
# from .forms import AddCreateObjectForm


def create_visa(request):
    pass


def edit_visa(request, id):
    pass


# def add_create_object(request):
#     if request.method == "POST":
#         form = AddCreateObjectForm(request.POST or None)
#         if form.is_valid():
#             for x in form:
#                 print(x.name, x.errors)
#                 print(" -------------- Line 16 Create Object Views.py ")
#             valid_form = form.save(commit=False)
#             valid_form.user = request.user
#             valid_form.updated_user = request.user
#             name = request.POST.get("name")
#             match = CreateObject.objects.filter(name=name).exists()
#             if not match:
#                 for x in form:
#                     print(x.name, x.errors)
#                     print(" -------------- Line 25 Create Object Views.py ")
#                 valid_form.save()
#                 name = valid_form.name
#                 id = valid_form.id
#                 messages.success(request, f"Object with name ({name}) created successfully.")
#                 return redirect(reverse_lazy("management:edit_create_object", args=(id,)))
#             else:
#                 messages.error(request, f"Add Object with name ({name}) failed, It seems that name already exists")
#                 return redirect(reverse_lazy("management:add_create_object"))
#         else:
#             messages.error(request, "Please fill in the form with valid data.")
#             form = AddCreateObjectForm()
#     else:
#         form = AddCreateObjectForm()
#     table_search = request.GET.get("table_search")
#     if table_search is None or table_search == "":
#         qs = CreateObject.objects.filter(user=request.user).only().order_by("type")
#     elif "table_search" in request.GET or request.GET["table_search"].strip():
#         qs = CreateObject.objects.filter(Q(user=request.user, name__icontains=table_search)).only().order_by("type")
#     else:
#         qs = CreateObject.objects.filter(Q(user=request.user)).only().order_by("type")

#     paginator = Paginator(qs, 4)
#     page = request.GET.get("page")
#     try:
#         main_page = paginator.page(page)
#     except PageNotAnInteger:
#         main_page = paginator.page(1)
#     except EmptyPage:
#         main_page = paginator.page(paginator.num_pages)
#     context = {
#         "form": form,
#         "page": page,
#         "main_page": main_page,
#         "title": "Create Object",
#     }
#     return render(request, "management/add_create_object.html", context)


# def edit_create_object(request, id):
#     qs = CreateObject.objects.get(id=id)
#     form = AddCreateObjectForm(request.POST or None, instance=qs)
#     if form.is_valid():
#         valid_form = form.save(commit=False)
#         valid_form.updated_user = request.user
#         valid_form.save()
#         name = valid_form.name
#         messages.success(request, f"Edit Object with name {name} done successfully")
#     context = {
#         "form": form,
#         "title": "Edit Object",
#     }
#     return render(request, "management/edit_create_object.html", context)
