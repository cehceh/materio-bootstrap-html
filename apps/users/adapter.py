from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import JsonResponse

from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.views import SignupView
from allauth.account.auth_backends import AuthenticationBackend
from apps.accounts.models import AdminProfile,EmployeeProfile,VendorProfile,CustomerProfile
from apps.employees.models import Employee
from apps.vendors.models import Vendor
from apps.configurations.models import ClientUsers, Departments, Branches

from django.contrib.auth import logout
# from fcm_django.models import FCMDevice

# from apps.accounts.models import AdminProfile, VendorProfile, ContactInfo
from apps.users.models import CustomUser
# from apps.configurations.models import 
from .forms import EmployeeCreationForm, CustomUserCreationForm 

from django.contrib import messages

from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect

# from apps.users.models import UserProfile


## As docs stated that we should override 
class CustomSignupView(SignupView):
    '''
        We override this class to 
        Create Admin and other user types from dashboard
    '''
    template_name = 'account/signup.html'
    form_class = CustomUserCreationForm

    def form_valid(self, form):
        next_url = self.request.META.get('HTTP_REFERER', '')
        # next_url = (url)
        self.user = form.save(self.request)
        if self.user.role == 'client' or self.user.role == 'rep' or self.user.role == 'vendor':
            # self.user.is_active = False
            CustomUser.objects.filter(username=self.user).update(is_active=False)
        ## next condition for create profile automatic 
        ## when we create user from dashboard as employee user
        # if self.user.user_type == 'admin':
        # mobile = self.user.mobile1
        # UserProfile.objects.create(
        #     user_id=self.user.id,
        #     mobile1='0'
        # )
        # created = not self.user  # Check if the user is being created
        # super().save()  # Call the parent class save method
        mobile = self.request.POST.get("mobile1")
        # mobile = self.user.mobile1
        print("MOBILEEEEE",mobile)

        # Create an admin profile if the user is being created and has the role of admin or owner
        mobile1=CustomUser.objects.get(mobile1=mobile).mobile1
        if self.user.role == 'client':
            ClientUsers.objects.create(
                name=self.user, role=1, is_client=True,
                user=self.request.user
            )
        print('MOBIKEEEEEEE!!!!!!',mobile1)
        if self.user.role == 'admin' or self.user.role == 'owner':
            print("INNN IFFF CONDDD FORRR ADMIN PROfFFF")
            AdminProfile.objects.create(
                first_name=self.user, admin_role=self.user.role, mobile1=mobile1, user=self.user
            )
        elif self.user.role == 'employee' or self.user.role == 'manager' or self.user.role == 'cashier':
            print("INNN IFFF CONDDD FORRR EMPLOYEE/MANAGER")
            EmployeeProfile.objects.create( 
                first_name=self.user, employee_role=self.user.role, mobile1=mobile1,user=self.user
            )
            # role = 3 if self.user.role == 'employee' else 2
            if self.user.role == 'supervisor':
                emp_role = 1
            if self.user.role == 'manager':
                emp_role = 2
            elif self.user.role == 'employee':
                emp_role = 3
            elif self.user.role == 'cashier':
                emp_role = 4
            elif self.user.role == 'delivery':
                emp_role = 5
            elif self.user.role == 'driver':
                emp_role = 6
            else:
                emp_role = 0

            employee = Employee.objects.create(
                full_name=self.user, 
                name=self.user,
                mobile1=mobile1, 
                employee_role=emp_role,
                department= Departments.objects.first(),
                branch=Branches.objects.first(),
                user=self.request.user,
                updated_user=self.request.user
            )
            ClientUsers.objects.create(
                name=self.user, name_id=employee.id, role=2, 
                is_employee=True, 
                mobile=mobile1,
                employee_id=employee.id,
                user=self.request.user,
                updated_user=self.request.user
            )
            
        #?no vendor role in vendor profile
        elif self.user.role == 'vendor':
            print("INNN IFFF CONDDD FORRR Vendor")
            VendorProfile.objects.create(
                user=self.user, mobile1=mobile
            )  
            Vendor.objects.create(full_name=self.user, mobile1=mobile,user=self.request.user)
            ClientUsers.objects.create(name=self.user, role=3, is_vendor=True, user=self.request.user)
        # data={}
        # if self.request.accepts('*/*'):
        #     data['type'] = 'success'
        #     data['msg'] = 'Create user done' #messages.get_messages(self.request)
        #     # {'success': True, , 'msg': messages.get_messages(self.request)}
        #     return JsonResponse(data)
        # else:
        #     return redirect(next_url)
        
        messages.success(self.request, 'Create (' + str(self.user.role) + ') User Done Successfully ...')
        return redirect(next_url)
    
    ###################??????
    # def form_valid(self, form):
    #     next_url = self.request.META.get('HTTP_REFERER', '')
    #     self.user = form.save(self.request)
        
    #     if self.user.role == 'client' or self.user.role == 'rep' or self.user.role == 'vendor':
    #         CustomUser.objects.filter(username=self.user).update(is_active=False)
        
    #     mobile = self.request.POST.get("mobile1")
    #     print("MOBILEEEEE", mobile)

    #     if self.user.role == 'admin' or self.user.role == 'owner':
    #         print("INNN IFFF CONDDD FORRR ADMIN PROfFFF")
    #         AdminProfile.objects.create(user=self.user, admin_role='Admin', mobile1=mobile)
    #         # Pass self.user instead of self

    #     messages.success(self.request, 'Create (' + str(self.user.role) + ') User Done Successfully ...')
    #     return redirect(next_url)

    
    
    def get_context_data(self, **kwargs):
        ret = super().get_context_data(**kwargs)
        ret['role'] = "admin"
        ret['title'] = "Create User"
        # if ret['role'] == "client":
        return ret






