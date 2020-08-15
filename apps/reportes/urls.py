from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^numero_historias_estimadas$', numero_historias_estimadas, name ='numero_historias_estimadas'),
]