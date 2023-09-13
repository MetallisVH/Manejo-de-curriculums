from django.shortcuts import render

def Index_page(request):
    return render(request, 'templates/html/index.html', {})
