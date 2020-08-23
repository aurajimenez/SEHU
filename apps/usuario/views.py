from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from historias_usuario.utilidades import verificar_cargo
from django.http import HttpResponse
from django.contrib import messages
from django.urls.base import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import  ListView
#from djagno.views.generic import *
from .forms import *

from .models import Usuario
from apps.Proyecto.models import Proyecto
from apps.Historia.models import Historia
from django.views.generic import FormView

from .forms import CrearUsuarioForm, ModificarUsuarioForm


def inicio(request):
	Usuario.crear_usuario_inicial()

	#if request.user.is_authenticated() == False:
	#	return redirect('login')

	if request.user.is_superuser == True:

		managers = Usuario.objects.filter(cargo="Integrante").count()
		integrantes = Usuario.objects.filter(cargo="Manager").count()
		usuarios_activos = Usuario.objects.filter(is_active=True).count()
		usuarios_inactivos = Usuario.objects.filter(is_active=False).count()

		contexto = {
	        'managers': managers,
	        'integrantes': integrantes,
	        'usuarios_activos': usuarios_activos,
	        'usuarios_inactivos': usuarios_inactivos,
	   	}
	else:

		from django.db.models import Count, Q

		proyectos = Proyecto.objects.filter(Q(creador= request.user) | Q(miembros=request.user)).distinct()
		#proyectos = Proyecto.objects.all()
		historias = proyectos_con_historias = Proyecto.objects.annotate(numero_historias=Count("historias_del_proyecto")).filter(Q(creador= request.user) | Q(miembros=request.user)).filter(numero_historias__gt=0)
		#historias = Historia.objects.all()
		numero_proyectos = proyectos.count()
		numero_historias = historias.count()
		numero_historias_sin_estimar = historias.filter(estado="Sin estimar").count()
		numero_historias_estimadas = historias.filter(estado="Estimada").count()

		contexto = {
	        'numero_proyectos': numero_proyectos,
	        'numero_historias': numero_historias,
	        'numero_historias_estimadas': numero_historias_estimadas,
	        'numero_historias_sin_estimar': numero_historias_sin_estimar,
	   	}

	return render(request, "inicio.html", contexto)

@verificar_cargo(cargos_permitidos=["Administrador"])
def crear_modificar_usuario(request, id_usuario=None):
	usuario = Usuario.verificar_existencia_usuario(id_usuario)
	clase_form = ModificarUsuarioForm
	if not usuario:
		if id_usuario:
			messages.error(request, "No existe el usuario")
			return redirect('listar_usuarios')

		usuario = None
		clase_form = CrearUsuarioForm
	if request.method == 'POST':
		form = clase_form(request.POST,request.FILES, instance = usuario)

		if form.is_valid():
			form.save()
			messages.success(request, 'El usuario ha sido guardado correctamente')
			return redirect('listar_usuarios')
		messages.error(request, "Error al crear el usuario")

	else:
		form = clase_form(instance=usuario)

	return render(request, "crear_modificar_usuario.html", {'form': form})

@verificar_cargo(cargos_permitidos=["Administrador", "Manager", "Integrante"])
def usuario_modificar(request, id_usuario=None):
	usuario = Usuario.verificar_existencia_usuario(id_usuario)
	clase_form = ModificarUsuarioForm
	if not usuario:
		if id_usuario:
			messages.error(request, "No existe el usuario")
			return redirect('listar_usuarios')

		usuario = None
		clase_form = CrearUsuarioForm
	if request.method == 'POST':
		form = clase_form(request.POST,request.FILES, instance = usuario)

		if form.is_valid():
			form.save()
			messages.success(request, 'El usuario ha sido modificado correctamente')
			return redirect('listar_usuarios')
		messages.error(request, "Error al modificar el usuario")

	else:
		form = clase_form(instance=usuario)

	return render(request, "modificar_usuario.html", {'form': form})

@verificar_cargo(cargos_permitidos=["Manager", "Integrante"])
def perfil_modificar(request, id_usuario=None):
	usuario = Usuario.verificar_existencia_usuario(id_usuario)
	clase_form = ModificarMiPerfilForm
	if not usuario:
		if id_usuario:
			messages.error(request, "No existe el usuario")
			return redirect('listar_usuarios')

		usuario = None
		clase_form = CrearUsuarioForm
	if request.method == 'POST':
		form = clase_form(request.POST,request.FILES, instance = usuario)

		if form.is_valid():
			form.save()
			messages.success(request, 'El usuario ha sido modificado correctamente')
			return redirect('listar_usuarios')
		messages.error(request, "Error al modificar el usuario")

	else:
		form = clase_form(instance=usuario)

	return render(request, "modificar_usuario.html", {'form': form})

def listarUsuarios(request):
	listar_usuarios = Usuario.objects.all().exclude(cargo= 'Administrador',is_active= False)
	return render(request, "listar_usuarios.html", {
		'listar_usuarios': listar_usuarios,
		})

@verificar_cargo(cargos_permitidos=["Administrador"])
def activar_usuario(request, id_usuario):
	try:
		usuario = Usuario.objects.get(id=id_usuario)
		usuario.is_active= True
		usuario.save()
		messages.success(request, "El usuario ha sido activado correctamente")
	except Usuario.DoesNotExist:
		messages.error(request, "El usuario solicitado no existe")
	return redirect('listar_usuarios')

@verificar_cargo(cargos_permitidos=["Administrador"])
def inactivar_usuario(request, id_usuario):
	try:
		usuario = Usuario.objects.get(id=id_usuario)
		usuario.is_active= False
		usuario.save()
		messages.success(request, "El usuario ha sido activado correctamente")
	except Usuario.DoesNotExist:
		messages.error(request, "El usuario solicitado no existe")
	return redirect('listar_usuarios')

	
def perfil_usuario(request, id_usuario):
	from django.shortcuts import get_object_or_404
	try:

		usuario = get_object_or_404(Usuario, pk=id_usuario)
		username =usuario.username
		cargo = usuario.cargo
		first_name = usuario.first_name
		last_name = usuario.last_name
		email = usuario.email
		skills = usuario.skills
		enfoque = usuario.enfoque
		acerca_de_mi = usuario.acerca_de_mi

		contexto = {
			"usuario": usuario, # poner este solo
            }

	except Usuario.DoesNotExist:
		messages.error(request, "El usuario requerido no existe")
		return redirect('listarUsuarios')

	return render(request, 'perfil_usuario.html',contexto)

class Login(FormView):
	form_class = LoginForm
	template_name = 'login.html'

	# funcion que se ejecuta antes de ejecutar la vista, sirve para revisar permisos, ver si el objeto que se busca existe.
	def dispatch(self, request, *args, **kwargs):
		return super(Login, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		mensaje = ""
		user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
		if user is not None:
			if user.is_active:
				self.success_url = reverse_lazy('inicio')
				login(self.request, user)
				usuario = get_object_or_404(Usuario, pk=self.request.user.pk)
				usuario.save()
				return super(Login, self).form_valid(form)
			else:
				mensaje = "El usuario o la contraseña son incorrectos"
		else:
			mensaje = "El usuario o la contraseña son incorrectos"
		form.add_error('username', mensaje)
		print(mensaje)
		messages.add_message(self.request, messages.ERROR, mensaje)
		return super(Login, self).form_invalid(form)

	def form_invalid(self, form):
		messages.add_message(self.request, messages.ERROR, "El usuario  o la contraseña son incorrectos")
		return super(Login, self).form_invalid(form)


@login_required
def Logout(request):
    logout(request)
    return redirect('login')