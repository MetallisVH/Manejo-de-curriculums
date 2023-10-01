from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from .forms import *
from django.shortcuts import render, redirect
from .models import Usuarios, Curriculums, Experiencias, Educaciones
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from datetime import date
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.urls import reverse
from django.http import HttpResponseRedirect
from .config import EMAIL_HOST_Usuario #Direccion de correo de config.py
import uuid

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

def user_logout(request):
    logout(request)
    
    return redirect('Home_page')

def Email_confirm(request):
    return render(request, 'html/Confirmacion.html')

def Error_403(request):
    return render(request, 'html/Error_403.html')

def recuperar(request):
    return render(request, 'html/Recuperacion.html')

def Recuperar_nombre_usuario(request):
    return render(request, 'html/Rec_usuario.html')

def Recuperar_contrasena(request):
    return render(request, 'html/Rec_contrasena.html')

def Info_curriculum(request):
    return render(request,'html/info_cvp.html')

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
                
            # Generar un token único
            token = str(uuid.uuid4())

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
                dv = form.cleaned_data['dv'],
                direccion = form.cleaned_data['direccion'],
                oauth = 0,
                auth_token = token
                # Asigna otros campos del modelo Usuarios según sea necesario
            )
            usuario.save()  # Guarda el usuario en la base de datos
            
            # Enviar correo electrónico de confirmación
            subject = 'Confirma tu dirección de correo electrónico'
            message = f'Haz clic en el siguiente enlace para confirmar tu correo electrónico: {request.build_absolute_uri(reverse("confirmar_email", args=[token]))}'
            from_email = EMAIL_HOST_Usuario
            recipient_list = [form.cleaned_data['correo']]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            messages.success(request, '¡Registro exitoso! Se ha enviado un correo electrónico de confirmación a tu dirección de correo.')
            
            return redirect('Email_confirm')
    else:
        form = RegistroEmpleadoForm()  # Crea una instancia del formulario vacío

    return render(request, 'html/Registro_empleado.html', {'form': form})

def registro_empleador(request):
    if request.method == 'POST':
        form = RegistroEmpleadorForm(request.POST)
        if form.is_valid():
            # Calcula la edad a partir de la fecha de nacimiento y el año actual
            fecha_nacimiento = form.cleaned_data['fechaNacimientoEmpleador']
            año_actual = date.today().year
            edad = año_actual - fecha_nacimiento.year - ((date.today().month, date.today().day) < (fecha_nacimiento.month, fecha_nacimiento.day))
            
            genero = form.cleaned_data['generoEmpleador']
            
            token = str(uuid.uuid4())

            
            if genero == 'otro':
                # Toma el valor ingresado en el campo 'otroGeneroEmpleador'
                genero = form.cleaned_data['otroGeneroEmpleador']

            # Crea una instancia del modelo Usuarios y asigna los valores del formulario
            usuario = Usuarios(
                nombre_usu=form.cleaned_data['nombreUsuarioEmpleador'],
                email=form.cleaned_data['correoEmpleador'],
                contrasena=make_password(form.cleaned_data['contrasenaEmpleador']),
                telefono=form.cleaned_data['telefonoEmpleador'],
                fecha_nac=form.cleaned_data['fechaNacimientoEmpleador'],
                genero=genero,
                edad=edad,
                nivel_cuenta=1,
                nombre=form.cleaned_data['razonSocial'],
                apellido_p = form.cleaned_data['apellidoPaterno'],
                apellido_m = form.cleaned_data['apellidoMaterno'],
                rut=form.cleaned_data['rut'],
                dv=form.cleaned_data['dv'],
                direccion=form.cleaned_data['direccion'],
                direccion_empr=form.cleaned_data['direccionEmpresa'],
                razon_social=form.cleaned_data['razonSocial'],
                rut_empr=form.cleaned_data['rut_emp'],
                dv_empr=form.cleaned_data['dv_emp'],
                oauth = 0,
                auth_token = token,
            )
            usuario.save()
            
            # Enviar correo electrónico de confirmación
            subject = 'Confirma tu dirección de correo electrónico'
            message = f'Haz clic en el siguiente enlace para confirmar tu correo electrónico: {request.build_absolute_uri(reverse("confirmar_email", args=[token]))}'
            from_email = EMAIL_HOST_Usuario
            recipient_list = [form.cleaned_data['correoEmpleador']]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            
            return redirect('Email_confirm')
    else:
        form = RegistroEmpleadorForm()

    return render(request, 'Registro_empleador.html', {'form': form})

