from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from .forms import *
from django.utils import timezone
from django.shortcuts import render, redirect
from .models import models ,Usuarios, Curriculums, Experiencias, Educaciones, Habilidades, Idiomas, Trabajos, Aplicaciones, Candidatos
from django.template.loader import get_template
from reportlab.pdfgen import canvas
from io import BytesIO
from collections import defaultdict
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from datetime import date
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from .config import EMAIL_HOST_Usuario #Direccion de correo de config.py
from datetime import datetime
import uuid
from django.db.models import Q

def Index_page(request):
    return render(request, 'html/index.html')

def Home_page(request):
    try:
        nombre_usu = request.session.get('nombre_usu')
        
        usuario = Usuarios.objects.get(nombre_usu=nombre_usu)
        
        curriculum = Curriculums.objects.get(nombre_usu=usuario)
        
        empleado_area = curriculum.area

        # Filtra los trabajos basados en el área del empleado
        trabajos_recomendados = Trabajos.objects.filter(area=empleado_area)
    except:
        trabajos_recomendados = ''

    return render(request, 'html/Home.html', {'trabajos_recomendados': trabajos_recomendados})

def Login_empleado(request):
    return render(request, 'html/inicio_empleado.html')

def Editar_curriculum(request):
    nombre_usuario = request.session.get('nombre_usu')
    usuario=Usuarios.objects.get(nombre_usu=nombre_usuario) 
    curriculum = Curriculums.objects.get(nombre_usu=usuario)
    experiencias_laborales = Experiencias.objects.filter(nombre_usu=usuario)
    habilidades = Habilidades.objects.filter(nombre_usu=usuario)
    idiomas=Idiomas.objects.filter(nombre_usu=usuario)
    educacion=Educaciones.objects.filter(nombre_usu=usuario)
    
    context = {'curriculum':curriculum, 'experiencias_laborales':experiencias_laborales,'habilidades':habilidades,'idiomas':idiomas,'educacion':educacion} 
    
    return render(request, 'html/editar_curriculum.html',context)

def Login_empleador(request):
    return render(request, 'html/inicio_empleador.html')

def Register_empelado(request):
    return render(request, 'html/Registro_empleado.html')

def Register_empleador(request):
    return render(request, 'html/Registro_empleador.html')

def exp_opciones(request):
    nombre_usuario = request.session.get('nombre_usu')
    usuario = Usuarios.objects.get(nombre_usu=nombre_usuario)
    curriculum = Curriculums.objects.get(nombre_usu=usuario)
    experiencias = Experiencias.objects.filter(nombre_usu=usuario)
    habilidades = Habilidades.objects.filter(nombre_usu=usuario)
    idiomas = Idiomas.objects.filter(nombre_usu=usuario)
    educacion = Educaciones.objects.filter(nombre_usu=usuario)
    
    contexto = {
        'usuario': usuario,
        'curriculum': curriculum,
        'experiencias': experiencias,
        'habilidades': habilidades,
        'idiomas': idiomas,
        'educaciones': educacion,
    }
    
    return render(request, 'html/exp_curriculum.html', contexto)

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

def lista_trabajos(request):
    nom_usu = request.session.get('nombre_usu')
    usuario = Usuarios.objects.get(nombre_usu=nom_usu,deleted_at=None)
    trabajos = Trabajos.objects.filter(publicador=usuario,deleted_at=None)
    
    context = {'trabajos':trabajos}
    
    
    return render(request,'html/listado_trabajos.html',context)

def Info_curriculum(request):
    try:
        # Recuperar datos del usuario desde la tabla Curriculums
        nombre_usu = request.session.get('nombre_usu')
        usuario = Curriculums.objects.get(nombre_usu=nombre_usu,deleted_at=None)

        # Recuperar experiencias laborales, educación, habilidades e idiomas asociadas al usuario
        experiencias_laborales = Experiencias.objects.filter(nombre_usu=nombre_usu, deleted_at=None)
        educacion = Educaciones.objects.filter(nombre_usu=nombre_usu, deleted_at=None)
        habilidades = Habilidades.objects.filter(nombre_usu=nombre_usu, deleted_at=None)
        idiomas = Idiomas.objects.filter(nombre_usu=nombre_usu, deleted_at=None)
        curriculum = Curriculums.objects.get(nombre_usu=nombre_usu,deleted_at=None)
        curr_area = curriculum.area

        if curriculum.deleted_at is not None:
            raise Curriculums.DoesNotExist

        return render(request, 'html/info_cvp.html', {
            'usuario': usuario,
            'experiencias_laborales': experiencias_laborales,
            'educacion': educacion,
            'habilidades': habilidades,
            'idiomas': idiomas,
            'area': curr_area
        })
    except Curriculums.DoesNotExist:
        return render(request, 'html/info_cvp.html', {'crear_curriculum': True})

