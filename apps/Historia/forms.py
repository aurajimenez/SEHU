import datetime
from django import forms
from django_select2.forms import Select2Widget
from django.forms import ModelForm, Textarea, TextInput
from historias_usuario.utilidades import MyDateWidget, MyTimeWidget
from django.contrib.auth.forms import UserCreationForm
from .models import Historia
from .models import Proyecto 
from .models import Estimacion, Criterio_Aceptacion
from django.forms import formset_factory


class CrearHistoriaForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(CrearHistoriaForm, self).__init__(*args, **kwargs)
		self.fields['nombre'].label = 'Nombre'
		self.fields['identificador'].label = 'Identificador'
		self.fields['quiero'].label = 'Quiero'
		self.fields['actores'].label = 'Actores'
		self.fields['para'].label = 'Para'
		self.fields['criterios_aceptacion'].label = 'Criterios de aceptación'
		self.fields['prioridad'].label = 'Prioridad'

		self.fields['nombre'].required = True
		self.fields['identificador'].required = True
		self.fields['quiero'].required = True
		self.fields['actores'].required = True
		self.fields['para'].required = True
		self.fields['criterios_aceptacion'].required = True
		self.fields['prioridad'].required = False

	class Meta:
		model = Historia
		fields = ('nombre', 'identificador', 'actores','quiero', 'para','criterios_aceptacion','prioridad',)

class ModificarHistoriaForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(ModificarHistoriaForm, self).__init__(*args, **kwargs)
		self.fields['nombre'].label = 'Nombre'
		self.fields['identificador'].label = 'Identificador'
		self.fields['quiero'].label = 'Quiero'
		self.fields['actores'].label = 'Actores'
		self.fields['para'].label = 'Para'
		self.fields['criterios_aceptacion'].label = 'Criterios de aceptación'
		self.fields['prioridad'].label = 'Prioridad'

		self.fields['nombre'].required = True
		self.fields['identificador'].required = True
		self.fields['quiero'].required = True
		self.fields['actores'].required = True
		self.fields['para'].required = True
		self.fields['criterios_aceptacion'].required = True
		self.fields['prioridad'].required = False

	class Meta:
		model = Historia
		fields = ('nombre', 'identificador', 'actores','quiero', 'para','criterios_aceptacion', 'prioridad',)
		widgets = {
            }

class EstimarHistoriaForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(EstimarHistoriaForm, self).__init__(*args, **kwargs)
		self.fields['requiereUI'].label = 'Requiere Interfaz de Usuario'
		self.fields['requiereBK'].label = 'Requiere Desarrollo Backend'
		self.fields['usoORM'].label = 'Uso ORM'
		self.fields['diseno_responsive'].label = 'Diseño responsive'
		self.fields['diseno_desarrollo_peticiones_asincronas'].label = 'Diseño y desarrollo de peticiones asincronas'
		self.fields['uso_framework'].label = 'Usa framework'
		self.fields['interaccion_BD'].label = 'Interacción con BD'
		self.fields['interaccion_webservices'].label = 'Tiene peticiones diferentes con Servidores externos (Webservice)'
		self.fields['numero_dependencias'].label = 'Tiene dependencias (llamados a otras clases, modelos, entre otros)'
		self.fields['manejo_peticiones'].label = 'Tipos de manejos de peticiones (POST, GET, PUT)'
		self.fields['pruebas_unitarias'].label = 'Pruebas unitarias'
		self.fields['logs'].label = 'Permisos, logs (registro de eventos desde la IP, a que hora, que hizo)'
		self.fields['porcentaje_reutilizacion'].label = 'Porcentaje de reutilización'

		self.fields['requiereUI'].required = True
		self.fields['requiereBK'].required = True
		self.fields['usoORM'].required = True
		self.fields['diseno_responsive'].required = True
		self.fields['diseno_desarrollo_peticiones_asincronas'].required = True
		self.fields['uso_framework'].required = True
		self.fields['interaccion_BD'].required = True
		self.fields['interaccion_webservices'].required = True
		self.fields['numero_dependencias'].required = True
		self.fields['manejo_peticiones'].required = True
		self.fields['pruebas_unitarias'].required = True
		self.fields['logs'].required = True
		self.fields['porcentaje_reutilizacion'].required = True


	class Meta:
		model = Estimacion
		fields = ('requiereBK','requiereUI','uso_framework','diseno_responsive','diseno_desarrollo_peticiones_asincronas','usoORM',
			 'interaccion_BD', 'interaccion_webservices', 'numero_dependencias', 'manejo_peticiones', 'manejo_peticiones', 'pruebas_unitarias', 'logs','porcentaje_reutilizacion')


class CriteriosHistoriaForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(CriteriosHistoriaForm, self).__init__(*args, **kwargs)
		self.fields['descripcion'].label = 'Criterio de aceptación'
		self.fields['descripcion'].required = False

	class Meta:
		model = Criterio_Aceptacion
		fields = ('descripcion',)
		widgets = {
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el criterio de aceptación'
                }
            )
        }
CriteriosHistoriaFormset = formset_factory(CriteriosHistoriaForm, extra=10)