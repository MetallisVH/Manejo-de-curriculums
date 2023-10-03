from django.contrib import admin
from .models import Usuarios,Educaciones,Experiencias,Habilidades,Idiomas,Curriculums,Trabajos  # Importa el modelo

# Registra el modelo para que aparezca en el sitio admin
admin.site.register(Usuarios)
admin.site.register(Educaciones)
admin.site.register(Experiencias)
admin.site.register(Habilidades)
admin.site.register(Idiomas)
admin.site.register(Curriculums)
admin.site.register(Trabajos)