from django.urls import path
from . import views

urlpatterns = [
    path('/', views.Index_page, name = 'Index_page'),
    path('/Home/', views.Home_page, name = 'Home_page'),
    path('/Home/emplogin/', views.Login_empleado, name= 'Login_empleado'),
    path('/Home/contrlogin/', views.Login_empleador, name = 'Login_empleador'),
    path('/Home/regemp/', views.Register_empelado, name = 'Register_empleado'),
    path('/Home/regcontr/', views.Register_empleador, name = 'Register_empleador'),
    path('/Home/regemp/dreg', views.registro_empleado, name = 'registro_empleado'),
    path('/Home/regcontr/ereg', views.registro_empleador, name = 'registro_empleador'),
    path('/Home/emplogin/dauth', views.autenticar_empleado, name = 'autenticar_empleado'),
    path('/Home/contrlogin/eauth', views.autenticar_empleador, name = 'autenticar_empleador'),
    path('/Home/srchjb',views.listado_empleos,name='Listado_trabajos'),
    path('/Home/pubjob',views.publicar_trabajo,name='publicar_trabajo'),
    path('reget/',views.Registro_exitoso,name='Registro_exitoso'),
    path('logout/', views.user_logout, name='user_logout'),
    path('Email_confirm/',views.Email_confirm,name='Email_confirm'),
    path('/Home/listemp',views.listado_aplicantes,name='listado_aplicantes'),
    path('confirmar_email/<str:token>/', views.confirmar_email, name='confirmar_email'),
    path('resetear_contrasena/<str:email>/<str:token>/',views.resetear_contrasena, name='resetear_contrasena'),
    path('enviar_usuario/<str:email>/<str:token>/', views.enviar_usuario, name='enviar_usuario'),
    path('/reset_contrasena/<str:email>/<str:token>/', views.reset_contrasena, name='reset_contrasena'),
    path('Recuperar/',views.recuperar,name='Recuperar'),
    path('Recuperar_contrasena/',views.Recuperar_contrasena,name='Recuperar_contrasena'),
    path('recuperacion_contrasena/',views.recuperacion_contrasena,name='recuperacion_contrasena'),
    path('Recuperar_nombre_usuario/',views.Recuperar_nombre_usuario,name='Recuperar_nombre_usuario'),
    path('recuperar_usu/',views.recuperacion_usuario,name='recuperacion_usuario'),
    path('/Home/cvdm',views.Info_curriculum,name='Info_curriculum'),
    path('/Home/regc',views.Registro_curriculum,name='Registro_curriculum'),
    path('guardar_curriculum/',views.registrar_curriculum,name='guardar_curriculum'),
    path('svex',views.guardar_experiencia,name='guardar_experiencia'),
    path('sved',views.guardar_educacion,name='guardar_educacion'),
    path('svhb',views.guardar_habilidad,name='guardar_habilidad'),
    path('svid',views.guardar_idioma,name='guardar_idioma'),
    path('svjb',views.guardar_trabajo,name='guardar_trabajo'),
    path('jbapp/<int:trabajo_id>/',views.aplicar_trabajo,name='aplicar_trabajo'),
    path('jbdetail/<int:trabajo_id>/',views.detalle_trabajo,name='detalle_trabajo'),
    path('/Home/emplst',views.lista_candidatos,name='Listado_empleados'),
    path('/Home/applist',views.mis_aplicaciones,name='Mis_aplicaciones'),
    path('/Home/trlst',views.lista_trabajos,name='listado_trabajos'),
    path('/Home/appdl/<int:aplicacion_id>/',views.cancelar_aplicacion,name='cancelar_aplicacion'),
    path('/Home/currch',views.Editar_curriculum,name='Editar_curriculum'),
    path('upcur/',views.actualizar_curriculum,name='actualizar_curriculum'),
    path('upxp/<int:experiencia_id>/',views.actualizar_experiencia,name='actualizar_experiencias'),
    path('upap/<int:habilidad_id>/',views.actualizar_habilidad,name='actualizar_habilidad'),
    path('uplg/<int:idioma_id>/',views.actualizar_idioma,name='actualizar_idioma'),
    path('upes/<int:educacion_id>/',views.actualizar_educacion,name='actualizar_educacion'),
    path('showp/<str:id_empleado>/',views.mostrar_perfil,name='Ver_detalles_empleado'),
    path('delxp/<int:experiencia_id>/',views.eliminar_experiencia,name='eliminar_experiencia'),
    path('deledu/<int:educacion_id>/',views.eliminar_educacion,name='eliminar_educacion'),
    path('delap/<int:habilidad_id>/',views.eliminar_habilidad,name='eliminar_habilidad'),
    path('delg/<int:idioma_id>/',views.eliminar_idioma,name='eliminar_idioma'),
    path('deltr/<int:trabajo_id>/',views.eliminar_trabajo,name='eliminar_trabajo'),
    path('showus/',views.ver_perfil,name='ver_perfil'),
    path('edpro/',views.editar_perfil,name='Editar_perfil'),
    path('svpro/',views.guardar_perfil,name='guardar_perfil'),
    path('expc/',views.exp_opciones,name='opciones_exportar'),
    path('expdf/',views.to_pdf,name='to_pdf'),
    path('dltcrr/',views.eliminar_curriculum,name='eliminar_curriculum'),
    path('Error_403/',views.Error_403,name='Error_403'),
]