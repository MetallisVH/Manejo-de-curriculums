from django import forms

class RegistroEmpleadoForm(forms.Form):
    nombreUsuario = forms.CharField(max_length=50, label='Nombre de usuario')
    correo = forms.EmailField(label='Correo')
    contrasena = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    repetirContrasena = forms.CharField(widget=forms.PasswordInput, label='Repetir contraseña')
    telefono = forms.CharField(max_length=20, required=False, label='Número de teléfono')
    fechaNacimiento = forms.DateField(required=False, label='Fecha de nacimiento')
    genero = forms.ChoiceField(
        choices=[
            ('masculino', 'Masculino'),
            ('femenino', 'Femenino'),
            ('noContestar', 'Prefiero no contestar'),
            ('otro', 'Otro'),
        ],
        label='Género'
    )
    otroGenero = forms.CharField(max_length=54, required=False, label='Otro', widget=forms.TextInput(attrs={'style': 'display:none;'}))

    rut = forms.CharField(max_length=8, label='Rut', required=False)
    dv = forms.CharField(max_length=1, label='DV', required=False)  # Campo para el dígito verificador
    nombre = forms.CharField(max_length=54, label='Nombre', required=True)
    apellidoPaterno = forms.CharField(max_length=54, label='Apellido Paterno', required=True)
    apellidoMaterno = forms.CharField(max_length=54, label='Apellido Materno', required=True)
    direccion = forms.CharField(max_length=54,label='Dirección de su domicilio',required=True)

    def clean(self):
        cleaned_data = super().clean()
        contrasena = cleaned_data.get('contrasena')
        repetir_contrasena = cleaned_data.get('repetirContrasena')

        if contrasena and repetir_contrasena and contrasena != repetir_contrasena:
            raise forms.ValidationError('Las contraseñas no coinciden.')

        return cleaned_data

class RegistroEmpleadorForm(forms.Form):
    nombreUsuarioEmpleador = forms.CharField(max_length=50, label='Nombre de usuario')
    correoEmpleador = forms.EmailField(label='Correo')
    contrasenaEmpleador = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    repetirContrasenaEmpleador = forms.CharField(widget=forms.PasswordInput, label='Repetir contraseña')
    telefonoEmpleador = forms.CharField(max_length=20, required=False, label='Número de teléfono')
    fechaNacimientoEmpleador = forms.DateField(required=False, label='Fecha de nacimiento')
    generoEmpleador = forms.ChoiceField(
        choices=[
            ('masculino', 'Masculino'),
            ('femenino', 'Femenino'),
            ('noContestar', 'Prefiero no contestar'),
            ('otro', 'Otro'),
        ],
        label='Género'
    )
    otroGeneroEmpleador = forms.CharField(max_length=50, required=False, label='Otro', widget=forms.TextInput(attrs={'style': 'display:none;'}))
    
    rut = forms.CharField(max_length=8, label='Rut', required=False)
    dv = forms.CharField(max_length=1, label='DV', required=False)  # Campo para el dígito verificador
    nombre = forms.CharField(max_length=54, label='Nombre', required=True)
    apellidoPaterno = forms.CharField(max_length=54, label='Apellido Paterno', required=True)
    apellidoMaterno = forms.CharField(max_length=54, label='Apellido Materno', required=True)
    direccion = forms.CharField(max_length=54,label='Dirección de su oficina',required=True)

    razonSocial = forms.CharField(max_length=54, label='Razón social')
    rut_emp = forms.CharField(max_length=8, label='RUT de la empresa')
    dv_emp = forms.CharField(max_length=1, label='DV_emp', required=False)
    direccionEmpresa = forms.CharField(max_length=54, label='Dirección de la empresa')

    def clean(self):
        cleaned_data = super().clean()
        contrasenaEmpleador = cleaned_data.get('contrasenaEmpleador')
        repetir_contrasenaEmpleador = cleaned_data.get('repetirContrasenaEmpleador')

        if contrasenaEmpleador and repetir_contrasenaEmpleador and contrasenaEmpleador != repetir_contrasenaEmpleador:
            raise forms.ValidationError('Las contraseñas no coinciden.')

        return cleaned_data
    
class RecuperacionContrasenaForm(forms.Form):
    email = forms.EmailField(label='Correo Electrónico', max_length=100, required=True)
    
class RecuperacionUsuarioForm(forms.Form):
    email = forms.EmailField(label='Correo Electrónico', max_length=100, required=True)
    
class RestablecerContrasenaForm(forms.Form):
    nueva_contrasena = forms.CharField(widget=forms.PasswordInput, label='Nueva Contraseña', max_length=100, required=True)
    confirmar_contrasena = forms.CharField(widget=forms.PasswordInput, label='Confirmar Contraseña', max_length=100, required=True)

    def clean(self):
        cleaned_data = super().clean()
        nueva_contrasena = cleaned_data.get('nueva_contrasena')
        confirmar_contrasena = cleaned_data.get('confirmar_contrasena')

        if nueva_contrasena and confirmar_contrasena and nueva_contrasena != confirmar_contrasena:
            raise forms.ValidationError("Las contraseñas no coinciden. Por favor, inténtalo de nuevo.")

        return cleaned_data