def Registro_curriculum(request):
    try:
        nombre_usuario = request.session.get('nombre_usu')
        usuario = Usuarios.objects.get(nombre_usu=nombre_usuario, deleted_at=None)
    except Usuarios.DoesNotExist:
        usuario = ''

    try:
        curriculum = Curriculums.objects.get(nombre_usu=usuario, deleted_at=None)
    except Curriculums.DoesNotExist:
        curriculum = ''

    try:
        experiencias_laborales = Experiencias.objects.filter(nombre_usu=usuario, deleted_at=None)
    except Experiencias.DoesNotExist:
        experiencias_laborales = ''

    try:
        habilidades = Habilidades.objects.filter(nombre_usu=usuario, deleted_at=None)
    except Habilidades.DoesNotExist:
        habilidades = ''

    try:
        idiomas = Idiomas.objects.filter(nombre_usu=usuario, deleted_at=None)
    except Idiomas.DoesNotExist:
        idiomas = ''

    try:
        educacion = Educaciones.objects.filter(nombre_usu=usuario, deleted_at=None)
    except Educaciones.DoesNotExist:
        educacion = ''

    context = {'curriculum': curriculum, 'experiencias_laborales': experiencias_laborales,
            'habilidades': habilidades, 'idiomas': idiomas, 'educacion': educacion}

    return render(request, 'html/Registro_curriculums.html', context)

def Registro_exitoso(request):
    return render(request, 'html/Registro_exitoso.html')

def publicar_trabajo(request):
    educaciones_superior = Educaciones.objects.filter(nivel_educacion='superior')
    
    areas_unicas = educaciones_superior.values_list('especialidad', flat=True).distinct()
    
    context = {'especialidades': areas_unicas}
    
    return render(request,'html/Publicar_trabajo.html',context)

def listado_empleos(request):
    # Obtener todos los trabajos disponibles
    trabajos = Trabajos.objects.all()

    # Pasa la lista de trabajos al contexto de la plantilla
    context = {'trabajos': trabajos}

    # Renderiza la plantilla
    return render(request, 'html/lista_empleos.html', context)

def listado_aplicantes(request):
    # Obtener la lista de aplicantes ordenada por puntos
    aplicantes = Aplicaciones.objects.all().order_by('-puntos_aplicante')
    
    # Obtener todos los curriculums
    curriculums = Curriculums.objects.all()
    
    trabajos = Trabajos.objects.all()

    # Crear un diccionario que contenga la información necesaria para la plantilla
    context = {'aplicantes': aplicantes, 'curriculums': curriculums,'trabajos':trabajos}

    return render(request, 'html/lista_candidatos_ordenados.html', context)

def lista_empleados(request):
    curriculums = Curriculums.objects.all().order_by('-puntaje')
    return render(request, 'html/lista_candidatos.html', {'curriculums': curriculums})

def mis_aplicaciones(request):
    # Obtener el usuario actual
    nombre_usuario = request.session.get('nombre_usu')
    usuario_actual = Usuarios.objects.get(nombre_usu=nombre_usuario,deleted_at=None)

    # Filtrar las aplicaciones realizadas por el usuario actual
    aplicaciones_usuario = Aplicaciones.objects.filter(aplicante=usuario_actual,deleted_at=None)

    # Puedes agregar más contexto según tus necesidades
    context = {
        'aplicaciones_usuario': aplicaciones_usuario
    }

    return render(request, 'html/mis_aplicaciones.html', context)
   
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
                rut_empr=form.cleaned_data['rut'],
                dv_empr=form.cleaned_data['dv'],
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
            if check_password(contrasena, usuario.contrasena) and usuario.oauth == 1 and usuario.nivel_cuenta == 0:
                # Autenticación exitosa, inicia sesión al usuario
                request.session['rol_usu'] = usuario.nivel_cuenta
                request.session['nombre_usu'] = usuario.nombre_usu
                
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
            if check_password(contrasena, empleador.contrasena) and empleador.oauth == 1 and empleador.nivel_cuenta == 1:
                # Autenticación exitosa, inicia sesión al usuario
                request.session['rol_usu'] = empleador.nivel_cuenta
                request.session['nombre_usu'] = empleador.nombre_usu
                
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
        nombre_completo = request.POST['nombre']
        email = request.POST['correo']
        telefono = request.POST.get('telefono', None)
        area = request.POST.get('area', None)  # Asegúrate de que 'area' sea el nombre correcto en tu formulario

        # Utiliza el nombre de usuario almacenado en la variable de sesión
        nombre_usu = request.session.get('nombre_usu')
        usuario = Usuarios.objects.get(nombre_usu=nombre_usu)

        # Guarda el nuevo curriculum con el área
        curriculum = Curriculums(nombre_completo=nombre_completo, email=email, telefono=telefono, area=area, nombre_usu=usuario)
        curriculum.save()

        # Si también necesitas procesar y guardar otros datos relacionados, como experiencia laboral, educación, habilidades, idiomas, etc.,
        # deberías hacerlo aquí siguiendo un patrón similar.

        # Calcula el puntaje total y actualiza el campo 'puntaje' en el modelo Curriculums
        puntaje_total = calcular_puntaje(usuario=nombre_usu)
        curriculum.puntaje = puntaje_total
        curriculum.save()

        return redirect('Registro_exitoso')  # Redirige a la página de confirmación o a donde quieras

    return render(request, 'tu_template.html')

