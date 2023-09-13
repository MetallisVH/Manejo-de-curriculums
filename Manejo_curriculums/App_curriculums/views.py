from django.shortcuts import render

def Index_page(request):
    return render(request, 'html/index.html')

def Home_page(request):
    return render(request, 'html/Home.html')

def Login_empleado(request):
    return render(request, 'html/inicio_empleado.html')

def Login_empleador(request):
    return render(request, 'html/inicio_empleador.html')

def Register_empelado(request):
    return render(request, 'html/Registro_empleado.html')

def Register_empleador(request):
    return render(request, 'html/Registro_empleador.html')