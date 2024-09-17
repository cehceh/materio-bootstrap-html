from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.http import JsonResponse


from apps.accounts.models import AdminProfile, EmployeeProfile
# from django.contrib.auth import authenticate, login
from apps.accounts.forms import AdminProfileForm , EmployeeProfileForm
from .forms import MessageForm

# from .forms import CustomUserCreationForm, CustomUserChangeForm
from itertools import chain

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.views import generic
from .models import CustomUser, Message #, UserProfile
from django.conf import settings
# from posapp.utils import prevent_changing_user_id


# @login_required
# @prevent_changing_user_id
# def add_user_profile(request, user_id):
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST or None, request.FILES or None)
#         if form.is_valid():
#             profile_form = form.save(commit=False)
#             profile_form.user = request.user
#             profile_form.save()
#             uuid = profile_form.profile_uuid
#             return redirect(reverse('users:edit_user_profile', args=(profile_form.user_id, uuid))) 
#     else:
#         form = UserProfileForm()

#     context = {
#         'btn' : 'Add User Profile',
#         'form': form,
#     }
#     return render(request, 'account/profile.html', context)

##### 
def users_table(request):
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

        main = CustomUser.objects.values(
                'id', 'username','role','mobile1','is_active',
            )

        data['main-list'] = [obj for obj in main]

        print("data['main-list'] ***",data['main-list'] , 'main.query******>', main.query)
        return JsonResponse(data, safe=False)
    elif show_log == 'true':
        log_qs = CustomUser.objects.values(
                'id', 'username','role','mobile1','is_active','date_joined','last_login'
            )
        log = log_qs
        data['log-list'] = [obj for obj in log]
        print("data['log-list'] ***", data['log-list'], 'main.query******>', log.query)
        return JsonResponse(data, safe=False)
    elif in_active == 'true':
        inactive = CustomUser.objects.values(
                'id', 'username','role','mobile1','is_active',
            ).filter(is_active=False).order_by('-id')
        # main = []
        data['inactive-list'] = [obj for obj in inactive]
        return JsonResponse(data, safe=False)
    elif is_active == 'true':
        active = CustomUser.objects.values(
            'id', 'username','role','mobile1',"is_active"
            ).filter(is_active=True).order_by('-id')
        data['active-list'] = [obj for obj in active]
        print("data['active-list'] ***", data['active-list'], 'main.query******>', active.query)
        return JsonResponse(data, safe=False)
    # elif show_deleted:
    #     delete = CustomUser.objects.values(
    #             'id', 'username','role','mobile1', 'updated_user__username','deleted_at','active'
    #         ).filter(
    #         is_deleted=True).order_by('-id')
            
    #     data['delete-list'] = [obj for obj in delete]
    #     print("data['delete-list'] ***", data['delete-list'], 'delete.query******>', delete.query)
    #     return JsonResponse(data, safe=False)
    
    
    
    
    
    
    # qs= CustomUser.objects.only()
    # qs = CustomUser.objects.select_related().order_by('-id')
    # inactive_qs = CustomUser.objects.select_related('address').filter( is_active=False).order_by('-id')
    # deleted_qs = CustomUser.objects.select_related('address').filter().order_by('-id')
    # main_qs = CustomUser.objects.select_related('address').only().filter().order_by('-id')
    # table_qs = CustomUser.objects.select_related('address').filter(is_active=True).order_by('-id')
    # combined_qs = list(chain(table_qs, inactive_qs))
    total_inv=CustomUser.objects.values('id').filter().count()
    total_active = CustomUser.objects.values('id').filter(is_active=True).count()
    total_inactive = CustomUser.objects.values('id').filter(is_active=False).count()

    
    context = {
        # 'qs':qs,
        # 'inactive_qs':inactive_qs,
        # 'deleted_qs':deleted_qs,
        # 'main_qs':main_qs,
        # 'table_qs':table_qs,
        # 'combined_qs':combined_qs,
        'total_inv':total_inv,
        'total_active':total_active,
        'total_inactive':total_inactive,
        
        'title': 'Users',
        }
    return render (request,'account/users_table.html',context )
######################???????? not needeed here needed in accounts app
# def edit_user_profile(request, user_id):
#     match = EmployeeProfile.objects.filter(user_id=user_id).exists()
#     if match:
#         qs = EmployeeProfile.objects.select_related('user').get(user_id=user_id)
#     else:
#         qs = None
#     form = EmployeeProfileForm(request.POST or None, request.FILES or None, instance=qs)
#     if form.is_valid():
#         profile_form = form.save(commit=False)
#         profile_form.user_id = request.user.id
#         profile_form.save()
        