def calcular_puntaje(usuario):
    # Calcula el puntaje total para un usuario sumando los puntos de experiencias, educaciones, habilidades e idiomas
    puntaje_experiencias = Experiencias.objects.filter(nombre_usu=usuario,deleted_at=None).aggregate(Sum('puntos'))['puntos__sum'] or 0
    puntaje_educaciones = Educaciones.objects.filter(nombre_usu=usuario,deleted_at=None).aggregate(Sum('puntos'))['puntos__sum'] or 0
    puntaje_habilidades = Habilidades.objects.filter(nombre_usu=usuario,deleted_at=None).aggregate(Sum('puntos'))['puntos__sum'] or 0
    puntaje_idiomas = Idiomas.objects.filter(nombre_usu=usuario,deleted_at=None).aggregate(Sum('puntos'))['puntos__sum'] or 0

    puntaje_total = puntaje_experiencias + puntaje_educaciones + puntaje_habilidades + puntaje_idiomas
    return puntaje_total

def guardar_educacion(request):
    if request.method == 'POST':
        nivel_educacion = request.POST.get('nivelEducacion')
        nombre_instituto = request.POST.get('instituto')
        cursos = request.POST.get('cursos')
        carrera = request.POST.get('titulo_carrera')
        curso_termino = request.POST.get('cursoTermino') # Nuevo campo
        area = request.POST.get('area')
        
        if carrera != '':
            cursos = carrera
            curso_termino = carrera
        
        if area == None or area == '' or area == 'No seleccionada':
            area = 'Conocimiento escolar base (general/generalista)'
        
        # Utiliza timezone.make_aware para asegurar que la zona horaria esté presente
        fecha_inicio = timezone.make_aware(datetime.strptime(request.POST.get('fechaInicio'), '%Y-%m-%d'))

        # Asegúrate de que fecha_termino también sea un objeto datetime
        fecha_termino = timezone.make_aware(datetime.strptime(request.POST.get('fechaTermino'), '%Y-%m-%d'))

        # Puedes acceder al archivo de la siguiente manera:
        archivo_educacion = request.FILES.get('archivoEducacion')

        # Verifica si se cargó un archivo
        if archivo_educacion:
            archivo_subido = 'si'
            puntos = 20
        else:
            archivo_subido = 'no'
            puntos = 10

        # Obtén la instancia de Usuarios correspondiente al nombre de usuario
        nombre_usuario = request.session.get('nombre_usu')
        usuario = Usuarios.objects.get(nombre_usu=nombre_usuario)

        # Crea una instancia de Educacion y guarda los datos
        educacion = Educaciones(
            nombre_usu=usuario,
            nivel_educacion=nivel_educacion,
            nombre_instituto=nombre_instituto,
            curso=cursos,
            curso_termino=curso_termino,  # Nuevo campo
            desde=fecha_inicio,
            hasta=fecha_termino,
            archivo_educacion=archivo_subido,
            puntos=puntos,
            area=area,
            especialidad=carrera
        )
        educacion.save()
        print(f"Datos guardados correctamente: {educacion}")

        # Redirige o responde según tu lógica
        try:
            curriculum=Curriculums.objects.get(nombre_usu=usuario,deleted_at=None)
            new_puntaje_curriculum = calcular_puntaje(usuario)
            curriculum.puntaje = new_puntaje_curriculum
            curriculum.save()
        except:
            return redirect('Registro_curriculum')
        
        return redirect('Registro_curriculum')
    else:
        return redirect('Registro_curriculum')
    

def guardar_experiencia(request):
    if request.method == 'POST':
        empresa = request.POST.get('empresa')
        puesto = request.POST.get('puesto')
        area = request.POST.get('area')
        
        # Utiliza timezone.make_aware para asegurar que la zona horaria esté presente
        fecha_inicio = timezone.make_aware(datetime.strptime(request.POST.get('fechaInicio'), '%Y-%m-%d'))

        # Asegúrate de que fecha_termino también sea un objeto datetime
        fecha_termino_str = request.POST.get('fechaTermino')
        fecha_termino = timezone.make_aware(datetime.strptime(fecha_termino_str, '%Y-%m-%d')) if fecha_termino_str else None

        archivo_experiencia = request.FILES.get('archivoExperiencia')

        if archivo_experiencia:
            archivo_subido = 'si'
            puntos = 20
        else:
            archivo_subido = 'no'
            puntos = 10

        nombre_usuario = request.session.get('nombre_usu')
        usuario = Usuarios.objects.get(nombre_usu=nombre_usuario)

        experiencia = Experiencias(
            nombre_usu=usuario,
            empresa=empresa,
            puesto=puesto,
            desde=fecha_inicio,
            hasta=fecha_termino,
            archivo_experiencia=archivo_subido,
            puntos=puntos,
            area=area
        )
        experiencia.save()
        
        try:
            curriculum=Curriculums.objects.get(nombre_usu=usuario,deleted_at=None)
            new_puntaje_curriculum = calcular_puntaje(usuario)
            curriculum.puntaje = new_puntaje_curriculum
            curriculum.save()
        except:
            return redirect('Registro_curriculum')

        return redirect('Registro_curriculum')
    else:
        return redirect('Registro_curriculum')
    
