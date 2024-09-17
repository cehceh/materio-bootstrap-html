from django.shortcuts import render
from django.http import JsonResponse

from ..models import Departments
from ..forms import DepartmentsForm
from config.utils import model_id_restriction



def add_departments(request):
    data = {}
    data['department_id'] = None 
    data['error'] = 'ERROR !!!'
    data['type'] = 'error'
    if request.accepts('*/*') and request.method == "POST":
        form = DepartmentsForm(
            request.POST or None, 
        )
        
        for f in form:
            print(
                f.name,
                f.errors
            )
            if not f.errors:
                print('No errors, from is valid and : ', request.accepts('*/*'), request.method)
        
        department_name = request.POST.get("name") 
        print(
            'department_name**', department_name,
        )
        if not form.is_valid():
            data['department_id'] = None 
            msg = [
                ('department ' + key+' Error:', value[0]['message']) for key, value in (
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
            Departments.objects.filter(id=save_form.id).update(code='department-'+str(save_form.id))
            print('CODE >>>>', Departments.objects.get(id=save_form.id).code )
            msg = ('department with name "%s" saved successfully' % (department_name))
            
            data['department_id'] = save_form.id 
            data['department_name'] = save_form.name 
            #data['code'] = "department-" + str(save_form.id)
            data['error'] = msg
            data['type'] = 'success'
            return JsonResponse(data)
        
    else:
        form = DepartmentsForm()
    department_code = 'department-' + str(id)
    context = {
        'department_code' : department_code,
        'form': form,
        'title': 'Create Department'
    }
    return render(request, 'configurations/departments/add_departments.html', context)


@model_id_restriction(app_name='configurations', model_name='Departments')
def edit_departments(request, id):
    data = {}
    # data['Departments_id'] = id 
    # data['error'] = 'ERROR !!!'
    # data['type'] = 'error'
    
    
    qs = Departments.objects.select_related('user').get(id=id)
    form = DepartmentsForm(
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
        department_name = request.POST.get("name") 
        
        if not form.is_valid():
            msg = [
                (key +' Error:', value[0]['message']) for key, value in (
                    form.errors.get_json_data().items()
                )
            ]
            data['department_id'] = id
            data['error'] = msg
            data['type'] = 'error'    
            return JsonResponse(data)
        
        if form.is_valid():

            save_form = form.save(commit=False)
            save_form.updated_user = request.user
            save_form.code = 'department-' + str(id)
            print("EDIT-CODE-----",save_form.code)
            save_form.save()
            # save_form.code = 'department-' + str(id)
            error = ('department with name "%s" saved successfully' % (department_name))
            
            data['department_id'] = id 
            data['error'] = error
            data['type'] = 'success'
            return JsonResponse(data)
        # else:
            # form = DepartmentsForm()
    department_code = 'department-' + str(id)
    context = {
        'form': form,
        'qs': qs,
        'department_code' : department_code,
        'title': 'Edit department'
    }
    return render(request, 'configurations/departments/edit_departments.html', context)




def create_ajax_department_message(request):
    data = {}
    data['brannches_id'] = None 
    data['error'] = 'ERROR !!!'
    data['type'] = 'error'
    if request.is_ajax() and request.method == "POST":
        form = DepartmentsForm(request.POST or None)
        department_name = request.POST.get("department_name") 
        match = Departments.objects.select_related('user').filter(name=department_name).exists()
        if not match:
            if form.is_valid():

                save_form = form.save(commit=False)
                save_form.name = department_name
                save_form.user = request.user
                save_form.updated_user = request.user
                
                save_form.save()
                error = ('department with name "%s" saved successfully' % (department_name))
                data['department_id'] = save_form.id 
                data['error'] = error
                data['type'] = 'success'
            else:
                for f in form:
                    print('error from is not valid: ', f.name, f.errors)
                data['error'] = 'error from is not valid'
        else:
            print('name already exists and we must deal with it ...')
            error = ('department with name "%s" already exists !!!' % (department_name))
            data['department_id'] = None
            data['error'] = error
            data['type'] = 'error'
    else:
        form = DepartmentsForm()

    return JsonResponse(data)



def departments_table(request):
    show_log = request.GET.get("show-log")
    show_deleted = request.GET.get("show-deleted")
    in_active = request.GET.get("in-active")
    is_active = request.GET.get("active")
    show_main = request.GET.get('show-main')

    print(
        # 'TYPE****', type,
        'show_log@@@@@@@@@@@', show_log,
        "SHOW DELETEDDDDDD",show_deleted,
        "INACTIVEEEEE",in_active,
        'ACTIVEEEEE',is_active,
        'SHOWMAINNNNNN',show_main,
        )
   
    data = {}
    main = []
    log = []

    active = []
    inactive = []
    delete = []
    total_main = 0
    if show_main == 'true':

        main = Departments.objects.values(
                'id', 'code', 'name', 
            ).filter(is_deleted=False)

        data['main-list'] = [obj for obj in main]

        print("data['main-list'] ***",data['main-list'] , 'main.query******>', main.query)
        return JsonResponse(data, safe=False)
    elif show_log == 'true':
        log_qs = Departments.objects.values(
                'id', 'code', 'name','user__username','updated_user__username','created_at','updated_at','active'
            ).filter(is_deleted=False)
        log = log_qs
        data['log-list'] = [obj for obj in log]
        print("data['log-list'] ***", data['log-list'], 'main.query******>', log.query)
        return JsonResponse(data, safe=False)
    elif in_active == 'true':
        inactive = Departments.objects.values(
                'id', 'code', 'name'
            ).filter(active=False, is_deleted=False).order_by('-id')
        # main = []
        data['inactive-list'] = [obj for obj in inactive]
        return JsonResponse(data, safe=False)
    elif is_active == 'true':
        active = Departments.objects.values(
            'id', 'code', 'name'
            ).filter(active=True, is_deleted=False).order_by('-id')
        data['active-list'] = [obj for obj in active]
        print("data['active-list'] ***", data['active-list'], 'main.query******>', active.query)
        return JsonResponse(data, safe=False)
    elif show_deleted:
        delete = Departments.objects.values(
                'id', 'code', 'name', 'updated_user__username','deleted_at','active'
            ).filter(
            is_deleted=True).order_by('-id')
            
        data['delete-list'] = [obj for obj in delete]
        print("data['delete-list'] ***", data['delete-list'], 'delete.query******>', delete.query)
        return JsonResponse(data, safe=False)
    
    # table_qs = Departments.objects.select_related('user').only().order_by('-id')
    #?--Esraa--
    active_total = Departments.objects.select_related('user').filter(is_deleted=False, active=True).order_by('-id').count()
    inactive_total =  Departments.objects.select_related('user').filter(is_deleted=False, active=False).order_by('-id').count()
    deleted_total =  Departments.objects.select_related('user').filter(is_deleted=True).order_by('-id').count()
    
    main_total = Departments.objects.select_related('user').filter(is_deleted=False).order_by('-id').count()
    


    context = {
        # 'table_qs': table_qs,
        'title': 'Departments',
        # 'active_qs' : active_qs,
        # 'inactive_qs': inactive_qs,
        'inactive_total': inactive_total,
        'active_total': active_total,
        'deleted_total': deleted_total,
        'main_total': main_total,
        # 'table_total' :table_total,
        # 'deleted_qs': deleted_qs,
        # 'main_qs': main_qs,
        # 'combined_qs': combined_qs,

    }
    return render(request, 'configurations/departments/departments_table.html', context)