def autenticar_empleado(request):
    if request.method == 'POST':
        nombre_usuario = request.POST['usuario']
        contrasena = request.POST['contrasena']

        try:
            # Busca un usuario con el nombre de usuario proporcionado
            usuario = Usuarios.objects.get(nombre_usu=nombre_usuario)

            # Verifica si la contraseña proporcionada coincide con la contraseña almacenada
            if check_password(contrasena, usuario.contrasena) and usuario.oauth == 1:
                # Autenticación exitosa, inicia sesión al usuario
                request.session['rol_usu'] = usuario.nivel_cuenta
                
                return redirect('Home_page')  # Redirige a la página de inicio después del inicio de sesión
            elif usuario.oauth == 0:
                
                return redirect('Error_403')
                
            else:
                # Contraseña incorrecta
                messages.error(request, 'Contraseña incorrecta')
        except Usuarios.DoesNotExist:
            # Usuario no encontrado
            messages.error(request, 'Usuario no encontrado')

    return render(request, 'html/inicio_empleado.html')

def autenticar_empleador(request):
    if request.method == 'POST':
        nombre_usuario = request.POST['usuario']
        contrasena = request.POST['contrasena']

        try:
            # Busca un empleador con el nombre de usuario proporcionado
            empleador = Usuarios.objects.get(nombre_usu=nombre_usuario)

            # Verifica si la contraseña proporcionada coincide con la contraseña almacenada
            if check_password(contrasena, empleador.contrasena) and empleador.oauth == 1:
                # Autenticación exitosa, inicia sesión al usuario
                request.session['rol_usu'] = empleador.nivel_cuenta
                
                return redirect('Home_page')  # Redirige a la página de inicio después del inicio de sesión
            elif empleador.oauth == 0:
                
                return redirect('Error_403')
            
            else:
                # Contraseña incorrecta
                messages.error(request, 'Contraseña incorrecta')
        except Usuarios.DoesNotExist:
            # Empleador no encontrado
            messages.error(request, 'Empleador no encontrado')

    return render(request, 'html/inicio_empleador.html')

def confirmar_email(request, token):
    try:
        # Buscar un usuario con el token de confirmación proporcionado
        usuario = Usuarios.objects.get(auth_token=token)

        # Marcar la dirección de correo electrónico como confirmada
        usuario.oauth = 1
        usuario.auth_token = None
        usuario.save()

        # Redirigir al usuario a una página de confirmación exitosa o cualquier otra página que desees
        return render(request, 'html/Registro_exitoso.html')
    except Usuarios.DoesNotExist:
        # Si el token no es válido o el usuario no existe, redirige a una página de error o muestra un mensaje de error
        return render(request, 'html/Error_confirmacion.html')