def guardar_habilidad(request):
    if request.method == 'POST':
        habilidad = request.POST.get('habilidad')
        nivel = request.POST.get('nivel')
        area = request.POST.get('area')

        # Puedes acceder al archivo de la siguiente manera:
        archivo_habilidad = request.FILES.get('archivoHabilidad')

        # Verifica si se cargó un archivo
        if archivo_habilidad:
            archivo_subido = 'si'
            puntos = 20
        else:
            archivo_subido = 'no'
            puntos = 10

        # Obtén la instancia de Usuarios correspondiente al nombre de usuario (ajusta según tu lógica)
        nombre_usuario = request.session.get('nombre_usu')
        usuario = Usuarios.objects.get(nombre_usu=nombre_usuario)

        # Crea una instancia de Habilidades y guarda los datos
        habilidad = Habilidades(
            nombre_usu=usuario,
            habilidad=habilidad,
            nivel=nivel,
            archivo_habilidad=archivo_subido,
            puntos=puntos,
            area=area
        )
        habilidad.save()

        # Aquí puedes hacer algo con los puntos, como almacenarlos en otro modelo o realizar alguna lógica adicional
        
        try:
            curriculum=Curriculums.objects.get(nombre_usu=usuario,deleted_at=None)
            new_puntaje_curriculum = calcular_puntaje(usuario)
            curriculum.puntaje = new_puntaje_curriculum
            curriculum.save()
        except:
            return redirect('Registro_curriculum')

        # Redirige o responde según tu lógica
        return redirect('Registro_curriculum')
    else:
        return redirect('Registro_curriculum')
    
def guardar_idioma(request):
    if request.method == 'POST':
        idioma = request.POST.get('idioma')
        nivel_idioma = request.POST.get('nivelIdioma')
        area = request.POST.get('area')

        # Puedes acceder al archivo de la siguiente manera:
        archivo_idioma = request.FILES.get('archivoIdioma')

        # Verifica si se cargó un archivo
        if archivo_idioma:
            archivo_subido = 'si'
            puntos = 20
        else:
            archivo_subido = 'no'
            puntos = 10

        # Obtén la instancia de Usuarios correspondiente al nombre de usuario
        nombre_usuario = request.session.get('nombre_usu')  # Reemplaza esto con la lógica para obtener el nombre de usuario actual
        usuario = Usuarios.objects.get(nombre_usu=nombre_usuario)

        # Crea una instancia de Idiomas y guarda los datos
        idioma_instancia = Idiomas(
            nombre_usu=usuario,  
            idioma=idioma,
            nivel_idioma=nivel_idioma,
            archivo_idioma=archivo_subido,
            puntos=puntos,
            area=area
        )
        idioma_instancia.save()
        
        try:
            curriculum=Curriculums.objects.get(nombre_usu=usuario,deleted_at=None)
            new_puntaje_curriculum = calcular_puntaje(usuario)
            curriculum.puntaje = new_puntaje_curriculum
            curriculum.save()
        except:
            return redirect('Registro_curriculum')

        # Redirige o responde según tu lógica
        return redirect('Registro_curriculum')  # Reemplaza con la URL correcta
    else:
        return redirect('Registro_curriculum')  # Reemplaza con la URL correcta
    
def guardar_trabajo(request):
    if request.method == 'POST':
        titulo = request.POST['titulo']
        descripcion = request.POST['descripcion']
        requisitos = request.POST['requisitos']
        ubicacion = request.POST['ubicacion']
        sueldo = request.POST['sueldo']
        area = request.POST['area']
        fecha_publicacion = request.POST['fecha_publicacion']
        trabajo_remoto = request.POST.get('trabajo_remoto', False)
        fecha_limite = request.POST['fecha_limite']
        tipo_trabajo = request.POST['tipo_trabajo']
        tipo_contrato = request.POST['tipo_contrato']
        especialidades_buscadas = request.POST.getlist('especialidades[]')
        especialidades_usuarios = Educaciones.objects.filter(Q(nivel_educacion='superior') & ~Q(especialidad='') & Q(deleted_at=None))
        cuenta_especialidades_por_usuario = defaultdict(int)
        puntos_candidato = 0

        for especialidad in especialidades_buscadas:
            aplicantes_aptos = especialidades_usuarios.filter(especialidad=especialidad)
            
            for aplicante in aplicantes_aptos:
                # Aquí puedes diferenciar por el atributo 'especialidad' de cada aplicante
                print(f"Usuario {aplicante.nombre_usu} tiene la especialidad {aplicante.especialidad}")
                
                # Sumar 10 puntos por cada especialidad encontrada
                cuenta_especialidades_por_usuario[aplicante.nombre_usu] = cuenta_especialidades_por_usuario.get(aplicante.nombre_usu, 0) + 1

        # Calcular los puntos totales para cada usuario
            
        
        if fecha_limite == '':
            fecha_limite = None
        
        nombre_usuario = request.session.get('nombre_usu')
        usuario = Usuarios.objects.get(nombre_usu=nombre_usuario)

        # Crear una instancia del modelo Trabajo y guardar los datos
        trabajo = Trabajos(
            publicador = usuario,
            titulo=titulo,
            descripcion=descripcion,
            requisitos=requisitos,
            ubicacion=ubicacion,
            sueldo=sueldo,
            area=area,
            fecha_publicacion=fecha_publicacion,
            remoto=trabajo_remoto,
            fecha_limite=fecha_limite,
            tipo_trabajo=tipo_trabajo,
            tipo_contrato=tipo_contrato,
        )
        trabajo.save()
        
        for usuarios, cuenta_especialidades in cuenta_especialidades_por_usuario.items():
            puntos_candidato = cuenta_especialidades * 20  # Calcular los puntos
            usuario_objeto = Usuarios.objects.get(nombre_usu=usuarios.nombre_usu,deleted_at=None)  # Obtener el objeto de usuario
            trabajo_objeto = trabajo  # Obtener el objeto del trabajo, completa esta línea con los detalles adecuados
            
            curriculum = Curriculums.objects.get(nombre_usu=usuarios.nombre_usu,deleted_at=None)
            puntos_totales = puntos_candidato + curriculum.puntaje
            
            area_candidato = curriculum.area
            
            print(usuarios)
            # Crear un nuevo Candidato y guardar los valores
            candidato = Candidatos(
                candidato=usuario_objeto,
                trabajo=trabajo_objeto,
                puntos_candidato=puntos_totales,
                area=area_candidato
            )
            
            candidato.save()

        # Puedes redirigir a una página de confirmación o a donde desees
        return redirect('Registro_exitoso')

    return render(request, 'tu_template.html')

