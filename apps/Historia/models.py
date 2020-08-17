from django.contrib.auth.models import AbstractUser
from django.db import models
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from apps.usuario.models import Usuario
from apps.Proyecto.models import *

import math

intercepto = -0.438709995968395

class TaggedHistoria(TaggedItemBase):
	content_object = models.ForeignKey('Historia', on_delete=models.CASCADE,)

class Historia(models.Model):
	ESTADOS = (
		('Estimada','Estimada'),
		('Sin estimar','Sin estimar'),
	)

	nombre = models.CharField(max_length=200, verbose_name="Nombre")
	identificador = models.CharField(max_length=10, verbose_name= "Identificador", help_text="Ejemplo: HU001")
	estado = models.CharField(max_length= 50, choices= ESTADOS, default="Sin estimar")
	quiero = models.CharField(verbose_name='quiero', max_length=1200)
	para = models.CharField(verbose_name='para', max_length=1200)
	#creador = models.ForeignKey(Usuario, related_name="creador")
	actores = models.CharField(max_length= 500, verbose_name= "Actores")
	quiero = models.TextField()
	para = models.TextField()
	criterios_aceptacion = TaggableManager(through=TaggedHistoria, help_text="Criterios de aceptación")
	proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name="historias_del_proyecto")
	estimacionHU = models.FloatField(max_length= 50, null= True, default= 0)
	prioridad = models.IntegerField(null= True, default= 1)

	class Meta:
		unique_together = (("identificador", "proyecto"))

	def __str__(self):
		return self.nombre

	@staticmethod
	def revisar_existencia_historia(id_historia):
		try:
			historia = Historia.objects.get(id=id_historia)
			return historia
		except Exception:
			pass
		return False

	def promedio_estimacion(self, id_historia):
		estimacionTotal = 0
		vez = 0
		#proyecto = Proyecto.objects.get(id=1)
		estimaciones = Estimacion.objects.filter(historiaHH__id=id_historia)

		for estimacion in estimaciones:
			estimacionTotal = estimacionTotal + estimacion.estimacionF
			vez = vez + 1 
			print ("Esta es la estimacion de toda la HU")
		self.estimacionHU = estimacionTotal/vez
		print (estimacionTotal)


class Criterio_Aceptacion(models.Model):
	descripcion = models.CharField(max_length= 500)
	historia = models.ForeignKey(Historia, on_delete= models.CASCADE)

class Estimacion(models.Model):

	OPCIONES = (
		('Si', 'Si'),
		('No', 'No'),
	)


	
	porcentaje_reutilizacion = models.FloatField(max_length= 50, null= True, default=0)
	estimacionF = models.FloatField(max_length= 50, null= True, default=0)
	estimador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
	uso_framework = models.CharField(max_length= 500, choices= OPCIONES)
	historiaHH = models.ForeignKey(Historia, on_delete=models.CASCADE,related_name="estimaciones_de_la_historia")
	#Frontend
	requiereUI = models.CharField(max_length= 500, choices= OPCIONES)
	diseno_responsive = models.CharField(max_length= 500, choices= OPCIONES)
	diseno_desarrollo_peticiones_asincronas = models.CharField(max_length= 500, choices= OPCIONES)

	#Backend
	requiereBK  = models.CharField(max_length= 500, choices= OPCIONES)
	interaccion_BD = models.CharField(max_length= 500, choices= OPCIONES)
	interaccion_webservices = models.CharField(max_length= 500, choices= OPCIONES)
	numero_dependencias = models.CharField(max_length= 500, choices= OPCIONES)
	manejo_peticiones = models.CharField(max_length= 500, choices= OPCIONES)
	pruebas_unitarias = models.CharField(max_length= 500, choices= OPCIONES)
	logs = models.CharField(max_length= 500, choices= OPCIONES)
	usoORM = models.CharField(max_length= 500, choices= OPCIONES)


	def calcula_uso_framework(self):
		if self.uso_framework == 'Si':
			return 0.5
		else: 
			return 0.1

	def calcula_diseno_responsive(self):
		if self.diseno_responsive == 'Si':
			return 3.15590299729753
		else: 
			return 0

	def calcula_diseno_desarrollo_peticiones_asincronas(self):
		if self.diseno_desarrollo_peticiones_asincronas == 'Si':
			return 2.68537993846187
		else: 
			return 0

	def calcula_interaccion_BD(self):
		if self.interaccion_BD == 'Si':
			return 1.74060509217283
		else: 
			return 0

	def calcula_interaccion_webservices(self):
		if self.interaccion_webservices == 'Si':
			return 5.16166896369406
		else: 
			return 0

	def calcula_numero_dependencias(self):
		if self.numero_dependencias == 'Si':
			return 1.6076378417706
		else: 
			return 0

	def calcula_manejo_peticiones(self):
		if self.manejo_peticiones == 'Si':
			return -0.00192348489253423
		else: 
			return 0

	def calcula_pruebas_unitarias(self):
		if self.pruebas_unitarias == 'Si':
			return 0.90701874898798
		else: 
			return 0

	def calcula_logs(self):
		if self.logs == 'Si':
			return 4.96720820086259
		else: 
			return 0

	def calcula_usoORM(self):
		if self.usoORM == 'Si':
			return 2.61604848132595
		else: 
			return 0

	def calculo_estimacion(self): 
		proyecto = self.historiaHH.proyecto
		complejidad = ComplejidadDelProyecto.obtener_complejidad_del_proyecto(proyecto, self.estimador)
		a = (self.calcula_diseno_responsive() + self.calcula_diseno_desarrollo_peticiones_asincronas()+ self.calcula_interaccion_BD()+ self.calcula_interaccion_webservices()+self.calcula_numero_dependencias()+self.calcula_manejo_peticiones()+self.calcula_pruebas_unitarias()+ self.calcula_logs()+self.calcula_usoORM() + intercepto+complejidad.sumatoria)
		estimacionF = (a*self.calcula_uso_framework()) - (a*self.porcentaje_reutilizacion*self.calcula_uso_framework())
		print ("Esta es la sumatorio")
		print (complejidad.sumatoria)
		self.estimacionF = estimacionF
		print (estimacionF)

	@staticmethod
	def obtener_estimacion_de_la_hu(historia, usuario):
		try:
			estimacion = Estimacion.objects.get(historiaHH=historia, estimador=usuario)
			return estimacion
		except Exception:
			pass
		return None


