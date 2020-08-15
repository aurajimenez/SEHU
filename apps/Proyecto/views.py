from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from historias_usuario.utilidades import verificar_cargo
from django.http import HttpResponse
from django.urls.base import reverse_lazy
from django.contrib import messages
from django.shortcuts import render, redirect
#from djagno.views.generic import *
from .forms import *
from apps.Historia.models import Historia
from .models import Proyecto
from django.views.generic import FormView

from .forms import CrearProyectoForm, EstimarProyectoForm
from datetime import *
from time import *

@verificar_cargo(cargos_permitidos=["Manager"])
def crearProyecto(request):
    if request.method == 'POST':
        form =CrearProyectoForm(request.POST)
        if form.is_valid():
            proyecto = form.save(commit=False)
            proyecto.creador = request.user
            proyecto.save()
            form.save_m2m()
            messages.success(request, "El proyecto ha sido registrado correctamente")
            return redirect("listar_proyectos")
        messages.error(request, "Error al crear el proyecto")
    else: 
        form = CrearProyectoForm()
    
    return render(request, "crear_modificar_proyecto.html", {
        "form": form,
    })

@verificar_cargo(cargos_permitidos=["Manager", "Integrante"])
def estimar_proyecto(request,id_proyecto):
    proyecto = Proyecto.revisar_existencia_proyecto(id_proyecto)

    complejidad_del_proyecto = ComplejidadDelProyecto.obtener_complejidad_del_proyecto(proyecto, request.user)
    print(complejidad_del_proyecto)

    if request.method == 'POST':
        form = EstimarProyectoForm(request.POST, instance=complejidad_del_proyecto)
        if form.is_valid():             
            complejidad = form.save(commit=False)
            complejidad.usuario = request.user
            complejidad.proyecto = proyecto
            complejidad.grado_complejidad()
            complejidad.estado = "En proceso"
            complejidad.save()
            messages.success(request, "La complejidad del proyecto ha sido registrada correctamente")
            return redirect('listar_proyectos')
        messages.error(request, "Error al definir la complejidad del proyecto")
    else:
        form = EstimarProyectoForm(instance=complejidad_del_proyecto)
    return render(request, "estimar_proyecto.html", {'form': form})

@verificar_cargo(cargos_permitidos=["Manager"])
def modificarProyecto(request, id_proyecto):
    proyecto = Proyecto.revisar_existencia_proyecto(id_proyecto)
    
    if not proyecto:
        messages.error(request, "Error al modificar el proyecto")
        return redirect("listar_proyectos")

    if request.method == 'POST':
        form = ModificarProyectoForm(request.POST, instance=proyecto)
        if form.is_valid():
            form.save()
            messages.success(request, "El proyecto ha sido guardado correctamente")
            return redirect('listar_proyectos')
        messages.error(request, "Error al modificar el proyecto")
    else:
        form = ModificarProyectoForm(instance=proyecto)
    return render(request, "modificar_proyecto.html", {'form': form})

    
@verificar_cargo(cargos_permitidos=["Manager", "Integrante"])
def listarProyectos(request):
    from django.db.models import Q
    listar_proyectos = Proyecto.objects.filter(Q(creador= request.user) | Q(miembros=request.user)).distinct()
    return render(request, "listar_proyectos.html", {
        "listar_proyectos": listar_proyectos,
    })

@verificar_cargo(cargos_permitidos=["Manager", "Integrante"])
def estimacion_proyecto(request):
    from django.db.models import Q
    estimacion_proyecto = Proyecto.objects.filter(Q(creador= request.user) | Q(miembros=request.user)).distinct()

    contexto = {
        'estimacion_proyecto': estimacion_proyecto,
    }

    return render(request,"estimacion_proyecto.html",contexto)   

@verificar_cargo(cargos_permitidos=["Manager", "Integrante"])
def perfil_proyecto(request, id_proyecto):
    try:
        proyecto = Proyecto.objects.get(id=id_proyecto)
        nombre =proyecto.nombre
        miembros = proyecto.miembros
        tecnologias = proyecto.tecnologias
        enfoque = proyecto.enfoque
        area = proyecto.area
        tipo = proyecto.tipo
        listar_historias = obtener_listar_historias(proyecto)
        descripcion = proyecto.descripcion
        listar_miembros = obtener_listar_miembros(proyecto)

        contexto = {
            'proyecto': proyecto,
            'listar_historias': listar_historias,
            'listar_miembros': listar_miembros,
        }

    except Proyecto.DoesNotExist:
        messages.error(request, "El proyecto requerido no existe")
        return redirect('listarProyectos')

    return render(request,'perfil_proyecto.html',contexto)

def obtener_listar_historias(_proyecto):
    listar_historias = Historia.objects.filter(proyecto=_proyecto)
    return listar_historias

def obtener_listar_miembros(_proyecto):
    listar_miembros = Proyecto.miembros
    return listar_miembros