def detalle_trabajo(request, trabajo_id):
    # Obtén el trabajo específico o muestra un error 404 si no existe
    trabajo = Trabajos.objects.get(id=trabajo_id)

    # Pasa el trabajo al contexto de la plantilla
    context = {'trabajo': trabajo}

    # Renderiza la plantilla de detalle
    return render(request, 'html/detalle_trabajo.html', context)

def aplicar_trabajo(request, trabajo_id):
    trabajo = Trabajos.objects.get(id=trabajo_id)
    area_trabajo = trabajo.area

    if request.method == 'POST':
        nombre_usu = request.session.get('nombre_usu')  # Acceder a la variable de sesión 'nombre_usu'

        if nombre_usu:
            usuario = Usuarios.objects.get(nombre_usu=nombre_usu)

            # Filtrar experiencias por área y sumar los puntos
            puntos_experiencias = Experiencias.objects.filter(nombre_usu=nombre_usu, area=area_trabajo, deleted_at=None).aggregate(Sum('puntos'))['puntos__sum'] or 0

            # Filtrar idiomas por área y sumar los puntos
            puntos_idiomas = Idiomas.objects.filter(nombre_usu=nombre_usu, area='Conocimiento idiomatico',deleted_at=None).aggregate(Sum('puntos'))['puntos__sum'] or 0

            # Filtrar habilidades por área y sumar los puntos
            puntos_habilidades = Habilidades.objects.filter(nombre_usu=nombre_usu, area=area_trabajo,deleted_at=None).aggregate(Sum('puntos'))['puntos__sum'] or 0

            # Filtrar educaciones por área y sumar los puntos
            puntos_educaciones = Educaciones.objects.filter(Q(nombre_usu=nombre_usu, area=area_trabajo,deleted_at=None) | Q(nombre_usu=nombre_usu, area='Conocimiento escolar base (general/generalista)'),deleted_at=None).aggregate(Sum('puntos'))['puntos__sum'] or 0

            # Sumar los puntos totales
            puntos_totales = puntos_experiencias + puntos_idiomas + puntos_habilidades + puntos_educaciones

            # Crear una instancia de Aplicaciones y guardar los datos
            aplicacion = Aplicaciones(
                aplicante=usuario,
                trabajo=trabajo,
                puntos_aplicante=puntos_totales
            )
            aplicacion.save()

            # Puedes agregar un mensaje de éxito si lo deseas
            messages.success(request, 'Aplicación enviada con éxito.')

            return redirect('Aplicacion_exitosa')
        else:
            # Puedes manejar el caso en que 'nombre_usu' no esté en la sesión
            messages.error(request, 'Error al enviar la aplicación.')

    return render(request, 'tu_template.html', {'trabajo': trabajo})

def cancelar_aplicacion(request, aplicacion_id):
    # Obtén la aplicación a cancelar
    aplicacion = Aplicaciones.objects.get(id=aplicacion_id)

    # Asegúrate de que la aplicación pertenezca al usuario actual
    if aplicacion.aplicante.nombre_usu != request.session.get('nombre_usu'):
        # Si no pertenece, podrías mostrar un mensaje de error o redirigir a alguna otra parte
        return redirect('alguna_otra_vista')

    # Elimina la aplicación
    aplicacion.deleted_at = timezone.now()
    aplicacion.save()

    # Redirige a alguna otra vista o página de éxito
    return redirect('Mis_aplicaciones')

def actualizar_curriculum(request):
    nom_usu = request.session.get('nombre_usu')
    usuario = Usuarios.objects.get(nombre_usu=nom_usu)
    curriculum = Curriculums.objects.get(nombre_usu=usuario)

    if request.method == 'POST':
        new_nombre_completo = request.POST['nombre']
        new_correo = request.POST['correo']
        new_telefono = request.POST['telefono']
        new_area = request.POST.get('areaCurr', None)
        
        if new_area == None:
            new_area = curriculum.area
        
        curriculum.nombre_completo = new_nombre_completo
        curriculum.email = new_correo
        curriculum.telefono = new_telefono
        curriculum.area = new_area
        curriculum.save()

    return redirect('Registro_curriculum')

def actualizar_experiencia(request,experiencia_id):
    experiencia = Experiencias.objects.get(id=experiencia_id)

    if request.method == 'POST':
        new_empresa = request.POST['empresa']
        new_puesto = request.POST['puesto']
        new_fecha_inicio = request.POST['fechaInicio']
        new_fecha_termino = request.POST['fechaTermino']
        new_area = request.POST.get('area', None)
        
        if new_fecha_inicio == '':
            new_fecha_inicio = experiencia.desde
        if new_fecha_termino == '':
            new_fecha_termino = experiencia.hasta
        if new_area == None:
            new_area = experiencia.area
        
        experiencia.empresa = new_empresa
        experiencia.puesto = new_puesto
        experiencia.desde = new_fecha_inicio
        experiencia.hasta = new_fecha_termino
        experiencia.area = new_area
        experiencia.save()

    return redirect('Registro_curriculum')

