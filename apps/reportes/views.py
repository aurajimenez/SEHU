from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.db.models.aggregates import Count
from django.db.models.functions.datetime import TruncDate
from django.http.response import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView

from historias_usuario.utilidades import verificar_cargo
from apps.Historia.models import *
from apps.Proyecto.models import *
from django.views.generic import FormView

def numero_historias_estimadas(request):
	numero_historias_estimadas = Historia.objects.filter(estado= "Estimada")
	return render(request, "reporte_numero_historias_estimadas.html", {"numero_historias_estimadas": numero_historias_estimadas})

