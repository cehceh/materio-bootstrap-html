from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse_lazy
from itertools import chain
from django.http import JsonResponse

from .models import CreateVisa
from .forms import CreateVisaForm
from posapp.utils import model_id_restriction

def add_visa(request):
    data = {}
    data['visa_id'] = None 
    data['error'] = 'ERROR !!!'
    data['type'] = 'error'
    if request.accepts('*/*') and request.method == "POST":
        form = CreateVisaForm(
            request.POST or None, 
        )
        
        for f in form:
            print(
                f.name,
                f.errors
            )
            if not f.errors:
                print('No errors, from is valid and : ', request.accepts('*/*'), request.method)
        
        #********************************
        visa_name = request.POST.get("visa_name") 
        visa_number= request.POST.get("visa_no") 
        expire_date = request.POST.get("expire_date")
        bank = request.POST.get("bank")
        bank_account = request.POST.get("account_no")
        
        if CreateVisa.objects.filter(visa_no=visa_number, user=request.user).exists():
            data['msg'] = "Visa with this number already exists."
            return JsonResponse(data)
        
        if visa_name == '':
            data['msg'] = "Please enter a visa  name"
            data['type'] = "error"
            return JsonResponse(data)
        
        if visa_number == '' or visa_number == '0' or visa_number == None:
            data['msg'] = "Please enter a visa  number"
            data['type'] = "error"
            return JsonResponse(data)
        

        if expire_date == '' or expire_date == None or expire_date == '0':
            data['msg'] = "Please enter an expire date"
            data ['error'] = "error"
            return JsonResponse(data)
        
        if bank == '':
            data['msg'] = "Please select bank name"
            data['type'] = "error"
            return JsonResponse(data)
        
        if bank_account == '':
            data['msg'] = "Please select bank account"
            data['type'] = "error"
            return JsonResponse(data)
        
        if not form.is_valid():
            data['visa_id'] = None 
            msg = [
                (key+' Error:', value[0]['message']) for key, value in (
                    form.errors.get_json_data().items()
                )
            ]
            data['msg'] = msg
            data['type'] = 'error'    
            return JsonResponse(data)
        
        if form.is_valid():
            save_form = form.save(commit=False)
            # save_form.full_name = full_name
            save_form.user = request.user
            save_form.updated_user = request.user
            save_form.active = True
            save_form.save()

            CreateVisa.objects.filter(id=save_form.id).update(code='visa-'+str(save_form.id))
                    
            msg = ('Visa with name "%s" saved successfully' % (save_form.visa_name))
            data['visa_id'] = save_form.id 
            data['visa_no'] = save_form.visa_no
            data['msg'] = msg
            data['type'] = 'success'
            return JsonResponse(data)
        
    else:
        form = CreateVisaForm()

    context = {
        'form': form,
        'title': 'Create Visa'
    }
    return render(request, 'management/create_visa/add_visa.html', context)