def actualizar_habilidad(request, habilidad_id):
    habilidad = Habilidades.objects.get(id=habilidad_id)
    
    if request.method == 'POST':
        new_habilidad = request.POST['habilidad']
        new_nivel = request.POST.get('nivel', None)
        new_area = request.POST.get('area', None)
        
        if new_nivel == None:
            new_nivel = habilidad.nivel
        if new_area == None:
            new_area = habilidad.area

        habilidad.habilidad = new_habilidad
        habilidad.nivel = new_nivel
        habilidad.area = new_area
        habilidad.save()

    return redirect('Registro_curriculum')

def actualizar_idioma(request,idioma_id):
    idioma = Idiomas.objects.get(id=idioma_id)
    
    if request.method == 'POST':
        new_idioma = request.POST['idioma']
        new_nivel = request.POST.get('nivel_idioma',None)
        
        if new_nivel == None:
            new_nivel = idioma.nivel_idioma
        
        idioma.idioma = new_idioma
        idioma.nivel_idioma = new_nivel
        idioma.save()
        
    return redirect('Registro_curriculum')

def actualizar_educacion(request,educacion_id):
    educacion = Educaciones.objects.get(id=educacion_id)
    
    if request.method == 'POST':
        new_nivel_edu = request.POST.get('nivel_educacion', None)
        new_nombre_i = request.POST['nombre_instituto']
        new_curso_i = request.POST['curso_inicio']
        new_fecha_i = request.POST.get('fecha_inicio', None)
        new_curso_t = request.POST['curso_termino']
        new_fecha_t = request.POST.get('fecha_termino', None)
        
        if new_fecha_i == None or new_fecha_i == '2001-01-01':
            new_fecha_i = educacion.desde
        if new_fecha_t == None or new_fecha_t == '2001-01-01':
            new_fecha_t = educacion.hasta
        if new_nivel_edu == None:
            new_nivel_edu = educacion.nivel_educacion
        
        educacion.nivel_educacion = new_nivel_edu
        educacion.nombre_instituto = new_nombre_i
        educacion.curso = new_curso_i
        educacion.desde = new_fecha_i
        educacion.curso_termino = new_curso_t
        educacion.hasta = new_fecha_t
        educacion.save()
        
    return redirect('Registro_curriculum')

def mostrar_perfil(request, id_empleado):
    # Obtener el usuario desde la base de datos 
    usuario = Usuarios.objects.get(nombre_usu=id_empleado,deleted_at=None)
    curriculum = Curriculums.objects.get(nombre_usu=usuario,deleted_at=None)
    experiencias = Experiencias.objects.filter(nombre_usu=usuario,deleted_at=None)
    habilidades = Habilidades.objects.filter(nombre_usu=usuario,deleted_at=None)
    idiomas = Idiomas.objects.filter(nombre_usu=usuario,deleted_at=None)
    educacion = Educaciones.objects.filter(nombre_usu=usuario,deleted_at=None)

    # Extraer los campos que quieres mostrar
    nombre_completo = f"{usuario.nombre} {usuario.apellido_p} {usuario.apellido_m}"
    genero = usuario.genero
    direccion = usuario.direccion
    telefono = curriculum.telefono
    email = curriculum.email
    rut = f"{usuario.rut}-{usuario.dv}"

    # Crear un diccionario con la información a pasar al template
    contexto = {
        'nombre_completo': nombre_completo,
        'genero': genero,
        'direccion': direccion,
        'rut': rut,
        'curriculum':curriculum,
        'experiencias':experiencias,
        'habilidades':habilidades,
        'idiomas':idiomas,
        'educaciones': educacion,
        'telefono': telefono,
        'email': email
    }

    # Renderizar el template con el contexto
    return render(request, 'html/perfil_empleado.html', contexto)

def ver_perfil(request):
    
    nombre_usuario = request.session.get('nombre_usu')
    # Obtener el usuario desde la base de datos
    usuario = Usuarios.objects.get(nombre_usu=nombre_usuario)

    # Calcular la edad (esto es un ejemplo, asegúrate de ajustar la lógica según tus necesidades)
    edad = usuario.edad

    # Crear un diccionario con la información a pasar al template
    contexto = {
        'nombre_completo': f"{usuario.nombre} {usuario.apellido_p} {usuario.apellido_m}",
        'nombre_usu': usuario.nombre_usu,
        'genero': usuario.genero,
        'edad': edad,
        'email': usuario.email,
        'telefono': usuario.telefono,
    }

    # Renderizar el template con el contexto
    return render(request, 'html/Mi_perfil.html', contexto)