class EmployeeSignupView(SignupView):
    '''
        We override this class to 
        Create Admin and other users types from dashboard
    '''
    template_name = 'account/signup.html' #? important (No need to use another template "employee_signup.html"
    form_class = EmployeeCreationForm
    # redirect_field_name = 'next'
    # view_name = "company_signup_view"
    # success_url = No

    def form_valid(self, form):
        self.user = form.save(self.request)
        # if self.user.role == 'client' or self.user.role == 'rep' or self.user.role == 'vendor':
        #     self.user.is_active = False
        ## next condition for create profile automatic 
        ## when we create user from dashboard as employee user
        # if self.user.user_type == 'admin':
        # mobile = self.user.mobile1
        # UserProfile.objects.create(
        #     user_id=self.user.id,
        #     mobile1='0'
        # )
        messages.success(self.request, 'Create (' + str(self.user.role) + ') User Done Successfully ...')
        return redirect('/')
    
    def get_context_data(self, **kwargs):
        ret = super().get_context_data(**kwargs)
        ret['role'] = "employee"
        return ret


class CustomAccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        """
        Checks whether or not the site is open for signups.

        Next to simply returning True/False you can also intervene the
        regular flow by raising an ImmediateHttpResponse

        (Comment reproduced from the overridden method.)
        """
        ## The next condition for make create user in dashboard from admin users  
        if not request.user.is_authenticated: 
            return False
        else:
            if request.user.role == 'admin' or request.user.role == 'owner':  
                return True
            else: 
                return False
        


    # def save_user(self, request, user, form, commit=False):
    #     user = super().save_user(request, user, form, commit)
    #     data = form.cleaned_data
    #     # user.user_type = data.get('user_type')
    #     user.save() 
    #     print('username= ', user)
    #     UserProfile.objects.create(
    #         user_id=self.user.id,
    #         mobile1='0'
    #     )
    #     return user
    # def save_user(self, request, user, form, commit=False):
    #     data = form.cleaned_data
    #     user.email = data.get('email')
    #     user.username = data.get('username')
    #     # all your custom fields
    #     user.date_of_birth = data.get('date_of_birth')
    #     user.gender = data.get('gender')
    #     if 'password1' in data:
    #         user.set_password(data["password1"])
    #     else:
    #         user.set_unusable_password()
    #     self.populate_username(request, user)
    #     if commit:
    #         user.save()
    #         UserProfile.objects.create(
    #         user_id=self.user.id,
    #         mobile1='0'
    #     )
    #     return user

    def get_signup_redirect_url(self, request):
        # UserProfile.objects.create(
        #     user_id=self.request.user.id,
        # )
        if request:
            return reverse('users:edit_user_profile', args=(request.user.id,))
        return super().get_signup_redirect_url(request)

    def pre_authenticate(self, request, **credentials):
        '''
            To catch unauthorized users in login page 
        '''
        #? prevent customer from login in dashboard 
        username = request.POST.get('login')
        check_types = CustomUser.objects.filter(
            Q(username=username, is_active=True)
            ).exists() 
        if not check_types:
            # print('you are a customer')
            # from django.contrib import messages
            # messages.error(request, 'You are not allowed to access this site ... ')
            # return redirect('/accounts/login/')
            raise ValidationError(
                "You are not allowed to access this site ... ask administrator !!!! "
            )

