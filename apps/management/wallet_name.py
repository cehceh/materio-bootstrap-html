from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from itertools import chain

from .models import WalletName
from .forms import WalletNameForm
from posapp.utils import model_id_restriction
def add_wallet_name(request):
    data = {}
    data['wallet_name_id'] = None 
    data['error'] = 'ERROR !!!'
    data['type'] = 'error'
    if request.accepts('*/*') and request.method == "POST":
        form = WalletNameForm(
            request.POST or None, 
        )
        
        for f in form:
            print(
                f.name,
                f.errors
            )
            if not f.errors:
                print('No errors, from is valid and : ', request.accepts('*/*'), request.method)
        
        wallet_name = request.POST.get("name") 
        print(
            'wallet_name**', wallet_name,
        )
        if not form.is_valid():
            data['wallet_name_id'] = None 
            msg = [
                ('Wallet ' + key+' Error:', value[0]['message']) for key, value in (
                    form.errors.get_json_data().items()
                )
            ]
            data['error'] = msg
            data['type'] = 'error'    
            return JsonResponse(data)
        
        if form.is_valid():
            save_form = form.save(commit=False)
            # save_form.full_name = full_name
            save_form.user = request.user
            save_form.updated_user = request.user
            
            
            save_form.save()
            
            #?Esraa
            #UPDATING THE CODE FIELD
            WalletName.objects.filter(id=save_form.id).update(code='walname-'+str(save_form.id))

            msg = ('Wallet with name "%s" saved successfully' % (wallet_name))
            
            data['wallet_name_id'] = save_form.id 
            data['wallet_name'] = save_form.name 
            #data['code'] = "branch-" + str(save_form.id)
            data['error'] = msg
            data['type'] = 'success'
            return JsonResponse(data)
        
    else:
        form = WalletNameForm()

    context = {
        'form': form,
        'title': 'Create Wallet Name'
    }
    return render(request, 'management/wallet_name/add_wallet_name.html', context)


# @model_id_restriction(app_name='management', model_name='WalletName')
def edit_wallet_name(request, id):
    data = {}
    # data['branches_id'] = id 
    # data['error'] = 'ERROR !!!'
    # data['type'] = 'error'
    
    
    qs = WalletName.objects.select_related('user').get(id=id)
    form = WalletNameForm(
        request.POST or None,
        request.FILES or None, 
        instance=qs,
    )

    for f in form:
        print(
            f.name,
            f.errors
        )
        if not f.errors:
            print('No errors, from is valid and : ', request.accepts("*/*"), request.method)
    
    if request.accepts('*/*') and request.method == "POST":
        wallet_name = request.POST.get("name") 
        
        if not form.is_valid():
            msg = [
                (key +' Error:', value[0]['message']) for key, value in (
                    form.errors.get_json_data().items()
                )
            ]
            data['wallet_name_id'] = id
            data['error'] = msg
            data['type'] = 'error'    
            return JsonResponse(data)
        
        if form.is_valid():

            save_form = form.save(commit=False)
            save_form.updated_user = request.user
            save_form.code = 'walname-' + str(id)
            print("EDIT-CODE-----",save_form.code)
            save_form.save()
            # save_form.code = 'branch-' + str(id)
            error = ('Wallet with name "%s" saved successfully' % (wallet_name))
            
            data['wallet_name_id'] = id 
            data['error'] = error
            data['type'] = 'success'
            return JsonResponse(data)
        # else:
            # form = BranchForm()
    branch_code = 'walname-' + str(id)
    context = {
        'form': form,
        'qs': qs,
        'wallet_code' : branch_code,
        'title': 'Edit Wallet Name'
    }
    return render(request, 'management/wallet_name/edit_wallet_name.html', context)




def create_ajax_wallet_message(request):
    data = {}
    data['wallet_name_id'] = None 
    data['error'] = 'ERROR !!!'
    data['type'] = 'error'
    if request.is_ajax() and request.method == "POST":
        form = WalletNameForm(request.POST or None)
        wallet_name = request.POST.get("wallet_name") 
        match = WalletName.objects.select_related('user').filter(name=wallet_name).exists()
        if not match:
            if form.is_valid():

                save_form = form.save(commit=False)
                save_form.name = wallet_name
                save_form.user = request.user
                save_form.updated_user = request.user
                
                save_form.save()
                error = ('Wallet with name "%s" saved successfully' % (wallet_name))
                data['wallet_name_id'] = save_form.id 
                data['error'] = error
                data['type'] = 'success'
            else:
                for f in form:
                    print('error from is not valid: ', f.name, f.errors)
                data['error'] = 'error from is not valid'
        else:
            print('name already exists and we must deal with it ...')
            error = ('Wallet with name "%s" already exists !!!' % (wallet_name))
            data['wallet_name_id'] = None
            data['error'] = error
            data['type'] = 'error'
    else:
        form = WalletNameForm()

    return JsonResponse(data)



def wallet_name_table(request):
    # table_qs = Branches.objects.select_related('user').only().order_by('-id')
    #?--Esraa--
    active_qs = WalletName.objects.select_related('user').filter(is_deleted=False, active=True).order_by('-id')
    inactive_qs = WalletName.objects.select_related('user').filter(is_deleted=False, active=False).order_by('-id')
    deleted_qs = WalletName.objects.select_related('user').filter(is_deleted=True).order_by('-id')
    main_qs = WalletName.objects.select_related('user').filter(is_deleted=False).order_by('-id')
    table_qs = WalletName.objects.select_related('user').filter(is_deleted=False , active=True).order_by('-id')
    combined_qs = list(chain(table_qs, inactive_qs))
    
    active_total = active_qs.count()
    inactive_total = inactive_qs.count()
    deleted_total = deleted_qs.count()
    table_total = main_qs.count()

    context = {
        'table_qs': table_qs,
        'title': 'Wallets',
        'active_qs' : active_qs,
        'inactive_qs': inactive_qs,
        'inactive_total': inactive_total,
        'active_total': active_total,
        'deleted_total': deleted_total,
        'table_total' :table_total,
        'deleted_qs': deleted_qs,
        'main_qs': main_qs,
        'combined_qs': combined_qs,

    }
    return render(request, 'management/wallet_name/wallet_name_table.html', context)