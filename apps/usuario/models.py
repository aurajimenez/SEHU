from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from django.db import models

def crear_ruta_foto_perfil(instance, filename):
	return "fotos-perfil/%s-%s"%(instance.id, filename.encode('ascii','ignore'))

class TaggedUsuario(TaggedItemBase):
	content_object = models.ForeignKey('Usuario',on_delete=models.CASCADE,)

class Usuario(AbstractUser):
	CARGOS =(
		('Administrador', 'Administrador'),
		('Integrante','Integrante'),
		('Manager','Manager'),
		('ProductO','ProductO'),
		)

	ENFOQUE = (
		('BACKEND', 'BACKEND'),
		('FRONTEND', 'FRONTEND'),
		('FULLSTACK', 'FULLSTACK'),
		('QA','QA'),
		('CEO','CEO')
		)

	username = models.CharField(max_length=20, verbose_name="username", unique=True)
	cargo = models.CharField(max_length=50, choices=CARGOS)
	foto_perfil = models.ImageField(upload_to=crear_ruta_foto_perfil, blank=True, help_text='Seleccione una imagen de perfil')
	first_name = models.CharField(max_length=200, verbose_name="Nombre", unique=False)
	last_name = models.CharField(max_length=200, verbose_name="Apellidos", unique=False)
	email = models.CharField(max_length=200, verbose_name="Correo electrónico", unique=True)
	is_active = models.BooleanField(default=True)
	skills = TaggableManager(through=TaggedUsuario, help_text="Una lista de skills separados por comas.")
	enfoque = models.CharField(max_length=20, choices= ENFOQUE)
	acerca_de_mi = models.CharField(max_length=500, verbose_name="Acerca de mi")

	@staticmethod
	def crear_usuario_inicial():
		total_usuarios = Usuario.objects.all().count()
		if total_usuarios == 0:
			password = "historias"
			user = Usuario.objects.create_user('admin', 'root@gmail.com', password)
			user.set_password(password)
			user.first_name = 'Administrador'
			user.is_superuser = True
			user.is_staff = True
			user.cargo = 'Administrador'
			user.save()

	@staticmethod
	def verificar_existencia_usuario(usuario):
		try:
			usuario = Usuario.objects.get(id=usuario)
			return usuario
		except Exception:
			pass
		return False

	def __str__(self):
		return "%s %s"%(self.first_name, self.last_name)
