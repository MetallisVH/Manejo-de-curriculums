from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index_page, name = 'Index_page')
]