def editar_perfil(request):
    nombre_usuario =request.session.get('nombre_usu')
    # Obtener el usuario desde la base de datos
    usuario = Usuarios.objects.get(nombre_usu=nombre_usuario)

    if request.method == 'POST':
        # Actualizar los datos del usuario con los datos del formulario
        usuario.nombre = request.POST.get('nombre_completo', '')
        usuario.nombre_usu = request.POST.get('nombre_usu', '')
        usuario.genero = request.POST.get('genero', '')
        usuario.edad = request.POST.get('edad', '')
        usuario.email = request.POST.get('email', '')
        usuario.telefono = request.POST.get('telefono', '')
        
        # Guardar los cambios en la base de datos
        usuario.save()

        # Redireccionar a la página de perfil después de editar
        return redirect('ver_perfil', nombre_usuario=nombre_usuario)

    # Renderizar el formulario para editar el perfil
    contexto = {
        'nombre_completo': f"{usuario.nombre} {usuario.apellido_p} {usuario.apellido_m}",
        'nombre_usu': usuario.nombre_usu,
        'genero': usuario.genero,
        'edad': usuario.edad,
        'email': usuario.email,
        'telefono': usuario.telefono,
    }

    return render(request, 'html/editar_perfil.html', contexto)

def guardar_perfil(request):
    nombre_usuario = request.session.get('nombre_usu')
    # Obtener el usuario desde la base de datos
    usuario = Usuarios.objects.get(nombre_usu=nombre_usuario)

    if request.method == 'POST':
        # Actualizar los datos del usuario con los datos del formulario
        usuario.nombre = request.POST.get('nombre_completo', '')
        usuario.nombre_usu = request.POST.get('nombre_usu', '')
        usuario.edad = request.POST.get('edad', '')
        usuario.email = request.POST.get('email', '')
        usuario.telefono = request.POST.get('telefono', '')
        
        genero = request.POST.get('genero', '')
        if genero == 'Otro':
            usuario.genero = request.POST.get('otro_genero', '')
        else:
            usuario.genero = genero
        
        # Guardar los cambios en la base de datos
        usuario.save()

        # Redireccionar a la página de perfil después de editar
        return redirect('ver_perfil')

    # Si no es una solicitud POST, redireccionar a algún lugar adecuado
    # Puedes ajustar esto según tu lógica, por ejemplo, redirigir a la página de edición nuevamente.
    return redirect('ver_perfil')

def to_pdf(request):
    # Obtener datos del formulario POST
    nombre_usuario = request.session.get('nombre_usu')
    usuario = Usuarios.objects.get(nombre_usu=nombre_usuario)
    curriculum = Curriculums.objects.get(nombre_usu=usuario)
    experiencias = Experiencias.objects.filter(nombre_usu=usuario)
    habilidades = Habilidades.objects.filter(nombre_usu=usuario)
    idiomas = Idiomas.objects.filter(nombre_usu=usuario)
    educaciones = Educaciones.objects.filter(nombre_usu=usuario)

    # Crear un objeto BytesIO para almacenar el PDF
    buffer = BytesIO()

    # Crear el objeto PDF usando reportlab
    p = canvas.Canvas(buffer)

    # Agregar contenido al PDF con la información de tu modelo
    p.drawString(100, 800, f"Nombre Completo: {curriculum.nombre_completo}")
    p.drawString(100, 780, f"Email: {curriculum.email}")
    # Agrega más líneas según sea necesario para otros campos

    # Ejemplo de cómo agregar información de experiencias
    y_position = 750
    for experiencia in experiencias:
        p.drawString(100, y_position, f"Empresa: {experiencia.empresa}")
        p.drawString(100, y_position - 20, f"Puesto: {experiencia.puesto}")
        # Agrega más líneas según sea necesario para otros campos de experiencia
        y_position -= 40

    # Agregar sección de habilidades
    y_position -= 20  # Espacio entre secciones
    p.drawString(100, y_position, "Habilidades:")
    for habilidad in habilidades:
        p.drawString(120, y_position - 20, f"Habilidad: {habilidad.habilidad}")
        p.drawString(120, y_position - 40, f"Nivel: {habilidad.nivel}")
        p.drawString(120, y_position - 60, f"Área: {habilidad.area}")
        y_position -= 80

    # Agregar sección de idiomas
    y_position -= 20  # Espacio entre secciones
    p.drawString(100, y_position, "Idiomas:")
    for idioma in idiomas:
        p.drawString(120, y_position - 20, f"Idioma: {idioma.idioma}")
        p.drawString(120, y_position - 40, f"Nivel de Idioma: {idioma.nivel_idioma}")
        p.drawString(120, y_position - 60, f"Área: {idioma.area}")
        y_position -= 80

    # Agregar sección de educaciones
    y_position -= 20  # Espacio entre secciones
    p.drawString(100, y_position, "Educación:")
    for educacion in educaciones:
        p.drawString(120, y_position - 20, f"Nivel de Educación: {educacion.nivel_educacion}")
        p.drawString(120, y_position - 40, f"Instituto: {educacion.nombre_instituto}")
        p.drawString(120, y_position - 60, f"Curso: {educacion.curso}")
        p.drawString(120, y_position - 80, f"Fecha de Inicio: {educacion.desde}")
        p.drawString(120, y_position - 100, f"Fecha de Finalización: {educacion.hasta}")
        y_position -= 120

    # Guardar el objeto PDF
    p.showPage()
    p.save()

    # Mover el puntero del buffer al principio
    buffer.seek(0)

    # Crear una respuesta HTTP con el contenido del PDF
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=curriculum.pdf'

    return response