def recuperacion_contrasena(request):
    if request.method == 'POST':
        # Obtener la dirección de correo electrónico proporcionada por el usuario
        form = RecuperacionContrasenaForm(request.POST)
        if form.is_valid():
            # El formulario es válido, puedes acceder a la dirección de correo electrónico ingresada
            email = form.cleaned_data['email']
        else:
            return print('Error')

        try:
            # Buscar al usuario por su dirección de correo electrónico
            usuario = Usuarios.objects.get(email=email)

            # Generar un token o código único para la recuperación
            
            token = str(uuid.uuid4())
            usuario.auth_token = token
            usuario.save()

            # Enviar un correo electrónico al usuario con el enlace de recuperación
            subject = 'Reestablecimiento de contraseña'
            message = f'Haz clic en el siguiente enlace para restablecer tu contraseña: {request.build_absolute_uri(reverse("resetear_contrasena", args=[email, token]))}'
            from_email = EMAIL_HOST_Usuario
            recipient_list = [usuario.email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            # Redirigir a una página de éxito de recuperación
            return redirect('Email_confirm')

        except Usuarios.DoesNotExist:
            # Si no se encuentra el usuario, mostrar un mensaje de error
            error_message = 'No se encontró ningún usuario con esta dirección de correo electrónico.'
            return render(request, 'html/Rec_contrasena.html', {'error_message': error_message})

    return render(request, 'html/Rec_contrasena.html')

def recuperacion_usuario(request):
    if request.method == 'POST':
        form = RecuperacionUsuarioForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            try:
                
                usuario = Usuarios.objects.get(email=email)

                # Generar un token para la recuperación de nombre de usuario
                token = str(uuid.uuid4())
                    
                usuario.auth_token = token
                usuario.save()

                # Enviar un correo electrónico al usuario con el enlace de recuperación
                subject = 'Recuperación de Nombre de Usuario'
                message = f'Haz clic en el siguiente enlace para restablecer tu contraseña: {request.build_absolute_uri(reverse("enviar_usuario", args=[email, token]))}'
                from_email = EMAIL_HOST_Usuario
                recipient_list = [usuario.email]

                send_mail(subject, message, from_email, recipient_list, fail_silently=False)

                    # Redirigir a una página de éxito de recuperación
                return redirect('Email_confirm')
            except Usuarios.DoesNotExist:
                error_message = 'No se encontró ningún usuario con esta dirección de correo electrónico.'
                return render(request, 'html/Rec_usuario.html', {'error_message': error_message})
        else:
            # El formulario no es válido, mostrar un mensaje de error en el mismo formulario
            error_message = 'Por favor, ingresa una dirección de correo electrónico válida.'
            return render(request, 'recuperacion_usuario.html', {'error_message': error_message})

    form = RecuperacionUsuarioForm()
    return render(request, 'recuperacion_usuario.html', {'form': form})

def resetear_contrasena(request, email, token):

    try:
        # Buscar al usuario por su dirección de correo electrónico
        usuario = Usuarios.objects.get(email=email)

        # Verificar si el token es válido para el usuario

        if usuario.auth_token == token:
            return render(request, 'html/resetear_contrasena.html', {'email': email, 'token': token})
        else:
            # Si el token no es válido, mostrar un mensaje de error y redirigir a una página de error
            messages.error(request, 'El enlace de restablecimiento de contraseña no es válido. Por favor, solicita un nuevo enlace.')
            return redirect('pagina_de_error')  # Cambia 'pagina_de_error' al nombre de tu página de error
    except Usuarios.DoesNotExist:
        # Si no se encuentra el usuario, mostrar un mensaje de error y redirigir a una página de error
        messages.error(request, 'No se encontró ningún usuario con esta dirección de correo electrónico.')
        return redirect('pagina_de_error')  # Cambia 'pagina_de_error' al nombre de tu página de error
    
def reset_contrasena(request, email, token):
    print(email)
    print(token)
    try:
        # Buscar al usuario por su dirección de correo electrónico
        usuario = Usuarios.objects.get(email=email)

        # Verificar si el token es válido para el usuario

        if usuario.auth_token == token:
            if request.method == 'POST':
                form = RestablecerContrasenaForm(request.POST)

                if form.is_valid():
                    # Si el formulario es válido, establecer la nueva contraseña para el usuario
                    nueva_contrasena = form.cleaned_data['nueva_contrasena']
                    usuario.contrasena = nueva_contrasena
                    usuario.auth_token = None
                    usuario.save()

                    # Autenticar al usuario con la nueva contraseña
                    
                    if check_password(nueva_contrasena, usuario.contrasena):                      
                            
                        request.session['rol_usu'] = usuario.nivel_cuenta
                            
                        return redirect('Home_page')  # Cambia 'pagina_de_exito' a la URL que desees
                    
                    else:
                        # Si no se pudo autenticar al usuario, mostrar un mensaje de error
                        messages.error(request, 'Hubo un error al establecer la contraseña. Inténtalo nuevamente.')
                        return redirect('pagina_de_error')  # Cambia 'pagina_de_error' al nombre de tu página de error
                else:
                    form = RestablecerContrasenaForm()
                    # Si el formulario no es válido, mostrar el formulario con errores
                    return render(request, 'html/resetear_contrasena.html', {'form': form})
            else:
                # Si el método de solicitud no es POST, mostrar el formulario de restablecimiento de contraseña
                form = RestablecerContrasenaForm()
            
                return render(request,'html/resetear_contrasena.html', {'form': form})
        else:
            # Si el token no es válido, mostrar un mensaje de error y redirigir a una página de error
            messages.error(request, 'El enlace de restablecimiento de contraseña no es válido. Por favor, solicita un nuevo enlace.')
            return redirect('pagina_de_error')  # Cambia 'pagina_de_error' al nombre de tu página de error
    except Usuarios.DoesNotExist:
        # Si no se encuentra el usuario, mostrar un mensaje de error y redirigir a una página de error
        messages.error(request, 'No se encontró ningún usuario con esta dirección de correo electrónico.')
        return redirect('pagina_de_error')  # Cambia 'pagina_de_error' al nombre de tu página de error

def enviar_usuario(request, email, token):

    try:
        # Buscar al usuario por su dirección de correo electrónico
        usuario = Usuarios.objects.get(email=email)

        # Verificar si el token es válido para el usuario

        if usuario.auth_token == token:
            # Generar un mensaje de correo electrónico con el nombre de usuario
            usuario.auth_token = None
            usuario.save()
            
            subject = 'Recuperación de Nombre de Usuario'
            message = f'Tu nombre de usuario es: {usuario.nombre_usu}'
            from_email = EMAIL_HOST_Usuario  # Cambia esto a tu dirección de correo electrónico
            recipient_list = [usuario.email]

            # Enviar el correo electrónico
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            # Redirigir al usuario a una página de éxito o a su perfil, por ejemplo
            return redirect('pagina_de_exito')  # Cambia 'pagina_de_exito' a la URL que desees
        else:
            # Si el token no es válido, mostrar un mensaje de error y redirigir a una página de error
            messages.error(request, 'El enlace de recuperación de nombre de usuario no es válido. Por favor, solicita un nuevo enlace.')
            return redirect('pagina_de_error')  # Cambia 'pagina_de_error' al nombre de tu página de error
    except Usuarios.DoesNotExist:
        # Si no se encuentra el usuario, mostrar un mensaje de error y redirigir a una página de error
        messages.error(request, 'No se encontró ningún usuario con esta dirección de correo electrónico.')
        return redirect('pagina_de_error')  # Cambia 'pagina_de_error' al nombre de tu página de error

def registrar_curriculum(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre_completo = request.POST.get('nombre_completo')
        email = request.POST.get('email')
        puntaje = request.POST.get('puntaje')

        # Crear instancia del modelo y guardar en la base de datos
        curriculum = Curriculums(nombre_completo=nombre_completo, email=email, puntaje=puntaje)
        curriculum.save()

        return render(request, 'html/Registro_exitoso.html')
    else:
        # Renderizar el formulario para el método GET
        return render(request, 'tu_template.html')  # Reemplaza 'tu_template.html' con el nombre de tu plantilla
    