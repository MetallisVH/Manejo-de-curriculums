from django.shortcuts import render

def Index_page(request):
    return render(request, 'html/index.html')

def Home_page(request):
    return render(request, 'html/Home.html')