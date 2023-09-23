from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from .forms import RegistroEmpleadoForm
from django.shortcuts import render, redirect
from .models import Usuarios
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from datetime import date

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


def registro_empleado(request):
    if request.method == 'POST':
        form = RegistroEmpleadoForm(request.POST)
        if form.is_valid():
            # Calcula la edad a partir de la fecha de nacimiento y el año actual
            fecha_nacimiento = form.cleaned_data['fechaNacimiento']
            año_actual = date.today().year
            edad = año_actual - fecha_nacimiento.year - ((date.today().month, date.today().day) < (fecha_nacimiento.month, fecha_nacimiento.day))
            
            genero = form.cleaned_data['genero']
            
            if genero == 'otro':
                # Toma el valor ingresado en el campo 'otroGenero'
                genero = form.cleaned_data['otroGenero']

            # Crea una instancia del modelo Usuarios y asigna los valores del formulario
            usuario = Usuarios(
                nombre_usu=form.cleaned_data['nombreUsuario'],
                email=form.cleaned_data['correo'],
                contrasena=make_password(form.cleaned_data['contrasena']),
                telefono=form.cleaned_data['telefono'],
                fecha_nac=form.cleaned_data['fechaNacimiento'],
                genero=genero,
                edad=edad,  # Asigna la edad calculada
                nivel_cuenta = 0,
                nombre = form.cleaned_data['nombre'],
                apellido_p = form.cleaned_data['apellidoPaterno'],
                apellido_m = form.cleaned_data['apellidoMaterno'],
                rut = form.cleaned_data['rut'],
                dv = form.cleaned_data['dv']
                # Asigna otros campos del modelo Usuarios según sea necesario
            )
            usuario.save()  # Guarda el usuario en la base de datos
            messages.success(request, '¡Registro exitoso! Ahora puedes iniciar sesión.')
            return render(request, 'html/Registro_exitoso.html')
    else:
        form = RegistroEmpleadoForm()  # Crea una instancia del formulario vacío

    return render(request, 'Registro_empleado.html', {'form': form})