from django.db import models

class Usuarios(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    rut = models.IntegerField(null=True, blank=True)
    dv = models.CharField(max_length=1, null=True, blank=True)
    contrasena = models.TextField(null=False, blank=False)
    email = models.EmailField(max_length=10, null=False, blank=False, unique=True)
    nivel_cuenta = models.IntegerField(null=True, blank=True)
    fecha_nac = models.DateField(null=False, blank=False)
    edad = models.IntegerField(null=False, blank=False)
    nombre = models.CharField(max_length=54, null=True, blank=True)
    apellido_p = models.CharField(max_length=54, null=True, blank=True)
    apellido_m = models.CharField(max_length=54, null=True, blank=True)
    telefono = models.CharField(max_length=14, null=True, blank=True, unique=True)
    genero = models.CharField(max_length=54, null=True, blank=True)
    nombre_usu = models.CharField(max_length=54, null=True, blank=True, unique=True)
    deleted_at = models.DateTimeField(null=True, blank=True)