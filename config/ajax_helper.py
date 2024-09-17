from django.http import JsonResponse
from django.shortcuts import redirect
import json
from django.db.models import Count
from apps.categories.models import ParentCategory, NewCategory, MainCategory, SubCategory
from apps.configurations.models import (
    Branches, PosStation, UnitNames
)
from apps.vendors.models import Vendor
from apps.stores.models import Stores


def ajax_append(request):
    data = {}
    last_unit_name = UnitNames.objects.values_list('name').last()
    last_unit_id = UnitNames.objects.values_list('id').last()
    data['last_unit_name'] = last_unit_name #json.dumps(
    data['last_unit_id'] = last_unit_id #json.dumps(
    return JsonResponse(data) 
    
    
def login_required(request):
    data = {}
    data['error'] = ''
    data['type'] = '' 
    if not request.user.is_authenticated:
        msg ='You must be login in order to access our ERP system'
        data['error'] = msg
        data['type'] = 'info'
    else:
        msg ='Welcome to your dashboard'
        data['error'] = msg
        data['type'] = 'success'
    return JsonResponse(data)

def ajax_product_cat_tab(request):
    # branch_name = request.POST.get('pro-branch')
    # print('BRANCHES: ', branch_name, )
    # # branches = Branches.objects.only()
    # if branch_name != None or branch_name != '':
    #     pos_stations = PosStation.objects.values_list(
    #         'name', flat=True
    #     ).filter(
    #         branch=Branches.objects.select_related(
    #             'user'
    #         ).get(
    #             id=branch_name
    #         )
    #     )
    #     pos_names = [obj for obj in pos_stations]
    # else:
    #     pos_stations = []
    #     pos_names = []
    # print('BRANCHES: ', branch_name, 'POS-STATION: ', pos_stations, pos_names)

    main_category = request.POST.get('main_selected') # it is number not string
    parent_category = request.POST.get('parent_selected')
    
    #* for add new category without refresh the page
    # new_category_id = request.POST.get('new_cat_id')
    # print('WHY-IT-IS-EMPTY: ', new_category_id)
    # if new_category_id != None or new_category_id == '':
    #     new_cat_obj = NewCategory.objects.values('name', 'main', 'parent', 'child').filter(id=new_category_id)
    # else:
    #     new_cat_obj = []
    # print(
    #     # 'CAT-OBJ: ', [(obj['name']) for obj in new_cat_obj],
    #     'PARENT-CATEGORY', parent_category,
    #     'PARENT-MAIN: ', main_category,
    # )
    # sub_category = request.POST.get('sub_selected')
    if main_category:
        parent_main = MainCategory.objects.values(
            'parent__name', 'parent_id').filter(
                name=NewCategory.objects.get(id=main_category)) 
    else:
        parent_main = []
    parent_for_main = [(obj['parent_id'], obj['parent__name'] ) for obj in parent_main]
    # parent_for_main_name = [obj['parent__name'] for obj in parent_main]

    print(
        'PARENT-MAIN: ', main_category,
        'parent_for_main****', parent_for_main,
        'parent_category:::', parent_category,
    )
    if parent_category is not None and parent_category != '0':
        parent_sub = SubCategory.objects.values(
            'name__name').filter(
                parent=NewCategory.objects.get(name=parent_category)) #* I've changed (name= ) TO (id= )
    else: 
        parent_sub = []

    sub_for_parent = [obj['name__name'] for obj in parent_sub]

    print(
        'PARENT-CATEGORY', parent_category,
        'PARENT-MAIN: ', parent_for_main,
        'PARENT-SUB: ', parent_sub,
        'SUB-PARENT: ', sub_for_parent,
    )

    lev_1 = (request.POST.get("selectedLevel_1", ''))
    sub_2 = ParentCategory.objects.values('name').annotate(Count('name')).filter(parent__name=lev_1)
    sub_L2 = [obj['name'] for obj in sub_2]

    lev_2 = (request.POST.get("selectedLevel_2", ''))
    sub_3 = ParentCategory.objects.values('name').annotate(Count('name')).filter(parent__name=lev_2)
    sub_L3 = [obj['name'] for obj in sub_3]

    lev_3 = (request.POST.get("selectedLevel_3", ''))
    sub_4 = ParentCategory.objects.values('name').annotate(Count('name')).filter(parent__name=lev_3)
    sub_L4 = [obj['name'] for obj in sub_4]

    lev_4 = (request.POST.get("selectedLevel_4", ''))
    sub_5 = ParentCategory.objects.values('name').annotate(Count('name')).filter(parent__name=lev_4)
    sub_L5 = [obj['name'] for obj in sub_5]

    ##########    
    data = {
        "status": "ok",
        'parent_for_main': parent_for_main,
        # 'parent_for_main_name': parent_for_main_name,
        # 'parent_sub': parent_sub,
        'sub_for_parent': sub_for_parent,

        # 'pos_names': pos_names,

        # 'new_cat_obj': [(obj['name']) for obj in new_cat_obj],
        'sub_l2': sub_L2,        
        'sub_l3': sub_L3,

        'sub_l4': sub_L4,        
        'sub_l5': sub_L5,

    }
    return JsonResponse(data)


def category_message_post(request):
    _category_name = request.POST.get('cat')
    match = NewCategory.objects.filter(name=_category_name).exists()
    
    error_msg = request.POST.get('error_msg')
    print('ERROR FROM AJAX FUNCTION: ', error_msg)
    _main = request.POST.get('main')
    _parent = request.POST.get('parent')
    _child = request.POST.get('child')
    _main_name = request.POST.get('main_name')
    if error_msg == 'Please select a category type -> 2':
        msg = error_msg
        type = 'error'
    elif error_msg == 'Category name already exists !!! -> 3':
        msg = error_msg
        type = 'error'
    elif error_msg == 'Main Category saved successfully ... -> 4':
        msg = error_msg
        type = 'success'
    elif error_msg == 'Sub Category saved successfully ... -> 5':
        msg = error_msg
        type = 'success'
    else:
        msg = error_msg
        type = 'info'

    data = {
        'msg': msg,
        'type': type,
    }
    return JsonResponse(data)




def convert_text_to_id(request):
    data = {}
    
    vendor_name = request.GET.get('selectedText') 
    type = request.GET.get('type') 
    store_name = request.GET.get('selectedText') 
    print(
        'vendor_name****', "'",vendor_name,"'",
        'store_name****', "'", store_name, "'",
        Stores.objects.values('id').last(),
        'TYPE*****', type
    )
    if type == 'store':
        store_id = Stores.objects.values('id').filter(name=store_name)
        ven_id = []
    elif type == 'vendor':
        ven_id = Vendor.objects.values('id').filter(name=vendor_name)
        store_id = []
    else:
        store_id = []
        ven_id = []
        
    print(
        'store_id::***', store_id,
        'ven_id::***', ven_id,
    )
    data['vendor_id'] = [obj['id'] for obj in ven_id]
    data['store_id'] = [obj['id'] for obj in store_id]
    
    return JsonResponse(data)