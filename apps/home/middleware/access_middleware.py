from django.shortcuts import redirect # type: ignore
from django.urls import reverse # type: ignore
from django.http import (   # type: ignore
    HttpResponseRedirect, HttpResponse, JsonResponse
)
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime, date

from apps.carts.models import (
    SellService, SellServicePayments 
)
from apps.configurations.models import ManageAppSettings

class AccessRestrictionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.warrning_date = datetime(2025, 1, 31)
        # specify the cutoff date
        self.cutoff_date = timezone.make_aware(datetime(2025, 1, 4, hour=22, minute=0))  
        
        self.check = ManageAppSettings.objects.exists()
        if self.check:
            self.start_date = ManageAppSettings.objects.first().start_date        
            self.expire_date = ManageAppSettings.objects.first().expire_date  
        else:
            self.start_date = timezone.now()
            self.expire_date = timezone.now()

    def __call__(self, request):
        # today = date.today() 
        # today = datetime.now()
        today = timezone.now()
        sales_qs = SellService.objects.filter()
        sales_count = sales_qs.aggregate(count=Count('id'))
        
        print(
            "sales_count['count']--PRE>>>>", sales_count,
            'sales_count--->>>', sales_qs.values('id').annotate(count=Count('id')),# values('id')
            'sales_count.count()>>>>', sales_qs.values('id').count()
        )
        diff_days = self.expire_date - self.start_date
        print("DIFF-DAYS:", diff_days)
        # if diff_days.days >= 17:
        #     return redirect(reverse("home:error_page", args=('500',)))
        
        if today > (self.expire_date): #self.warrning_date.day:
            # print(' self.warrning_date.day--->>>', self.expire_date, "TODAY:::", today)
            return HttpResponse('{W-error: Error-code-306}') 
            # return HttpResponseRedirect('WARRNING') 
        elif today > self.cutoff_date:
            print('self.cutoff_date--->>>', self.cutoff_date)
            return HttpResponse('{D-error: Error-code-307}')
            # return HttpResponseRedirect('Ask Administrator for this issue ..... ')  # redirect to access denied page
        elif sales_count['count'] >= 200:
            print("sales_count['count']>>>>", sales_count)
            # return HttpResponseRedirect('Error-code-')  # redirect to access denied page
            # return HttpResponse({"b-error": "Error-code-308"})
            return HttpResponse('{B-error: Error-code-308}')
        
        print(
            # 'today.day>>>>>',  (today),
            # 'datetime.now()>>>>', datetime.now(),
            # 'timezone.now()>>>>', timezone.localtime(timezone.now()),
            # 'self.cutoff_date>>>', self.cutoff_date,
            # 'self.warrning_date.day>>>', self.warrning_date.day
        )
        response = self.get_response(request)
        return response



