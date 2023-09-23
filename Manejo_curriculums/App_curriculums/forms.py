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

    def clean(self):
        cleaned_data = super().clean()
        contrasena = cleaned_data.get('contrasena')
        repetir_contrasena = cleaned_data.get('repetirContrasena')

        if contrasena and repetir_contrasena and contrasena != repetir_contrasena:
            raise forms.ValidationError('Las contraseñas no coinciden.')

        return cleaned_data

