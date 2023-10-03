from django.db import models
from django.utils import timezone

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
    dv_empr = models.CharField(max_length=1,null=False,blank=False,default=-1)
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
    area = models.CharField(max_length=254,blank=True,null=False,default='Area no especificada')
    puntaje = models.IntegerField(null=True, blank=True)
    
class Experiencias(models.Model):
    id = models.AutoField(primary_key= True, null=False, unique=True)
    nombre_usu = models.ForeignKey(Usuarios, on_delete=models.CASCADE, to_field='nombre_usu')
    empresa = models.CharField(max_length=254,null=False,blank=True)
    puesto = models.CharField(max_length=254,null=False,blank=True)
    desde = models.DateTimeField(null=False,blank=False)
    hasta = models.DateTimeField(null=False,blank=False)
    archivo_experiencia = models.CharField(max_length=2,null=False,blank=False)
    puntos = models.IntegerField(null=False,blank=False,default=10)

class Educaciones(models.Model):
    id = models.AutoField(primary_key=True, null=False, unique=True)
    nombre_usu = models.ForeignKey(Usuarios, on_delete=models.CASCADE, to_field='nombre_usu')
    nivel_educacion = models.CharField(max_length=54,blank=False,null=False)
    nombre_instituto = models.CharField(max_length=254,blank=True,null=False)
    curso = models.CharField(max_length=254,blank=True,null=False)
    curso_termino = models.CharField(max_length=254,blank=True,null=False)
    desde = models.DateTimeField(null=False,blank=False)
    hasta = models.DateTimeField(null=False,blank=False)
    archivo_educacion = models.CharField(max_length=2,null=True,blank=True)
    puntos = models.IntegerField(null=False,blank=False,default=10)
    
class Habilidades(models.Model):
    id = models.AutoField(primary_key=True, null=False, unique=True)
    nombre_usu = models.ForeignKey(Usuarios, on_delete=models.CASCADE, to_field='nombre_usu')
    habilidad = models.CharField(max_length=254,null=False,blank=True)
    nivel = models.CharField(max_length=14,null=False,blank=False,default='No seleccionado')
    archivo_habilidad = models.CharField(max_length=2,null=True,blank=True)
    puntos = models.IntegerField(null=False,blank=False,default=10)
    
class Idiomas(models.Model):
    id = models.AutoField(primary_key=True, null=False, unique=True)
    nombre_usu = models.ForeignKey(Usuarios, on_delete=models.CASCADE, to_field='nombre_usu')
    idioma = models.CharField(max_length=254,blank=True,null=False)
    nivel_idioma = models.CharField(max_length=54,blank=False,null=False,default='No seleccionado')
    archivo_idioma = models.CharField(max_length=2,null=True,blank=True)
    puntos = models.IntegerField(null=False,blank=False,default=10)
    
class Trabajos(models.Model):
    id = models.AutoField(primary_key=True, null=False, unique=True)
    publicador = models.ForeignKey(Usuarios, on_delete=models.CASCADE, to_field='nombre_usu')
    area = models.CharField(max_length=254,blank=True,null=False,default='Area no especificada')
    tipo_trabajo = models.CharField(max_length=54,blank=True,null=True,default='No especificado')
    tipo_contrato = models.CharField(max_length=54,blank=True,null=True,default='No especificado')
    titulo = models.CharField(max_length=54,blank=True,null=False,default='No especificado')
    descripcion = models.TextField(null=False,blank=True,default='Sin descripcion')
    requisitos = models.CharField(max_length=254,null=False,blank=True,default='Sin requisitos')
    ubicacion = models.CharField(max_length=254,null=False,blank=False,default='Falta espesificar ubicacion')
    fecha_publicacion = models.DateTimeField(null=False,blank=False,default=timezone.now)
    fecha_limite = models.DateTimeField(null=True,blank=True)
    remoto = models.CharField(max_length=2,blank=False,null=False,default='NA')
    sueldo = models.IntegerField(null=True,blank=True)
    

class Aplicaciones(models.Model):
    id = models.AutoField(primary_key=True, null=False, unique=True)
    aplicante = models.ForeignKey(Usuarios, on_delete=models.CASCADE, to_field='nombre_usu')
    trabajo = models.ForeignKey(Trabajos, on_delete=models.CASCADE, to_field='id')
    puntos_aplicante = models.IntegerField(null=True,blank=True,default=None)