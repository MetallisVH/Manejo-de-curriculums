from django.db import models

class Usuarios(models.Model):
    id = models.AutoField(primary_key=True, null=False,unique=True)
    rut = models.IntegerField(null=True, blank=True,unique=True)
    dv = models.CharField(max_length=1, null=True, blank=True)
    direccion = models.CharField(max_length=54,null=True, blank=True)
    contrasena = models.TextField(null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False, unique=True)
    nivel_cuenta = models.IntegerField(null=True, blank=True)
    fecha_nac = models.DateField(null=False, blank=False)
    edad = models.IntegerField(null=False, blank=False)
    nombre = models.CharField(max_length=54, null=True, blank=True)
    apellido_p = models.CharField(max_length=54, null=True, blank=True)
    apellido_m = models.CharField(max_length=54, null=True, blank=True)
    telefono = models.CharField(max_length=14, null=True, blank=True, unique=True)
    genero = models.CharField(max_length=54, null=True, blank=True)
    nombre_usu = models.CharField(max_length=54, null=True, blank=True, unique=True)
    razon_social = models.CharField(max_length=54,null=True,blank=True,default='N/A')
    rut_empr = models.IntegerField(null=False,blank=False,default=0,unique=True)
    dv_empr = models.CharField(max_length=1,null=False,blank=False,default='N/A')
    direccion_empr = models.CharField(max_length=54,null=False,blank=False,default='N/A')
    last_login = models.DateTimeField(verbose_name='last login', blank=True, null=True,default=None)
    oauth = models.IntegerField(null=True,blank=True)
    auth_token = models.TextField(null=True,blank=True,unique=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
class Curriculums(models.Model):
    id = models.AutoField(primary_key=True, null=False,unique=True)
    nombre_completo = models.CharField(max_length=162, null=True, blank= True)
    email = models.EmailField(max_length=254, null=False, blank=False, unique=True)
    nombre_usu = models.ForeignKey(Usuarios, on_delete=models.CASCADE, to_field='nombre_usu')
    telefono = models.IntegerField(null=True,blank=True,unique=True)
    puntaje = models.IntegerField(null=True, blank=True)
    
class Experiencias(models.Model):
    id = models.AutoField(primary_key= True, null=False, unique=True)
    nombre_usu = models.ForeignKey(Usuarios, on_delete=models.CASCADE, to_field='nombre_usu')
    puntos = models.IntegerField(null=True,blank=True)

class Educaciones(models.Model):
    id= models.AutoField(primary_key=True, null=False, unique=True)
    nombre_usu = models.ForeignKey(Usuarios, on_delete=models.CASCADE, to_field='nombre_usu')
    puntos = models.IntegerField(null=True,blank=True)
    
class Habilidades(models.Model):
    id = id= models.AutoField(primary_key=True, null=False, unique=True)
    nombre_usu = models.ForeignKey(Usuarios, on_delete=models.CASCADE, to_field='nombre_usu')
    puntos = models.IntegerField(null=True,blank=True)
    