@model_id_restriction(app_name='management', model_name='CreateVisa')
def edit_visa(request, id):
    data = {}
    data['visa_id'] = id 
    data['msg'] = 'ERROR !!!'
    data['type'] = 'error'
    
    
    qs = CreateVisa.objects.select_related('user').get(id=id)
    form = CreateVisaForm(
        request.POST or None,
        request.FILES or None, 
        instance=qs,
    )
    
    if request.accepts('*/*') and request.method == "POST":
        visa_name = request.POST.get("visa_name") 
        visa_number= request.POST.get("visa_no") 
        expire_date = request.POST.get("expire_date")
        bank = request.POST.get("bank")
        bank_account = request.POST.get("account_no")
        
        # if CreateVisa.objects.filter(visa_no=visa_number, user=request.user).exists():
        #     data['msg'] = "Visa with this number already exists."
        #     return JsonResponse(data)
        
        if visa_name == '':
            data['msg'] = "Please enter a visa  name"
            data['type'] = "error"
            return JsonResponse(data)
        
        if visa_number == '' or visa_number == '0' or visa_number == None:
            data['msg'] = "Please enter a visa  number"
            data['type'] = "error"
            return JsonResponse(data)
        
        # if expire_date == '' or expire_date == None or expire_date == '0':
        #     data['msg'] = "Please enter an expire date"
        #     data ['error'] = "error"
        #     return JsonResponse(data)
        
        if bank == '':
            data['msg'] = "Please select a bank"
            data['type'] = "error"
            return JsonResponse(data)
        
        if bank_account == '':
            data['msg'] = "Please select a bank account"
            data['type'] = "error"
            return JsonResponse(data) 
        
        if not form.is_valid():
            msg = [
                (key +' Error:', value[0]['message']) for key, value in (
                    form.errors.get_json_data().items()
                )
            ]
            data['visa_id'] = id
            data['msg'] = msg
            data['type'] = 'error'    
            return JsonResponse(data)
        
        if form.is_valid():
            save_form = form.save(commit=False)
            save_form.updated_user = request.user
            save_form.save()
            msg = ('Visa with name "%s" saved successfully' % (save_form.visa_name))
            
            data['visa_id'] = id 
            data['msg'] = msg
            data['type'] = 'success'
            return JsonResponse(data)
        else:
            form = CreateVisaForm()
            
        
        #?trial for validating if visa number changed expire date should change
    # if visa_number and expire_date:
    #     # Check if visa number is changed and expire date is not changed
    #     existing_visa = CreateVisa.objects.filter(visa_no=visa_number).exclude(id=qs.instance.id).first()
    #     if existing_visa and existing_visa.expire_date == expire_date:
    #         data['msg']='If visa number is changed, expire date should also change.'
    # return JsonResponse(data)

    visa_code = 'visa-' + str(id)
    context = {
        'form': form,
        'qs': qs,
        'visa_code':visa_code,
        'title': 'Edit Visa'
    }
    return render(request, 'management/create_visa/edit_visa.html', context)




def create_ajax_visa_message(request):
    data = {}
    data['visa_id'] = None 
    data['error'] = 'ERROR !!!'
    data['type'] = 'error'
    if request.is_ajax() and request.method == "POST":
        form = CreateVisaForm(request.POST or None)
        visa_name = request.POST.get("visa_name") 
        match = CreateVisa.objects.select_related('user').filter(name=visa_name).exists()
        if not match:
            if form.is_valid():

                save_form = form.save(commit=False)
                save_form.name = visa_name
                save_form.user = request.user
                save_form.updated_user = request.user
                
                save_form.save()
                error = ('Visa with name "%s" saved successfully' % (save_form.visa_name))
                data['visa_id'] = save_form.id 
                data['error'] = error
                data['type'] = 'success'
            else:
                for f in form:
                    print('error from is not valid: ', f.name, f.errors)
                data['error'] = 'error from is not valid'
        else:
            print('name already exists and we must deal with it ...')
            error = ('Visa with name "%s" already exists !!!' % (save_form.visa_name))
            data['visa_id'] = None
            data['error'] = error
            data['type'] = 'error'
    else:
        form = CreateVisaForm()

    return JsonResponse(data)



def visa_table(request):
    table_qs = CreateVisa.objects.select_related('user').filter(is_deleted=False, active=True).order_by('-id')
    deleted_qs = CreateVisa.objects.select_related('user').filter(is_deleted=True,).order_by('-id')
    inactive_qs = CreateVisa.objects.select_related('user').filter(is_deleted=False, active=False).order_by('-id')
    combined_qs = list(chain(table_qs, inactive_qs))
    main_qs = CreateVisa.objects.select_related('user').only().filter().order_by('-id')
    
    table_total = table_qs.count()
    deleted_total = deleted_qs.count()
    inactive_total = inactive_qs.count()
    main_total = main_qs.count()
    context = {
        'table_qs': table_qs,
        'title': 'Visa',
        'inactive_qs': inactive_qs,
        'deleted_qs': deleted_qs,
        'combined_qs':combined_qs,
        'main_qs':main_qs,
        
        'table_total':table_total,
        'deleted_total':deleted_total,
        'inactive_total':inactive_total,
        'main_total':main_total,
    }
    return render(request, 'management/create_visa/visa_table.html', context)