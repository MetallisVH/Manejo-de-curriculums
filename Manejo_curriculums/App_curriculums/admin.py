from django.contrib import admin
from .models import Usuarios,Educaciones  # Importa el modelo

# Registra el modelo para que aparezca en el sitio admin
admin.site.register(Usuarios)
admin.site.register(Educaciones)