from django import forms
import datetime
from django.utils import timezone
from django_select2.forms import Select2Widget
from django_select2.forms import Select2MultipleWidget
from datetimewidget.widgets import DateWidget
from datetimewidget.widgets import DateTimeWidget
from historias_usuario.utilidades import MyDateWidget, MyTimeWidget
from .models import *

OPCIONES = (
	('Si','Si'),
	('No','No'),
	)

class CrearProyectoForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(CrearProyectoForm, self).__init__(*args, **kwargs)
		self.fields['nombre'].label = 'Nombre'
		self.fields['tecnologias'].label = 'Tecnologías'
		self.fields['enfoque'].label = 'Enfoque del proyecto'
		self.fields['area'].label = 'Área a la que pertenece el proyecto'
		self.fields['tipo'].label = 'Tipo'
		self.fields['miembros'].label = 'Integrantes'
		self.fields['descripcion'].label = 'Descripción'
		self.fields['fecha_fin'].SelectDateWidget = 'Fecha finalización'
		self.fields['fecha_inicio'].SelectDateWidget = 'Fecha inicio'
		self.fields['equivalente_puntos_hora'].label = 'Equivalente puntos - hora'

		self.fields['nombre'].required = True
		self.fields['tecnologias'].required = True
		self.fields['enfoque'].required = True
		self.fields['area'].required = True
		self.fields['tipo'].required = True
		self.fields['miembros'].required = True
		self.fields['fecha_fin'].required = False
		self.fields['fecha_inicio'].required = True
		self.fields['descripcion'].required = True
		self.fields['equivalente_puntos_hora'].required = True

	class Meta:
		model = Proyecto
		fields = ('nombre', 'tecnologias','descripcion', 'enfoque', 'area', 'tipo', 'equivalente_puntos_hora','miembros', 'fecha_inicio', 'fecha_fin')
		widgets = {
			'fecha_inicio': MyDateWidget(),
			'fecha_fin': MyDateWidget(),
			'miembros': Select2MultipleWidget(),
		}

class ModificarProyectoForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(ModificarProyectoForm, self).__init__(*args, **kwargs)
		self.fields['nombre'].label = 'Nombre'
		self.fields['tecnologias'].label = 'Tecnologías'
		self.fields['enfoque'].label = 'Enfoque'
		self.fields['area'].label = 'Area'
		self.fields['tipo'].label = 'Tipo'
		self.fields['miembros'].label = 'Integrantes'
		self.fields['descripcion'].label = 'Descripción'
		self.fields['equivalente_puntos_hora'].label = 'Equivalente puntos - hora'

		self.fields['nombre'].required = True
		self.fields['tecnologias'].required = True
		self.fields['enfoque'].required = True
		self.fields['area'].required = True
		self.fields['tipo'].required = True
		self.fields['miembros'].required = True
		self.fields['fecha_fin'].required = False
		self.fields['fecha_inicio'].required = False
		self.fields['descripcion'].required = True
		self.fields['equivalente_puntos_hora'].required = True

	class Meta:
		model = Proyecto
		fields = ('nombre', 'tecnologias','descripcion', 'enfoque', 'area', 'tipo', 'equivalente_puntos_hora','miembros', 'fecha_inicio', 'fecha_fin')
		widgets = {
			'fecha_inicio': MyDateWidget(),
			'fecha_fin': MyDateWidget(),
			'miembros': Select2MultipleWidget(),
		}
"""
class EstimarProyecto2Form(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(EstimarProyecto2Form, self).__init__(*args, **kwargs)
		self.fields['proyecto_unico'].label = 'Al estar involucrado en más de un proyecto al tiempo ¿Cómo cree que afecta el esfuerzo de desarrollo?'
		self.fields['conocimiento_tecnologias'].label = '¿Tiene conocimiento previo de las tecnologías del proyecto?'
		self.fields['grado_acierto_estimar'].label = '¿Cuál considera ha sido su grado de acierto en pasadas estimaciones?'
		self.fields['experiencia_estimador'].label = '¿Cuál es su grado de experiencia?'
		#proyecto_unico = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=OPCIONES)

		self.fields['proyecto_unico'].required = True
		self.fields['conocimiento_tecnologias'].required = True
		self.fields['grado_acierto_estimar'].required = True
		self.fields['experiencia_estimador'].required = True

	class Meta:
		model = Proyecto
		fields = ('proyecto_unico', 'conocimiento_tecnologias', 'grado_acierto_estimar','experiencia_estimador')
"""

class EstimarProyectoForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(EstimarProyectoForm, self).__init__(*args, **kwargs)
		self.fields['proyecto_unico'].label = 'Al estar involucrado en más de un proyecto al tiempo ¿Cómo cree que afecta el esfuerzo de desarrollo?'
		self.fields['conocimiento_tecnologias'].label = '¿Tiene conocimiento previo de las tecnologías del proyecto?'
		self.fields['grado_acierto_estimar'].label = '¿Cuál considera ha sido su grado de acierto en pasadas estimaciones?'
		self.fields['experiencia_estimador'].label = '¿Cuál es su grado de experiencia en el ciclo de vida de un proyecto?'
		
		self.fields['proyecto_unico'].required = True
		self.fields['conocimiento_tecnologias'].required = True
		self.fields['grado_acierto_estimar'].required = True
		self.fields['experiencia_estimador'].required = True

	class Meta:
		model = ComplejidadDelProyecto
		fields = ('proyecto_unico', 'conocimiento_tecnologias', 'grado_acierto_estimar','experiencia_estimador')