def eliminar_curriculum(request):
    nombre_usuario = request.session.get('nombre_usu')
    usuario = Usuarios.objects.get(nombre_usu=nombre_usuario,deleted_at=None)

    # Obtén el currículum del usuario actual
    curriculum = Curriculums.objects.get(nombre_usu=usuario,deleted_at=None)

    # Marca el currículum como eliminado
    curriculum.delete()
    Experiencias.objects.filter(nombre_usu=usuario).update(deleted_at=timezone.now())
    Habilidades.objects.filter(nombre_usu=usuario).update(deleted_at=timezone.now())
    Idiomas.objects.filter(nombre_usu=usuario).update(deleted_at=timezone.now())
    Educaciones.objects.filter(nombre_usu=usuario).update(deleted_at=timezone.now())
    
    calcular_puntaje(usuario)

    return redirect('Info_curriculum')

def eliminar_experiencia(request, experiencia_id):
    try:
        # Obtener la experiencia laboral a eliminar
        experiencia = Experiencias.objects.get(id=experiencia_id)
        
        nombre_usuario = request.session.get('nombre_usu')
        usuario = Usuarios.objects.get(nombre_usu=nombre_usuario)
        # Puedes comparar la experiencia con el usuario actual o aplicar tus propias reglas de verificación

        # Eliminar la experiencia (marcar como eliminada si estás utilizando "soft delete")
        experiencia.deleted_at = timezone.now()
        experiencia.save()
        
        calcular_puntaje(usuario)

        # Redirigir a alguna vista de éxito
        return redirect('Registro_curriculum')
    except Experiencias.DoesNotExist:
        # Manejar la situación donde la experiencia no existe
        return redirect('nombre_de_tu_vista_error')
    
def eliminar_educacion(request, educacion_id):
    try:
        # Obtener la educación a eliminar
        educacion = Educaciones.objects.get(id=educacion_id)

        # Verificar que la educación pertenezca al usuario actual (si es necesario)
        # Puedes comparar la educación con el usuario actual o aplicar tus propias reglas de verificación
        
        nombre_usuario = request.session.get('nombre_usu')
        usuario = Usuarios.objects.get(nombre_usu=nombre_usuario)

        # Eliminar la educación (marcar como eliminada si estás utilizando "soft delete")
        educacion.deleted_at = timezone.now()
        educacion.save()
        
        calcular_puntaje(usuario)

        # Redirigir a alguna vista de éxito
        return redirect('Registro_curriculum')
    except Educaciones.DoesNotExist:
        # Manejar la situación donde la educación no existe
        return redirect('nombre_de_tu_vista_error')
    
def eliminar_habilidad(request, habilidad_id):
    try:
        # Obtener la habilidad a eliminar
        habilidad = Habilidades.objects.get(id=habilidad_id)

        # Verificar que la habilidad pertenezca al usuario actual (si es necesario)
        # Puedes comparar la habilidad con el usuario actual o aplicar tus propias reglas de verificación
        
        nombre_usuario = request.session.get('nombre_usu')
        usuario = Usuarios.objects.get(nombre_usu=nombre_usuario)

        # Eliminar la habilidad (marcar como eliminada si estás utilizando "soft delete")
        habilidad.deleted_at = timezone.now()
        habilidad.save()
        
        calcular_puntaje(usuario)

        # Redirigir a alguna vista de éxito
        return redirect('Registro_curriculum')
    except Habilidades.DoesNotExist:
        # Manejar la situación donde la habilidad no existe
        return redirect('nombre_de_tu_vista_error')
    
def eliminar_idioma(request, idioma_id):
    try:
        # Obtener el idioma a eliminar
        idioma = Idiomas.objects.get(id=idioma_id)

        # Verificar que el idioma pertenezca al usuario actual (si es necesario)
        # Puedes comparar el idioma con el usuario actual o aplicar tus propias reglas de verificación
        
        nombre_usuario = request.session.get('nombre_usu')
        usuario = Usuarios.objects.get(nombre_usu=nombre_usuario)

        # Eliminar el idioma (marcar como eliminado si estás utilizando "soft delete")
        idioma.deleted_at = timezone.now()
        idioma.save()
        
        calcular_puntaje(usuario)

        # Redirigir a alguna vista de éxito
        return redirect('Registro_curriculum')
    except Idiomas.DoesNotExist:
        # Manejar la situación donde el idioma no existe
        return redirect('nombre_de_tu_vista_error')
    
def eliminar_trabajo(request, trabajo_id):
    try:
        # Obtener el trabajo a eliminar
        trabajo = Trabajos.objects.get(id=trabajo_id,deleted_at=None)

        trabajo.deleted_at=timezone.now()
        trabajo.save()

        # Redirigir a alguna vista de éxito o a donde desees después de eliminar
        return redirect('listado_trabajos')
    except Trabajos.DoesNotExist:
        # Manejar la situación donde el trabajo no existe
        return redirect('nombre_de_tu_vista_error')

def lista_candidatos(request,trabajo_id):
    candidatos = Candidatos.objects.all().order_by('-puntos_candidato')
    trabajo = Trabajos.objects.get(id=trabajo_id,deleted_at=None)
    print(trabajo.titulo)
    curriculums = Curriculums.objects.filter(deleted_at=None)
    area = trabajo.area
        
    context = {'candidatos': candidatos, 'area': area, 'curriculums': curriculums, 'trabajo': trabajo}
    
    return render(request, 'html/candidatos_aptos.html', context)