#     context = {
#         'btn' : 'Save Changes',
#         'form': form,
#         "title": "Edit User Profile",
#     }
#     return render(request, 'account/profile.html', context)

@login_required
def edit_user_profile_old(request, user_id):

    match = AdminProfile.objects.filter(user_id=user_id).exists()
    if match:
        qs = AdminProfile.objects.select_related('user').get(user_id=user_id)
    else:
        qs = None
    form = AdminProfileForm(request.POST or None, request.FILES or None, instance=qs)
    if form.is_valid():
        profile_form = form.save(commit=False)
        profile_form.user_id = request.user.id
        profile_form.save()
        
    context = {
        'btn' : 'Save Changes',
        'form': form,
        "title": "Edit User Profile",
    }
    return render(request, 'account/profile.html', context)


def profile_details(request, user_id):
    qs = AdminProfile.objects.select_related(
        'user'
    ).get(user_id=user_id)

    context = {
        "title": "Profile Details",
    }
    return render(request, '', context)


def sent_message(request):
    ''' '''
    if request.POST:
        form = MessageForm(request.POST or None, user=request.user.id)
        if form.is_valid():
            save_form = form.save(commit=False)
            save_form.sender_id = request.user.id
            save_form.save()
            messages.success(request, 'Message has been sent to ' + '(' + save_form.receiver.username + ')')
            return redirect(reverse('users:edit_message', kwargs={'id': save_form.id}))
            
    else:
        form = MessageForm(user=request.user.id)

    context = {
        'form': form,
        'btn': 'Send',
        "title": "Sent Message",
        # 'page_title': 'Sending Message To Any User',
    }
    return render(request, 'account/message.html', context) 


def edit_message(request, id):
    ''' '''
    # user = request.user.id
    # if  request.user.is_staff:
    qs = Message.objects.get(id=id)
    form = MessageForm(request.user.id, request.POST or None, instance=qs)
    if request.POST:
        if form.is_valid():
            save_form = form.save(commit=False)
            save_form.sender_id = request.user.id
            save_form.save()
            messages.success(request, 'Message has been changed and resent to ' + '(' + save_form.receiver.username + ')')
            return redirect(reverse('users:edit_message', kwargs={'id': save_form.id }))
            
    context = {
        'form': form,
        'btn': 'Resend Changes',
        "title": "Edit Message",
        # 'page_title': 'Edit Sending Message',
    }
    return render(request, 'account/message.html', context) 


def list_messages(request):
    ''' '''
    qs_all = Message.objects.filter(is_read=False, receiver_id=request.user.id)
    qs_true = Message.objects.filter(is_read=True, receiver_id=request.user.id)
    Users = Message.objects.select_related('sender').filter(sender__is_staff=True, receiver_id=request.user.id).order_by('-created').distinct()
    # Users = Message.objects.values('sender').annotate(Count('sender')).filter(sender__is_staff=True, receiver_id=request.user.id).order_by('-created')
    # record = [item for item in Users]
    print('Users_from_func:=', Users, )  #Users[0]['sender__count']
    context = {
        'qs_true': qs_true,
        'qs_all': qs_all,
        'users': Users,
        "title": "List Messages",
    }
    return render(request, "account/list_messages.html", context)


def list_user_messages(request, sender):
    # qs_all = Message.objects.values('sender_id__username','is_read').filter(reciever_id=request.user.id)
    # all_isread = request.POST.get('all-isread')
    
    # print(qs_all, all_isread)
    Users = Message.objects.select_related('sender').filter(sender__username=sender, receiver_id=request.user.id).order_by('-created').distinct()
    # sender = [item for item in Users]
    context = {
        'users': Users,
        "title": "List User Messages",
    }
    return render(request, 'account/list_user_messages.html', context)

def is_read_changes(request, id):
    qs = Message.objects.get(id=id)
    if qs.is_read:
        Message.objects.filter(id=id, receiver_id=request.user.id).update(is_read=False)
    else:
        Message.objects.filter(id=id, receiver_id=request.user.id).update(is_read=True)

    return redirect(reverse('users:list_user_messages', kwargs={'sender': qs.sender}))


def mark_all_is_read(request):
    ''''''
    # qs_all = Message.objects.values('sender_id__username','is_read').order_by('-created')
    qs_all = Message.objects.filter(is_read=False, receiver_id=request.user.id).order_by('-created')
    # if request.method == 'GET':
    #     all_is_read = request.GET.get('all-is_read')
    #     print(all_is_read)
    if qs_all:
        Message.objects.filter(is_read=False, receiver_id=request.user.id).update(is_read=True)
    else:
        Message.objects.filter(is_read=True, receiver_id=request.user.id).update(is_read=False)
    # print('qs_all', qs_all)
    return redirect(reverse('users:list_message'))