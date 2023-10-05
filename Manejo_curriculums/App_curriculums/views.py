from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from .forms import *
from django.utils import timezone
from django.shortcuts import render, redirect
from .models import models ,Usuarios, Curriculums, Experiencias, Educaciones, Habilidades, Idiomas, Trabajos, Aplicaciones
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from datetime import date
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.urls import reverse
from django.http import HttpResponseRedirect
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
        trabajos_recomendados = 0

    return render(request, 'html/Home.html', {'trabajos_recomendados': trabajos_recomendados})

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
    try:
        # Recuperar datos del usuario desde la tabla Curriculums
        nombre_usu = request.session.get('nombre_usu')
        usuario = Curriculums.objects.get(nombre_usu=nombre_usu)

        # Recuperar experiencias laborales, educación, habilidades e idiomas asociadas al usuario
        experiencias_laborales = Experiencias.objects.filter(nombre_usu=nombre_usu)
        educacion = Educaciones.objects.filter(nombre_usu=nombre_usu)
        habilidades = Habilidades.objects.filter(nombre_usu=nombre_usu)
        idiomas = Idiomas.objects.filter(nombre_usu=nombre_usu)
        curriculum = Curriculums.objects.get(nombre_usu=nombre_usu)
        curr_area = curriculum.area

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
    return render(request,'html/Registro_curriculums.html')

def Registro_exitoso(request):
    return render(request, 'html/Registro_exitoso.html')

def publicar_trabajo(request):
    return render(request,'html/Publicar_trabajo.html')

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

def lista_candidatos(request):
    curriculums = Curriculums.objects.all().order_by('-puntaje')
    return render(request, 'html/lista_candidatos.html', {'curriculums': curriculums})

def mis_aplicaciones(request):
    # Obtener el usuario actual
    nombre_usuario = request.session.get('nombre_usu')
    usuario_actual = Usuarios.objects.get(nombre_usu=nombre_usuario)

    # Filtrar las aplicaciones realizadas por el usuario actual
    aplicaciones_usuario = Aplicaciones.objects.filter(aplicante=usuario_actual)

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
    puntaje_experiencias = Experiencias.objects.filter(nombre_usu=usuario).aggregate(Sum('puntos'))['puntos__sum'] or 0
    puntaje_educaciones = Educaciones.objects.filter(nombre_usu=usuario).aggregate(Sum('puntos'))['puntos__sum'] or 0
    puntaje_habilidades = Habilidades.objects.filter(nombre_usu=usuario).aggregate(Sum('puntos'))['puntos__sum'] or 0
    puntaje_idiomas = Idiomas.objects.filter(nombre_usu=usuario).aggregate(Sum('puntos'))['puntos__sum'] or 0

    puntaje_total = puntaje_experiencias + puntaje_educaciones + puntaje_habilidades + puntaje_idiomas
    return puntaje_total

def guardar_educacion(request):
    if request.method == 'POST':
        nivel_educacion = request.POST.get('nivelEducacion')
        nombre_instituto = request.POST.get('instituto')
        cursos = request.POST.get('cursos')
        curso_termino = request.POST.get('cursoTermino') # Nuevo campo
        area = request.POST.get('area')
        
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
            area=area
        )
        educacion.save()
        print(f"Datos guardados correctamente: {educacion}")

        # Aquí puedes hacer algo con los puntos, como almacenarlos en otro modelo o realizar alguna lógica adicional

        # Redirige o responde según tu lógica
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
        
        if fecha_limite == '':
            fecha_limite = None
        
        usuario = request.session.get('nombre_usu')

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
            puntos_experiencias = Experiencias.objects.filter(nombre_usu=nombre_usu, area=area_trabajo).aggregate(Sum('puntos'))['puntos__sum'] or 0

            # Filtrar idiomas por área y sumar los puntos
            puntos_idiomas = Idiomas.objects.filter(nombre_usu=nombre_usu, area='Conocimiento idiomatico').aggregate(Sum('puntos'))['puntos__sum'] or 0

            # Filtrar habilidades por área y sumar los puntos
            puntos_habilidades = Habilidades.objects.filter(nombre_usu=nombre_usu, area=area_trabajo).aggregate(Sum('puntos'))['puntos__sum'] or 0

            # Filtrar educaciones por área y sumar los puntos
            puntos_educaciones = Educaciones.objects.filter(Q(nombre_usu=nombre_usu, area=area_trabajo) | Q(nombre_usu=nombre_usu, area='Conocimiento escolar base (general/generalista)')).aggregate(Sum('puntos'))['puntos__sum'] or 0

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