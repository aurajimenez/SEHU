from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^crear$', crear_modificar_usuario, name ='usuario_crear_modificar'),
    url(r'^modificar/(?P<id_usuario>\d+)$', usuario_modificar, name = 'usuario_modificar'),
    url(r'^modificarP/(?P<id_usuario>\d+)$', perfil_modificar, name = 'perfil_modificar'),
    url(r'^listar$', listarUsuarios, name = 'listar_usuarios'),
    url(r'^perfil/(?P<id_usuario>\d+)$', perfil_usuario, name = 'perfil_usuario'),
    url(r'^login$',Login.as_view() ,name = 'login'),
    url(r'^logout$',Logout ,name = 'logout'),
    url(r'^inactivar/(?P<id_usuario>\d+)$', inactivar_usuario, name = 'inactivar_usuario'),
    url(r'^activar/(?P<id_usuario>\d+)$', activar_usuario, name = 'activar_usuario'),

    #url(r'^$',inicio ,name = 'inicio'),
]