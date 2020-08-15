from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^crear/(?P<id_proyecto>\d+)$', crearHistoria, name ='historia_crear'),
    url(r'^modificar/(?P<id_historia>\d+)$', modificarHistoria, name ='modificarHistoria'),
    url(r'^listar$', listarHistorias, name = 'listar_historias'),
    url(r'^estimar/(?P<id_historia>\d+)$', estimarHistoria, name = 'estimarHistoria'),
    url(r'^criterios/(?P<id_historia>\d+)$', criteriosHistoria, name = 'criteriosHistoria'),
    url(r'^perfil/(?P<id_historia>\d+)$', perfil_historia, name = 'perfil_historia'),
]