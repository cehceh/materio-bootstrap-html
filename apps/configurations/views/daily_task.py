from decimal import Decimal
from django.apps import apps
from django.shortcuts import render
from django.http import JsonResponse
from django.db import transaction

from apps.configurations.models.daily_task_model import DailyTaskUOM, DailyTaskUnitPurchase, DailyTaskUnitSale
from apps.configurations.models.conf_models import UnitNames

from ..models import DailyTask
from ..forms import DailyTaskForm, DailyTaskUOMForm
from config.utils import pass_query

def add_daily_task(request):
    data = {}
    data['daily_task_id'] = None 
    if request.accepts('*/*') and request.method == "POST":
        form = DailyTaskForm(
            request.POST or None, 
        )
        active = request.POST.get("active")
        
        print("ACTIVE@@@************", active)
        
        for f in form:
            print(
                f.name,
                f.errors
            )
            if not f.errors:
                print('No errors, from is valid and : ', request.accepts('*/*'), request.method)
        
        daily_task_name = request.POST.get("name") 
        print(
            'daily_task_name**', daily_task_name,
        )
        if not form.is_valid():
            data['daily_task_id'] = None 
            msg = [
                (key+' Error:', value[0]['message']) for key, value in (
                    form.errors.get_json_data().items()
                )
            ]
            data['error'] = msg
            data['type'] = 'error'    
            return JsonResponse(data)
        
        if form.is_valid():
            save_form = form.save(commit=False)
            save_form.user = request.user
            save_form.updated_user = request.user
            save_form.active = True
            save_form.save()
            
            DailyTask.objects.filter(id=save_form.id).update(code='dailytask-'+str(save_form.id))
            
            msg = ('Daily Task with name "%s" saved successfully' % (daily_task_name))
            data['daily_task_id'] = save_form.id 
            data['daily_task_name'] = save_form.name 
            data['error'] = msg
            data['type'] = 'success'
            return JsonResponse(data)
        
    else:
        form = DailyTaskForm()

    context = {
        'form': form,
        'title': 'Create Daily Task'
    }
    return render(request, 'configurations/daily_task/add_daily_task.html', context)



