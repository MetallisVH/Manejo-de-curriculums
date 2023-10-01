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
    path('logout/', views.user_logout, name='user_logout'),
    path('Email_confirm/',views.Email_confirm,name='Email_confirm'),
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
    path('guardar_curriculum/',views.registrar_curriculum,name='guardar_curriculum'),
    path('Error_403/',views.Error_403,name='Error_403'),
]