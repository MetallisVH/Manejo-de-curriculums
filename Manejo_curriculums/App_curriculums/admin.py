from django.contrib import admin
from .models import Usuarios  # Importa el modelo

# Registra el modelo para que aparezca en el sitio admin
admin.site.register(Usuarios)
