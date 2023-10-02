# Generated by Django 4.2.4 on 2023-10-02 21:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('rut', models.IntegerField(blank=True, null=True, unique=True)),
                ('dv', models.CharField(blank=True, max_length=1, null=True)),
                ('direccion', models.CharField(blank=True, max_length=54, null=True)),
                ('contrasena', models.TextField()),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('nivel_cuenta', models.IntegerField(blank=True, null=True)),
                ('fecha_nac', models.DateField()),
                ('edad', models.IntegerField()),
                ('nombre', models.CharField(blank=True, max_length=54, null=True)),
                ('apellido_p', models.CharField(blank=True, max_length=54, null=True)),
                ('apellido_m', models.CharField(blank=True, max_length=54, null=True)),
                ('telefono', models.CharField(blank=True, max_length=14, null=True, unique=True)),
                ('genero', models.CharField(blank=True, max_length=54, null=True)),
                ('nombre_usu', models.CharField(blank=True, max_length=54, null=True, unique=True)),
                ('razon_social', models.CharField(blank=True, default='N/A', max_length=54, null=True)),
                ('rut_empr', models.IntegerField(default=0, unique=True)),
                ('dv_empr', models.CharField(default=-1, max_length=1)),
                ('direccion_empr', models.CharField(default='N/A', max_length=54)),
                ('last_login', models.DateTimeField(blank=True, default=None, null=True, verbose_name='last login')),
                ('oauth', models.IntegerField(blank=True, null=True)),
                ('auth_token', models.TextField(blank=True, null=True, unique=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Idiomas',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('idioma', models.CharField(blank=True, max_length=254)),
                ('nivel_idioma', models.CharField(default='No seleccionado', max_length=54)),
                ('archivo_idioma', models.CharField(blank=True, max_length=2, null=True)),
                ('puntos', models.IntegerField(default=10)),
                ('nombre_usu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_curriculums.usuarios', to_field='nombre_usu')),
            ],
        ),
        migrations.CreateModel(
            name='Habilidades',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('habilidad', models.CharField(blank=True, max_length=254)),
                ('nivel', models.CharField(default='No seleccionado', max_length=14)),
                ('archivo_habilidad', models.CharField(blank=True, max_length=2, null=True)),
                ('puntos', models.IntegerField(default=10)),
                ('nombre_usu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_curriculums.usuarios', to_field='nombre_usu')),
            ],
        ),
        migrations.CreateModel(
            name='Experiencias',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('empresa', models.CharField(blank=True, max_length=254)),
                ('puesto', models.CharField(blank=True, max_length=254)),
                ('desde', models.DateTimeField()),
                ('hasta', models.DateTimeField()),
                ('archivo_experiencia', models.CharField(max_length=2)),
                ('puntos', models.IntegerField(default=10)),
                ('nombre_usu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_curriculums.usuarios', to_field='nombre_usu')),
            ],
        ),
        migrations.CreateModel(
            name='Educaciones',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('nivel_educacion', models.CharField(max_length=54)),
                ('nombre_instituto', models.CharField(blank=True, max_length=254)),
                ('curso', models.CharField(blank=True, max_length=254)),
                ('curso_termino', models.CharField(blank=True, max_length=254)),
                ('desde', models.DateTimeField()),
                ('hasta', models.DateTimeField()),
                ('archivo_educacion', models.CharField(blank=True, max_length=2, null=True)),
                ('puntos', models.IntegerField(default=10)),
                ('nombre_usu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_curriculums.usuarios', to_field='nombre_usu')),
            ],
        ),
        migrations.CreateModel(
            name='Curriculums',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('nombre_completo', models.CharField(blank=True, max_length=162, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('telefono', models.IntegerField(blank=True, null=True, unique=True)),
                ('puntaje', models.IntegerField(blank=True, null=True)),
                ('nombre_usu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_curriculums.usuarios', to_field='nombre_usu')),
            ],
        ),
    ]
