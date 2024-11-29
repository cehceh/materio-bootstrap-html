from django.shortcuts import render


def main_page(request):
    
    context = {
        
    }
    return render(request, 'home/gold/main_page.html' , context)



