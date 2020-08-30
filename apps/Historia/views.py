from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls.base import reverse_lazy
from django.views.generic import FormView

from historias_usuario.utilidades import verificar_cargo

from .forms import *
from .models import Usuario, Historia, Estimacion
from .forms import CriteriosHistoriaFormset


@verificar_cargo(cargos_permitidos=["Manager"])
def crearHistoria(request, id_proyecto):
	proyecto = get_object_or_404(Proyecto, pk=id_proyecto)

	if request.method == 'POST':
		form = CrearHistoriaForm(request.POST)
		if form.is_valid():
			historia = form.save(commit=False)
			historia.proyecto = proyecto
			historia.save()
			form.save_m2m()
			messages.success(request, "La historia ha sido registrada correctamente")
			return redirect("listar_historias")
	else:
		form = CrearHistoriaForm()
	return render(request, "crear_modificar_historia.html", {
		"form": form,
	})

@verificar_cargo(cargos_permitidos=["Manager"])
def modificarHistoria(request, id_historia):
	historia = Historia.revisar_existencia_historia(id_historia)
	
	if not historia:
		messages.error(request, "Error al modificar la historia")
		return redirect("listar_historias")

	if request.method == 'POST':
		form = ModificarHistoriaForm(request.POST, instance=historia)
		if form.is_valid():
			form.save()
			messages.success(request, "La historia ha sido guardada correctamente")
			return redirect('listar_historias')
		messages.error(request, "Error al modificar la historia")
	else:
		form = ModificarHistoriaForm(instance=historia)
	return render(request, "modificar_historia.html", {'form': form})

@verificar_cargo(cargos_permitidos=["Manager", "Integrante"])
def estimarHistoria(request, id_historia):
	historia = Historia.revisar_existencia_historia(id_historia)
	
	estimacion_del_usuario = Estimacion.obtener_estimacion_de_la_hu(historia, request.user)

	if not historia:
		messages.error(request, "Error al modificar la historia")
		return redirect("listar_historias")

	if request.method == 'POST':
		form = EstimarHistoriaForm(request.POST, instance=estimacion_del_usuario)
		if form.is_valid():
			estimacion = form.save(commit=False)
			estimacion.estimador = request.user
			estimacion.historiaHH = historia
			estimacion.calculo_estimacion()
			estimacion.save()
			historia.estado = "Estimada"
			historia.promedio_estimacion(id_historia)
			historia.save()
			messages.success(request, "La historia ha sido estimada correctamente")
			return redirect('listar_historias')
		messages.error(request, "Error al estimar la historia")
	else:
		form = EstimarHistoriaForm(instance=estimacion_del_usuario)
	return render(request, "estimar_historia.html", {'form': form})

@verificar_cargo(cargos_permitidos=["Manager", "Integrante"])
def criteriosHistoria(request, id_historia):
	historia = Historia.revisar_existencia_historia(id_historia)
	
	if not historia:
		messages.error(request, "Error al modificar la historia")
		return redirect("listar_historias")

	if request.method == 'POST':
		formset = CriteriosHistoriaFormset(request.POST)
		if formset.is_valid():
			for form in formset:
				criterios = form.save(commit=False)
				if criterios.descripcion in ["", None]:
					continue
				criterios.historia = historia
				criterios.save()

			messages.success(request, "Criterios de aceptación creados correctamente")
			return redirect('listar_historias')
		messages.error(request, "Error al estimar la historia")
	else:
		formset = CriteriosHistoriaFormset()
	return render(request, "criterios_aceptacion.html", {'formset': formset})


@verificar_cargo(cargos_permitidos=["Manager", "Integrante", "ProductO"])
def listarHistorias(request):
	from django.db.models import Count, Q
	proyectos_con_historias = Proyecto.objects.annotate(numero_historias=Count("historias_del_proyecto")).filter(Q(creador= request.user) | Q(miembros=request.user)).filter(numero_historias__gt=0)
	return render(request, "listar_historias.html" , {
		"proyectos_con_historias": proyectos_con_historias,
	})

@verificar_cargo(cargos_permitidos=["Manager", "Integrante", "ProductO"])
def perfil_historia(request, id_historia):
	try:

		historia = Historia.objects.get(id=id_historia)
		nombre =historia.nombre
		identificador = historia.identificador
		quiero = historia.quiero
		criterios_aceptacion = historia.criterios_aceptacion
		estado = historia.estado
		proyecto = historia.proyecto
		estimacion = historia.estimaciones_de_la_historia.all

		contexto = {
			'historia': historia,
            #'estimacion': estimacion,
            #'miembros': miembros,
            #'valor_estimacion': valor_estimacion,
            }

	except Historia.DoesNotExist:
		messages.error(request, "La historia no existe")
		return redirect('listarHistorias')

	return render(request, 'perfil_historia.html',contexto)