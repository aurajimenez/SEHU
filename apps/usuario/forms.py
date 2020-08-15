import datetime
from django import forms
from historias_usuario.utilidades import MyDateWidget, MyTimeWidget
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class CrearUsuarioForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CrearUsuarioForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Nombres'
        self.fields['last_name'].label = 'Apellidos'
        self.fields['email'].label = 'Correo electrónico'
        self.fields['username'].label = 'Username'
        self.fields['cargo'].label = 'Cargo'
        self.fields['skills'].label = 'Skills'
        self.fields['enfoque'].label = 'Enfoque'

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['username'].required = True
        self.fields['cargo'].required = True
        self.fields['skills'].required = True
        self.fields['enfoque'].required = True

    username = forms.CharField(required=True, label="Número de documento de identificación",
                                  error_messages={'unique': "Ya existe un usuario con este número de documento de identificación" ,
        })
    password1 = forms.CharField(max_length=30, required=True, label="Contraseña", widget=forms.PasswordInput)


    class Meta:
        model = Usuario
        fields = ('username', 'first_name','last_name','email','cargo','skills','enfoque','foto_perfil')

class ModificarUsuarioForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModificarUsuarioForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Nombre'
        self.fields['last_name'].label = 'Apellidos'
        self.fields['email'].label = 'Correo electrónico'
        self.fields['username'].label = 'Username'
        self.fields['foto_perfil'].label = 'Foto de perfil'
        self.fields['cargo'].label = 'Cargo'
        self.fields['skills'].label = 'Skills'
        self.fields['enfoque'].label = 'Enfoque'
        self.fields['acerca_de_mi'].label = 'Acerca de mi'

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['username'].required = True
        self.fields['foto_perfil'].required = False
        self.fields['cargo'].required = False
        self.fields['enfoque'].required = True
        self.fields['skills'].required = True
        self.fields['acerca_de_mi'].required = False

    class Meta:
    	model = Usuario
    	fields = ('username', 'first_name','last_name', 'foto_perfil','email','cargo','skills', 'enfoque', 'acerca_de_mi')

class ModificarMiPerfilForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModificarMiPerfilForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Nombre'
        self.fields['last_name'].label = 'Apellidos'
        self.fields['email'].label = 'Correo electrónico'
        self.fields['foto_perfil'].label = 'Foto de perfil'
        self.fields['skills'].label = 'Skills'
        self.fields['enfoque'].label = 'Enfoque'
        self.fields['acerca_de_mi'].label = 'Acerca de mi'

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['foto_perfil'].required = False
        self.fields['enfoque'].required = True
        self.fields['skills'].required = True
        self.fields['acerca_de_mi'].required = False

    class Meta:
        model = Usuario
        fields = ('first_name','last_name', 'foto_perfil','email','skills', 'enfoque', 'acerca_de_mi')

class LoginForm(forms.Form):

    username = forms.CharField(max_length = 50,
            widget=forms.TextInput(attrs ={
                    'id':'usernameInput',
                    'placeholder': 'Nombre de usuario',
                    'class':'form-control'
                }))
    password = forms.CharField(max_length = 50,
            widget = forms.TextInput(attrs = {
                    'type' : 'password',
                    'id':'passwordInput',
                    'placeholder': 'Contraseña',
                    'class':'form-control'
                }))
