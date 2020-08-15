from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^crear$', crearProyecto, name ='proyecto_crear_modificar'),
    url(r'^listar$', listarProyectos, name = 'listar_proyectos'),
    url(r'^estimacion$', estimacion_proyecto, name = 'estimacion_proyecto'),
    url(r'^estimar/(?P<id_proyecto>\d+)$', estimar_proyecto, name = 'estimar_proyecto'),
    url(r'^perfil/(?P<id_proyecto>\d+)$', perfil_proyecto, name = 'perfil_proyecto'),
    url(r'^modificar/(?P<id_proyecto>\d+)$' ,modificarProyecto, name= 'modificar_proyecto'),
]