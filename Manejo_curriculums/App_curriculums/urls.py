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
]