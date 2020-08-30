from django.db import models
from datetime import date
from django.contrib.postgres.fields import ArrayField
from multiselectfield import MultiSelectField
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from apps.usuario.models import Usuario
#from apps.Historia.models import Historia
from historias_usuario.utilidades import verificar_cargo

import math

class TaggedProyecto(TaggedItemBase):
	content_object = models.ForeignKey('Proyecto',on_delete=models.CASCADE,)

class Proyecto(models.Model):

	OPCIONES = (
		('Si','Si'),
		('No','No'),
		)

	TECNOLOGIAS = (
		('HTML' , 'HTML'),
		('CSS', 'CSS'),
		('ANGULAR', 'ANGULAR'),
		)

	PORCENTAJES = (
		('80% - 100%', '80% - 100%'),
		('60% - 80%', '60% - 80%'),
		('40% - 60%','40% - 60%'),
		('20% - 40%','20% - 40%'),
		)

	GRADOS1 = (
		('AUMENTA', 'AUMENTA'),
		('DISMINUYE','DISMINUYE'),
		('PERMANECE IGUAL','PERMANECE IGUAL'),
		)

	ESTADOS = (
		('Estimado', 'Estimado'),
		('Sin estimar','Sin estimar'),
		('En proceso', 'En proceso'),
		)

	EXPERIENCIAS = (
		('Senior', 'Senior'),
		('Semisenior', 'Semisenior'),
		('Junior', 'Junior'),
		)

	nombre = models.CharField(max_length=200, verbose_name="Nombre", unique=True)
	miembros = models.ManyToManyField(Usuario, related_name="miembros")
	fecha_inicio = models.DateField(verbose_name="Fecha de inicio", blank=False, null=False,)
	fecha_fin = models.DateField(verbose_name="Fecha de finalización", blank=True, null=True)
	tecnologias = TaggableManager(through=TaggedProyecto, help_text="Una lista de tecnologías separadas por comas.")
	enfoque = models.CharField(max_length=100, verbose_name="Enfoque del proyecto", help_text="Ejemplo: Desarrollo")
	area = models.CharField(max_length=100, verbose_name= "Área a la que pertenece el proyecto", help_text="Ejemplo: Salud, Deporte, Gobierno, etc")
	tipo = models.CharField(max_length=100, verbose_name="Tipo de proyecto", help_text="Ejemplo: Web, Móvil, Hibrido")
	descripcion = models.TextField(verbose_name="Descripción")
	creador = models.ForeignKey(Usuario, related_name="creador",on_delete=models.CASCADE,)
	estado = models.CharField(max_length=100, choices=ESTADOS, default="Sin estimar")
	equivalente_puntos_hora = models.FloatField(max_length=50, null=True, default=0)
	total_esfuerzo_horas = models.FloatField(max_length=50, null=True, default=0)

	# variables de estimacion
	#proyecto_unico = models.CharField(max_length= 50,choices=GRADOS1)
	#conocimiento_tecnologias = models.CharField(max_length= 50, choices= OPCIONES)
	#grado_acierto_estimar = models.CharField(max_length= 50, choices= PORCENTAJES)
	#experiencia_estimador = models.CharField(max_length= 500, choices= EXPERIENCIAS)
	#sumatoria = models.FloatField(max_length= 50, null= True, default=0)

	def total_esfuerzo_en_horas(self, _proyecto):
		listar_historias = Historia.objects.filter(proyecto=_proyecto)
		total_esfuerzo_horas = listar_historias.estimacionHU*equivalente_puntos_hora
		self.total_esfuerzo_horas = total_esfuerzo_horas
		print (total_esfuerzo_horas)

	def __str__(self):
		return self.nombre
	
	@staticmethod
	def revisar_existencia_proyecto(proyecto):
		try:
			proyecto = Proyecto.objects.get(id=proyecto)
			return proyecto
		except Exception:
			pass
		return False

class ComplejidadDelProyecto(models.Model):
	GRADOS1 = (
		('AUMENTA', 'AUMENTA'),
		('DISMINUYE','DISMINUYE'),
		('PERMANECE IGUAL','PERMANECE IGUAL'),
		)

	ESTADOS = (
		('Estimado', 'Estimado'),
		('Sin estimar','Sin estimar'),
		('En proceso', 'En proceso'),
		)

	EXPERIENCIAS = (
		('Senior', 'Senior'),
		('Semisenior', 'Semisenior'),
		('Junior', 'Junior'),
		)

	OPCIONES = (
		('Si','Si'),
		('No','No'),
		)

	PORCENTAJES = (
		('80% - 100%', '80% - 100%'),
		('60% - 80%', '60% - 80%'),
		('40% - 60%','40% - 60%'),
		('20% - 40%','20% - 40%'),
		)

	usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE,)
	proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE,)

	proyecto_unico = models.CharField(max_length=50, choices=GRADOS1)
	conocimiento_tecnologias = models.CharField(max_length=50, choices=OPCIONES)
	grado_acierto_estimar = models.CharField(max_length=50, choices=PORCENTAJES)
	experiencia_estimador = models.CharField(max_length=500, choices=EXPERIENCIAS)
	sumatoria = models.FloatField(max_length=50, null=True, default=0)

	class Meta:
		unique_together = (("usuario", "proyecto"),)

	@staticmethod
	def obtener_complejidad_del_proyecto(proyecto, usuario):
		try:
			complejidad = ComplejidadDelProyecto.objects.get(proyecto=proyecto, usuario=usuario)
			return complejidad
		except Exception:
			pass
		return None

	def calcula_proyecto_unico(self):
		if self.proyecto_unico == 'AUMENTA':
			return 1.05454792627761
		elif self.proyecto_unico == 'DISMINUYE':
			return -2.11884091459399
		else: 
			return 1.06429298831647

	def calcula_conocimiento_tecnologias(self):
		if self.conocimiento_tecnologias == 'Si':
			return -2.51817334792353
		else:
			return 0

	def calcula_grado_acierto_estimar(self):
		if self.grado_acierto_estimar == '20% - 40%':
			return 1.39713274982291
		elif self.grado_acierto_estimar == '40% - 60%':
			return -0.551012151785984
		elif self.grado_acierto_estimar == '60% - 80%':
			return -0.470205339808949
		else: 
			return -0.375915258227933

	def calcula_experiencia(self):
		if self.experiencia_estimador == 'Senior':
			return 1.48341236185552
		elif self.experiencia_estimador == 'Semisenior':
			return 2.40647301565872
		else: 
			return -3.88988537751424

	def grado_complejidad(self):
		sumatoria = self.calcula_proyecto_unico() + self.calcula_conocimiento_tecnologias() + self.calcula_grado_acierto_estimar() + self.calcula_experiencia()
		self.sumatoria = sumatoria