def edit_daily_task(request, id):
    data = {}
    data['daily_task_id'] = id 
    
    
    qs = DailyTask.objects.select_related('user').get(id=id)
    form = DailyTaskForm(
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
        daily_task_name = request.POST.get("name") 
        
        if not form.is_valid():
            msg = [
                (key +' Error:', value[0]['message']) for key, value in (
                    form.errors.get_json_data().items()
                )
            ]
            data['daily_task_id'] = id
            data['error'] = msg
            data['type'] = 'error'    
            return JsonResponse(data)
        if form.is_valid():

            save_form = form.save(commit=False)
            save_form.updated_user = request.user
            
            save_form.save()
            msg = ('Work Type with name "%s" saved successfully' % (daily_task_name))
            
            data['daily_task_id'] = id 
            data['error'] = msg
            data['type'] = 'success'
            return JsonResponse(data)
        else:
            form = DailyTaskForm()


    daily_task_code = 'dailytask-' + str(id)

    context = {
        'form': form,
        'qs': qs,
        "dailytask_code" : daily_task_code,
        'title': 'Edit Daily Task'
    }
    return render(request, 'configurations/daily_task/edit_daily_task.html', context)




def create_ajax_daily_task_message(request):
    data = {}
    data['daily_task_id'] = None 
    data['error'] = 'ERROR !!!'
    data['type'] = 'error'
    if request.is_ajax() and request.method == "POST":
        form = DailyTaskForm(request.POST or None)
        daily_task_name = request.POST.get("daily_task_name") 
        match = DailyTask.objects.select_related('user').filter(name=daily_task_name).exists()
        if not match:
            if form.is_valid():

                save_form = form.save(commit=False)
                save_form.name = daily_task_name
                save_form.user = request.user
                save_form.updated_user = request.user
                
                save_form.save()
                msg = ('Work Type with name "%s" saved successfully' % (daily_task_name))
                data['daily_task_id'] = save_form.id 
                data['error'] = msg
                data['type'] = 'success'
            else:
                for f in form:
                    print('error from is not valid: ', f.name, f.errors)
                data['error'] = 'error from is not valid'
        else:
            print('name already exists and we must deal with it ...')
            error = ('daily_task with name "%s" already exists !!!' % (daily_task_name))
            data['daily_task_id'] = None
            data['error'] = error
            data['type'] = 'error'
    else:
        form = DailyTaskForm()

    return JsonResponse(data)



def daily_task_table(request):
    show_log = request.GET.get("show-log")
    show_deleted = request.GET.get("show-deleted")
    in_active = request.GET.get("in-active")
    is_active = request.GET.get("is-active")
    show_main = request.GET.get('show-main')
    print(
        "show_log===",show_log,
        "show_deleted===",show_deleted,
        "in_active===",in_active,
        "active===",is_active,
        "show_main===",show_main
    )
    data = {}
    main = []
    log = []
    active = []
    inactive = []
    delete = []
    if show_main == 'true':
        main = DailyTask.objects.values(
                    'id', 
                    'code',
                    'name',
                ).filter(is_deleted=False).order_by('-id') 
        
        unit = [{'unit_exists': DailyTaskUOM.objects.filter(daily_task_id=obj['id']).exists()} for obj in main]

        mainList = [obj for obj in main]
        # data['unit-exists'] = [obj for obj in unit]
        data['main-list']  = [{**obj,**un} for obj , un in zip (mainList , unit)]
        print("data['main-list'] ***", data['main-list'], 'main.query******>', main.query,'unit',unit)
        return JsonResponse(data, safe=False) 
    elif show_log == 'true':
        log = DailyTask.objects.select_related('user').only().values(
                    'id', 
                    'code',
                    'name',
                    'created_at',
                    'updated_at',
                    'updated_user__username',
                    'user__username',
                    
                ).filter(is_deleted=False).order_by('-id') 
        
        # inactive = []
        data['log-list'] = [obj for obj in log]
        print("data['log-list'] ***", data['log-list'], 'log.query******>', log.query)
        return JsonResponse(data, safe=False)
    elif in_active == 'true':
        inactive = DailyTask.objects.values(
                    'id', 
                    'code',
                    'name',
                    
                ).filter(is_deleted=False,active=False).order_by('-id') 

        data['inactive-list'] = [obj for obj in inactive]
        print("data['inactive-list'] ***", data['inactive-list'], 'inactive.query******>', inactive.query)
        return JsonResponse(data, safe=False)
    elif is_active == 'true':
        active = DailyTask.objects.values(
                    'id', 
                    'code',
                    'name',
                    
                ).filter(is_deleted=False,active=True).order_by('-id') 

        data['active-list'] = [obj for obj in active]
        print("data['active-list'] ***", data['active-list'], 'active.query******>', active.query)
        return JsonResponse(data, safe=False)
    elif show_deleted == 'true':
        delete = DailyTask.objects.values(
                    'id', 
                    'code',
                    'name',

                    
                ).filter(is_deleted=True).order_by('-id') 
        
        data['delete-list'] = [obj for obj in delete]
        print("data['delete-list'] ***", data['delete-list'], 'delete.query******>', delete.query)
        return JsonResponse(data, safe=False)

    inactive_total = DailyTask.objects.select_related('user').values('id').filter(is_deleted=False, active=False).count()
    deleted_total = DailyTask.objects.select_related('user').values('id').filter(is_deleted=True).count()
    main_log_total = DailyTask.objects.select_related('user').values('id').filter(is_deleted=False).count()
    active_total = DailyTask.objects.select_related('user').values('id').filter(is_deleted=False,active=True).count()
    context = {
        'title': 'Daily Tasks',
        'inactive_total':inactive_total,
        'deleted_total':deleted_total,
        'main_log_total':main_log_total,
        'active_total':active_total,
    }
    return render(request, 'configurations/daily_task/daily_task_table.html', context)

def unit_pricing_add(request, id):
    data = {}
    app_name = 'configurations'
    model_name = 'DailyTaskUOM'
    cls = apps.get_model(app_name, model_name)
    product_unit = cls.objects.select_related(
        'daily_task'
    ).filter(id=id).order_by('id')
    uoms = []
    # print('VALUES******', [obj 
    #                        for obj in 
    #                        UOM.objects.values_list('unit__name', flat=True).filter(id=id)])
    
    if DailyTaskUOM.objects.exists():
        uom = DailyTaskUOM.objects.select_related(
            'daily_task').filter(
                id=id
                ).order_by('id')
        uom_obj = [
            DailyTaskUOM.objects.select_related('daily_task').get(id=obj.id) for obj in uom
        ]
        
    else:
        uom = []
        uom_obj =[]
        # last_unit = None
     #? the next lines for passing through context  
    uom_ids = [obj.id for obj in uom]
    unit_purchase = DailyTaskUnitPurchase.objects.filter(uom_id__in=uom_ids)
    unit_purchase_IDS = [obj.uom_id for obj in unit_purchase]   
    
    unit_sale = DailyTaskUnitSale.objects.filter(uom_id__in=uom_ids)
    unit_sale_IDS = [obj.uom_id for obj in unit_sale]
    #*# for editing UOM form
    edit_uom_form = [
        DailyTaskUOMForm(
            request.POST or None,
            instance=obj,
            initial={
                'unit':obj.unit, #['unit__name'],
            }
        ) for obj in uom_obj
    ] 
    existing_uoms = DailyTaskUOM.objects.values('id').filter(daily_task_id=id).exists()

    
    
    # showUOM = request.GET.get('show-uom')
    # print("showUOM",showUOM)
    # showPurchase = request.GET.get('show-purchase')
    # print("showPurchase",showPurchase)
    # showSale = request.GET.get('show-sale')
    # print("showSale",showSale)
    
    if request.accepts('*/*') and request.method == "POST":
        
        uom_form = DailyTaskUOMForm(
        request.POST or None,
        prefix="uom"
        )

        #* The next line give a right list from ajax request
        uom_options_list = request.POST.getlist('uom_options_list', [])
        main_uom_list = request.POST.getlist('main_uom_list', [])
        unit_list = request.POST.getlist('unit_list', [])
        value_list = request.POST.getlist('value_list', [])
        uom_unit_list = request.POST.getlist('uom_unit_list', [])
        uom_value_list = request.POST.getlist('uom_value_list', [])
        unit_price_list = request.POST.getlist('unit_price_list', [])
        unit_conversion_list = request.POST.getlist('unit_conversion_list', [])
        print(
            'unit_list: ', unit_list, 
            'uom_check_list:', main_uom_list,     
            'option_list: ', uom_options_list,
            'value_list: ', value_list,
            'unit_label_list: ', uom_unit_list,
            'uom_value_list: ', uom_value_list,
            'unit_price_list: ', unit_price_list,   
        )
        
        if not uom_form.is_valid():

            msg = [
                (key, value[0]['message']) for key, value in (
                    uom_form.errors.get_json_data().items()
                )
            ]
            data['error'] = msg
            data['type'] = 'error'
            return JsonResponse(data)
        #* check for UOM form
        check_option_list = [True for obj in uom_options_list if obj == 'main']
        if existing_uoms == False :
            if uom_options_list == [] or unit_list == [] or value_list == []:
                data['pro_id'] = None 
                data['error'] = ' UOM data must be filled ...'
                data['type'] = 'error'
                return JsonResponse(data)
            
            if '' in value_list:
                data['pro_id'] = None 
                data['error'] = 'Enter correct UOM data or fill empty inputs ...'
                data['type'] = 'error'
                return JsonResponse(data)
            
            if '' in uom_options_list:
                data['pro_id'] = None 
                data['error'] = 'Enter correct UOM data or fill empty inputs ...'
                data['type'] = 'error'
                return JsonResponse(data)
            
            if '' in unit_list:
                data['pro_id'] = None 
                data['error'] = 'Enter correct UOM data or fill empty inputs ...'
                data['type'] = 'error'
                return JsonResponse(data)
            
            check_value_list = [
                True for i in value_list 
                    if (i.startswith('-')) or (Decimal(i).is_zero())
            ]
            # zero_in_value_list = [True for i in value_list if int(Decimal(i)) == 0]
            # or Decimal(i).is_zero()
            # print('check_value_list', check_value_list)
            if True in check_value_list: # or True in check_value_list:
                data['pro_id'] = None 
                data['error'] = 'Unit values must not be negative or zero...'
                data['type'] = 'error'
                return JsonResponse(data)
            
        

        
        if existing_uoms == True :
            # check_new_unit_list = [True for obj in unit_list if obj in unit_list]
            
            
            # Convert the list to a set to remove duplicates
            unique_values = set(unit_list)

            # Compare the lengths of the original list and the set
            if len(unit_list) != len(unique_values):
            #     print("Duplicates found")
            # else:
            #     print("No duplicates found")
            # if True in check_new_unit_list:
                data['pro_id'] = None 
                data['error'] = 'One or more unit is duplicated please review your new units added'
                data['type'] = 'info'
                return JsonResponse(data)
            
            negative_value_list = [
                True for i in value_list if (i.startswith('-'))
            ]
            if value_list != ['']:
                zero_value_list = [
                    True for i in value_list if ((Decimal(i)).is_zero())
                ]
            else:
                zero_value_list = []
            # zero_in_value_list = [True for i in value_list if int(Decimal(i)) == 0]
            # or Decimal(i).is_zero()
            # print('check_value_list', negative_value_list)
            if True in negative_value_list: # or True in check_value_list:
                data['pro_id'] = None 
                data['error'] = 'Unit values must not be negative...'
                data['type'] = 'info'
                return JsonResponse(data)
            
            if True in zero_value_list: # or True in check_value_list:
                data['pro_id'] = None 
                data['error'] = 'Unit values must not be zero...'
                data['type'] = 'info'
                return JsonResponse(data)
            
            negative_edit_value_list = [
                True for i in value_list if (i.startswith('-') or Decimal(i).is_zero())
            ]
            if True in negative_edit_value_list:
                # data['pro_id'] = None 
                data['error'] = 'Unit values must not be negative or zero !!! here1'
                data['type'] = 'info'
                return JsonResponse(data)
            
            # if uom_value_list == [''] or uom_value_list == []:
            #     data['error'] = 'Unit values must not be empty !!!'
            #     data['type'] = 'info'
            #     return JsonResponse(data)
            
            if '0' in uom_value_list or '0.0' in uom_value_list:
                data['error'] = 'Unit values must not be have zero values !!! - here 2'
                data['type'] = 'info'
                return JsonResponse(data)
            
            negative_uom_value_list = [
                True for i in uom_value_list if (i.startswith('-') or Decimal(i).is_zero())
            ]
            if True in negative_uom_value_list:
                # data['pro_id'] = None 
                data['error'] = 'Unit values must not be negative or zero !!!- here3'
                data['type'] = 'info'
                return JsonResponse(data)

        with transaction.atomic():
            # print(
            #     'UOM-FORM-VALIDITY:::', uom_form.is_valid(), 
            # )
            existing_uoms = DailyTaskUOM.objects.filter(daily_task_id=id).exists()

                #* the next code for saving model with multiple rows 
            if uom_form.is_valid():
                if existing_uoms == True :
                    uoms = DailyTaskUOM.objects.only().filter(id=id)
                    print("uoms",uoms)
                    uom_obj = [
                        DailyTaskUOM.objects.create(
                            id=id,
                            uom_options= opt,
                            main_uom=True if opt == 'main' else False,
                            unit_id= int(un),
                            value=(Decimal(val)),
                            uom_value=(Decimal(uom_val)),
                            uom_unit=uom_unit,
                            unit_conversion=Decimal(conv_val),
                            unit_price=(Decimal(price))
                        ) for opt, un, val, uom_val, uom_unit, conv_val, price in zip(
                                uom_options_list, unit_list, value_list,
                                uom_value_list, uom_unit_list, unit_conversion_list, unit_price_list
                            )
                    ]
                    data['pro_id'] = id 
                    
                    data['error'] = 'UOM saved successfully HERE22 ...'
                    data['type'] = 'success'
                    return JsonResponse(data)
                else :

                    uom_obj = [
                        DailyTaskUOM.objects.create(
                            id=id,
                            uom_options= opt,
                            main_uom=True if opt == 'main' else False,
                            unit_id= int(un),
                            value=(Decimal(val)),
                            uom_value=(Decimal(uom_val)),
                            uom_unit=uom_unit,
                            unit_conversion=Decimal(conv_val),
                            unit_price=(Decimal(price))
                        ) for opt, un, val, uom_val, uom_unit, conv_val, price in zip(
                                uom_options_list, unit_list, value_list,
                                uom_value_list, uom_unit_list, unit_conversion_list, unit_price_list
                            )
                    ]
                    data['pro_id'] = id
                    
                    data['error'] = 'UOM saved successfully here ...'
                    data['type'] = 'success'
                    return JsonResponse(data)
           
            
            # if uom_form.is_valid():
                #* important note here we are in the (not match_name) case 
                #* toast message will appear after all forms validity checks


    else:
        uom_form = DailyTaskUOMForm(prefix="uom")

    context = {
        'qs': product_unit,
        'id': id,
        "uom_form": uom_form,
        "edit_uom_form":edit_uom_form,
        "existing_uoms":existing_uoms,
        "uom":uom,
        'uom_obj':uom_obj,
        'unit_purchase': unit_purchase,
        'unit_purchase_ids': unit_purchase_IDS,
        'unit_sale': unit_sale,
        'unit_sale_ids': unit_sale_IDS,
        # 'unit_id': get_unit_id,
        "title":"Create Units and Price"
    }
    return pass_query(
        request=request,
        template_path='configurations/daily_task/unit_pricing/unit_pricing_add.html',
        context=context,
        app_name=app_name, 
        model_name=model_name,
    )

def unit_pricing(request, id):
    # from .helper import convert_unit
    data = {}
    app_name = 'configurations'
    model_name = 'DailyTaskUOM'
    cls = apps.get_model(app_name, model_name)
    product_unit = cls.objects.select_related(
        'daily_task'
    ).filter(id=id).order_by('id')
    uoms = []
    # print('VALUES******', [obj 
    #                        for obj in 
    #                        UOM.objects.values_list('unit__name', flat=True).filter(id=id)])
    
    if DailyTaskUOM.objects.exists():
        uom = DailyTaskUOM.objects.select_related(
            'daily_task').filter(
                daily_task_id=id
                ).order_by('id')
        uom_obj = [
            DailyTaskUOM.objects.select_related('daily_task').get(id=obj.id) for obj in uom
        ]
    else:
        uom = []
        uom_obj =[]
        # last_unit = None
     #? the next lines for passing through context  
    uom_ids = [obj.id for obj in uom]
    unit_purchase = DailyTaskUnitPurchase.objects.filter(uom_id__in=uom_ids)
    unit_purchase_IDS = [obj.uom_id for obj in unit_purchase]   
    
    unit_sale = DailyTaskUnitSale.objects.filter(uom_id__in=uom_ids)
    unit_sale_IDS = [obj.uom_id for obj in unit_sale]
    #*# for editing UOM form
    edit_uom_form = [
        DailyTaskUOMForm(
            request.POST or None,
            instance=obj,
            initial={
                'unit':obj.unit, #['unit__name'],
            }
        ) for obj in uom_obj
    ] 
    existing_uoms = DailyTaskUOM.objects.values('id').filter(daily_task_id=id).exists()
    
    
    # showUOM = request.GET.get('show-uom')
    # print("showUOM",showUOM)
    # showPurchase = request.GET.get('show-purchase')
    # print("showPurchase",showPurchase)
    # showSale = request.GET.get('show-sale')
    # print("showSale",showSale)
    
    if request.accepts('*/*') and request.method == "POST":
        
        uom_form = DailyTaskUOMForm(
        request.POST or None,
        prefix="uom"
        )

        #* The next line give a right list from ajax request
        uom_options_list = request.POST.getlist('uom_options_list', [])
        main_uom_list = request.POST.getlist('main_uom_list', [])
        unit_list = request.POST.getlist('unit_list', [])
        value_list = request.POST.getlist('value_list', [])
        uom_unit_list = request.POST.getlist('uom_unit_list', [])
        uom_value_list = request.POST.getlist('uom_value_list', [])
        unit_price_list = request.POST.getlist('unit_price_list', [])
        unit_conversion_list = request.POST.getlist('unit_conversion_list', [])
        # print(
        #     'unit_list: ', unit_list, 
        #     'uom_check_list:', main_uom_list,     
        #     'option_list: ', uom_options_list,
        #     'value_list: ', value_list,
        #     'unit_label_list: ', uom_unit_list,
        #     'uom_value_list: ', uom_value_list,
        #     'unit_price_list: ', unit_price_list,   
        # )
        
        if not uom_form.is_valid():

            msg = [
                (key, value[0]['message']) for key, value in (
                    uom_form.errors.get_json_data().items()
                )
            ]
            data['error'] = msg
            data['type'] = 'error'
            return JsonResponse(data)
        #* check for UOM form
        check_option_list = [True for obj in uom_options_list if obj == 'main']
        if existing_uoms == False :
            if uom_options_list == [] or unit_list == [] or value_list == []:
                data['pro_id'] = None 
                data['error'] = ' UOM data must be filled ...'
                data['type'] = 'error'
                return JsonResponse(data)
            
            if '' in value_list:
                data['pro_id'] = None 
                data['error'] = 'Enter correct UOM data or fill empty inputs ...'
                data['type'] = 'error'
                return JsonResponse(data)
            
            if '' in uom_options_list:
                data['pro_id'] = None 
                data['error'] = 'Enter correct UOM data or fill empty inputs ...'
                data['type'] = 'error'
                return JsonResponse(data)
            
            if '' in unit_list:
                data['pro_id'] = None 
                data['error'] = 'Enter correct UOM data or fill empty inputs ...'
                data['type'] = 'error'
                return JsonResponse(data)
            
            check_value_list = [
                True for i in value_list 
                    if (i.startswith('-')) or (Decimal(i).is_zero())
            ]
            # zero_in_value_list = [True for i in value_list if int(Decimal(i)) == 0]
            # or Decimal(i).is_zero()
            # print('check_value_list', check_value_list)
            if True in check_value_list: # or True in check_value_list:
                data['pro_id'] = None 
                data['error'] = 'Unit values must not be negative or zero...'
                data['type'] = 'error'
                return JsonResponse(data)
            
        

        
        if existing_uoms == True :
            # check_new_unit_list = [True for obj in unit_list if obj in unit_list]
            
            
            # Convert the list to a set to remove duplicates
            unique_values = set(unit_list)

            # Compare the lengths of the original list and the set
            if len(unit_list) != len(unique_values):
            #     print("Duplicates found")
            # else:
            #     print("No duplicates found")
            # if True in check_new_unit_list:
                data['pro_id'] = None 
                data['error'] = 'One or more unit is duplicated please review your new units added'
                data['type'] = 'info'
                return JsonResponse(data)
            
            negative_value_list = [
                True for i in value_list if (i.startswith('-'))
            ]
            if value_list != ['']:
                zero_value_list = [
                    True for i in value_list if ((Decimal(i)).is_zero())
                ]
            else:
                zero_value_list = []
            # zero_in_value_list = [True for i in value_list if int(Decimal(i)) == 0]
            # or Decimal(i).is_zero()
            # print('check_value_list', negative_value_list)
            if True in negative_value_list: # or True in check_value_list:
                data['pro_id'] = None 
                data['error'] = 'Unit values must not be negative...'
                data['type'] = 'info'
                return JsonResponse(data)
            
            if True in zero_value_list: # or True in check_value_list:
                data['pro_id'] = None 
                data['error'] = 'Unit values must not be zero...'
                data['type'] = 'info'
                return JsonResponse(data)
            
            negative_edit_value_list = [
                True for i in value_list if (i.startswith('-') or Decimal(i).is_zero())
            ]
            if True in negative_edit_value_list:
                # data['pro_id'] = None 
                data['error'] = 'Unit values must not be negative or zero !!! here1'
                data['type'] = 'info'
                return JsonResponse(data)
            
            # if uom_value_list == [''] or uom_value_list == []:
            #     data['error'] = 'Unit values must not be empty !!!'
            #     data['type'] = 'info'
            #     return JsonResponse(data)
            
            if '0' in uom_value_list or '0.0' in uom_value_list:
                data['error'] = 'Unit values must not be have zero values !!! - here 2'
                data['type'] = 'info'
                return JsonResponse(data)
            
            negative_uom_value_list = [
                True for i in uom_value_list if (i.startswith('-') or Decimal(i).is_zero())
            ]
            if True in negative_uom_value_list:
                # data['pro_id'] = None 
                data['error'] = 'Unit values must not be negative or zero !!!- here3'
                data['type'] = 'info'
                return JsonResponse(data)

        with transaction.atomic():
            # print(
            #     'UOM-FORM-VALIDITY:::', uom_form.is_valid(), 
            # )
            existing_uoms = DailyTaskUOM.objects.filter(daily_task_id=id).exists()

                #* the next code for saving model with multiple rows 
            if uom_form.is_valid():
                if existing_uoms == True :
                    uoms = DailyTaskUOM.objects.only().filter(daily_task_id=id)
                    print("uoms",uoms)
                    uom_obj = [
                        DailyTaskUOM.objects.create(
                            daily_task_id=id,
                            uom_options= opt,
                            main_uom=True if opt == 'main' else False,
                            unit_id= int(un),
                            value=(Decimal(val)),
                            uom_value=(Decimal(uom_val)),
                            uom_unit=uom_unit,
                            unit_conversion=Decimal(conv_val),
                            unit_price=(Decimal(price))
                        ) for opt, un, val, uom_val, uom_unit, conv_val, price in zip(
                                uom_options_list, unit_list, value_list,
                                uom_value_list, uom_unit_list, unit_conversion_list, unit_price_list
                            )
                    ]
                    data['pro_id'] = id 
                    
                    data['error'] = 'UOM saved successfully HERE22 ...'
                    data['type'] = 'success'
                    return JsonResponse(data)
                else :

                    uom_obj = [
                        DailyTaskUOM.objects.create(
                            daily_task_id=id,
                            uom_options= opt,
                            main_uom=True if opt == 'main' else False,
                            unit_id= int(un),
                            value=(Decimal(val)),
                            uom_value=(Decimal(uom_val)),
                            uom_unit=uom_unit,
                            unit_conversion=Decimal(conv_val),
                            unit_price=(Decimal(price))
                        ) for opt, un, val, uom_val, uom_unit, conv_val, price in zip(
                                uom_options_list, unit_list, value_list,
                                uom_value_list, uom_unit_list, unit_conversion_list, unit_price_list
                            )
                    ]
                    data['pro_id'] = id
                    
                    data['error'] = 'UOM saved successfully here ...'
                    data['type'] = 'success'
                    return JsonResponse(data)
           
            
            # if uom_form.is_valid():
                #* important note here we are in the (not match_name) case 
                #* toast message will appear after all forms validity checks


    else:
        uom_form = DailyTaskUOMForm(prefix="uom")

    context = {
        'qs': product_unit,
        'id': id,
        "uom_form": uom_form,
        "edit_uom_form":edit_uom_form,
        "existing_uoms":existing_uoms,
        "uom":uom,
        'uom_obj':uom_obj,
        'unit_purchase': unit_purchase,
        'unit_purchase_ids': unit_purchase_IDS,
        'unit_sale': unit_sale,
        'unit_sale_ids': unit_sale_IDS,
        # 'unit_id': get_unit_id,
        "title":"Create Units and Price"
    }
    return pass_query(
        request=request,
        template_path='configurations/daily_task/unit_pricing/unit_pricing_edit.html',
        context=context,
        app_name=app_name, 
        model_name=model_name,
    )
    # return render(request, '', context)
    
    
def add_uom_sale(request, id):
    data = {}
    value_list = request.GET.getlist('value-list[]')
    percentage_list = request.GET.getlist('percentage-list[]')
    
    product_price_list = request.GET.getlist('price-list[]')
    uom_id_list = request.GET.getlist('uom-id-list[]')
    
    uom = DailyTaskUOM.objects.select_related(
        'daily_task').filter(
            daily_task_id=id
            ).order_by('id')
        
    uom_ids = [obj.id for obj in uom]
    unit_sale = DailyTaskUnitSale.objects.filter(uom_id__in=uom_ids).order_by('uom_id')
    unit_sale_IDS = [obj.uom_id for obj in unit_sale]
    
    origin_data = [(obj.uom_id, obj.unit_price) for obj in unit_sale]
    
    old_uom_id = [
        (obj, val, percent, pr) for obj, val, percent, pr in zip(
            uom_id_list, value_list, percentage_list, product_price_list
            ) if int(obj) in unit_sale_IDS 
    ]
    new_uom_id = [
        (obj, val, percent, pr) for obj, val, percent, pr in zip(
            uom_id_list, value_list, percentage_list, product_price_list
            ) if int(obj) not in unit_sale_IDS
    ]
    
    int_uom_id_list = [int(obj) for obj in uom_id_list]

    print(
        '***old_uom_id***', old_uom_id, [(old_uom_id.remove(obj) if obj == False else obj) for obj in old_uom_id],
        '***NEW_uom_id***', new_uom_id, [new_uom_id.remove(obj) for obj in new_uom_id if obj == False] ,
        # [(new_uom_id.remove(obj) if obj == False else obj) for obj in new_uom_id],
        '**uom_id_list**', uom_id_list,
        '*##unit_SALE_IDS***', unit_sale_IDS, 
        unit_sale, '**uom_id_list==unit_SALE_IDS**', 
        [True if obj in int_uom_id_list else False for obj in unit_sale_IDS], int_uom_id_list,
        '**origin_data**', origin_data
    )

    if unit_sale_IDS == []: #* for handling new items
        save_unit_sale = [
            DailyTaskUnitSale.objects.create(
                uom_id= obj.id,
                value=val,
                percentage=percent,
                unit_price=price,
            ) for obj, val, percent, price in zip(uom, value_list, percentage_list, product_price_list) 
        ]
        data['error'] = 'Saving Unit Sale Price Done ...'
        data['type'] = 'success'
    elif old_uom_id != [] and new_uom_id != []:
        update_unit_sale = [
            DailyTaskUnitSale.objects.filter(
                    uom_id=obj[0],
                ).update(
                    value=obj[1] if obj[1] != '' else 0.00,
                    percentage=obj[2] if obj[2] != '' else 0.00,
                    unit_price=obj[3] if obj[3] != '' else 0.00,
            ) for obj in old_uom_id
        ]
        save_new_unit_sale = [
            DailyTaskUnitSale.objects.create(
                uom_id=obj[0],
                value=obj[1] if obj[1] != '' else 0.00,
                percentage=obj[2] if obj[2] != '' else 0.00,
                unit_price=obj[3] if obj[3] != '' else 0.00,
            ) for obj in (new_uom_id) 
        ]
        data['error'] = 'Saving new units and update existance units Sale Price Done ...'
        data['type'] = 'success'
        # data['price_list'] = [obj for obj in UnitPurchase.objects.values_list('unit_price', flat=True)]
    elif old_uom_id != []: #* in case of Old item only
        update_unit_sale = [
            DailyTaskUnitSale.objects.filter(
                    uom_id=obj[0],
                ).update(
                    value=obj[1] if obj[1] != '' else 0.00,
                    percentage=obj[2] if obj[2] != '' else 0.00,
                    unit_price=obj[3] if obj[3] != '' else 0.00,
            ) for obj in old_uom_id
        ]
        data['error'] = 'Updating Unit Sale Price Done ...'
        data['type'] = 'success'
        # data['price_list'] = [obj for obj in UnitPurchase.objects.values_list('unit_price', flat=True)]
    elif new_uom_id != []:
        save_new_unit_sale = [
            DailyTaskUnitSale.objects.create(
                uom_id= obj[0],
                value=obj[1] if obj[1] != '' else 0.00,
                percentage=obj[2] if obj[2] != '' else 0.00,
                unit_price=obj[3] if obj[3] != '' else 0.00,
            ) for obj in (new_uom_id) 
        ]
        data['error'] = 'Saving New Unit/units Sale Price Done ...'
        data['type'] = 'success'
    
    unit_purchase = DailyTaskUnitPurchase.objects.filter(uom_id__in=uom_ids)
    data['price_list'] = [obj for obj in unit_purchase.values_list('unit_price', flat=True).order_by('id')]
    data['value'] = [obj for obj in unit_sale.values_list('value', flat=True)]
    data['percentage'] = [obj for obj in unit_sale.values_list('percentage', flat=True)]
    print(
        '@@product_price_list::', product_price_list,
        '@@new_uom_id:::', new_uom_id,
        '**GROUP-OF-FIELDS**',
        [obj for obj in unit_sale.values_list('unit_price', 'value', 'percentage')]
        
    )
    
    return JsonResponse(data)



def update_sale_tab(request, id):
    data = {}
    
    unit_purchase = DailyTaskUnitPurchase.objects.values_list(
        'unit_price', flat=True
    ).filter(
        uom__daily_task_id=id
        )
    print([obj for obj in unit_purchase])
    data['unit_price'] = [obj for obj in unit_purchase]
    return JsonResponse(data)

def add_uom_purchase(request, id):
    data = {}
    # data['price_list'] = []
    product_price_list = request.GET.getlist('price-list[]')
    uom_id_list = request.GET.getlist('uom-id-list[]')
    
    uom = DailyTaskUOM.objects.select_related(
        'daily_task').filter(
            daily_task_id=id
            )
    uom_ids = [obj.id for obj in uom]
    unit_purchase = DailyTaskUnitPurchase.objects.filter(uom_id__in=uom_ids)
    unit_purchase_IDS = [obj.uom_id for obj in unit_purchase]
    
    origin_data = [(obj.uom_id, obj.unit_price) for obj in unit_purchase]
    
    old_uom_id = [
        (obj,pr) for obj,pr in zip(uom_id_list,product_price_list) if int(obj) in unit_purchase_IDS 
    ]
    new_uom_id = [
        (obj,pr) for obj,pr in zip(uom_id_list,product_price_list) if int(obj) not in unit_purchase_IDS]
    
    int_uom_id_list = [int(obj) for obj in uom_id_list]
    # new_uom_IDS = [(new_uom_id.remove(obj) if obj == False else obj) for obj in new_uom_id]
    print(
        '***old_uom_id***', old_uom_id, [(old_uom_id.remove(obj) if obj == False else obj) for obj in old_uom_id],
        '***NEW_uom_id***', new_uom_id, [new_uom_id.remove(obj) for obj in new_uom_id if obj == False] ,
        # [(new_uom_id.remove(obj) if obj == False else obj) for obj in new_uom_id],
        '**uom_id_list**', uom_id_list,
        '*##unit_purchase_IDS***', unit_purchase_IDS, 
        unit_purchase, '**uom_id_list==unit_purchase_IDS**', 
        [True if obj in int_uom_id_list else False for obj in unit_purchase_IDS], int_uom_id_list,
        '**origin_data**', origin_data
    )
    # data['unit_purchase'] = unit_purchase
    
    if unit_purchase_IDS == []: #* for handling new items
        save_unit_purchase = [
            DailyTaskUnitPurchase.objects.create(
                uom_id= obj.id,
                unit_price=price,
            ) for obj, price in zip(uom, product_price_list) 
        ]
        data['error'] = 'Saving Unit Purchase Price Done ...'
        data['type'] = 'success'
        # data['price_list'] = []
    elif old_uom_id != [] and new_uom_id != []:
        update_unit_purchase = [
            DailyTaskUnitPurchase.objects.filter(
                    uom_id=obj[0],
                ).update(
                    unit_price=obj[1],
            ) for obj in old_uom_id
        ]
        save_new_unit_purchase = [
            DailyTaskUnitPurchase.objects.create(
                uom_id= obj[0],
                unit_price=obj[1],
            ) for obj in (new_uom_id) 
        ]
        data['error'] = 'Saving new units and update existance units Purchase Price Done ...'
        data['type'] = 'success'
        # data['price_list'] = product_price_list
        #[obj for obj in unit_purchase.values_list('unit_price', flat=True)]
    elif old_uom_id != []: #* in case of Old item only
        update_unit_purchase = [
            DailyTaskUnitPurchase.objects.filter(
                    uom_id=obj[0],
                ).update(
                    unit_price=obj[1],
            ) for obj in old_uom_id
        ]
        data['error'] = 'Updating Unit Purchase Price Done ...'
        data['type'] = 'success'

    elif new_uom_id != []:
        save_new_unit_purchase = [
            DailyTaskUnitPurchase.objects.create(
                uom_id= obj[0],
                unit_price=obj[1],
            ) for obj in (new_uom_id) 
        ]
        data['error'] = 'Saving New Unit/units Purchase Price Done ...'
        data['type'] = 'success'
        # data['price_list'] = []
    # else:
        
    data['price_list'] = [obj for obj in unit_purchase.values_list('unit_price', flat=True)]   
    print(
        'product_price_list::', product_price_list,
        # 'save_unit_purchase::', save_unit_purchase,
        '$$$new_uom_id$$$:::', new_uom_id,
        '***WHY-PRICE-LIST-IS-EMPTY***',(data['price_list']) 
        # UnitPurchase.objects.filter(uom_id__in=[obj.id for obj in uom])
    )
    
    return JsonResponse(data)

def ajax_get(request):
    unit_id = request.POST.get("unit_id")
    if unit_id:
        unit = UnitNames.objects.values_list(
            'name', flat=True).filter(id=unit_id)
    else:
        unit = []
    data = {
        "unit": [obj for obj in unit],
    }
    return JsonResponse(data)