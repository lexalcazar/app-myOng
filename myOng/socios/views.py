from django.shortcuts import render
from .models import Socio

# Create your views here.
from django.http import HttpResponse

def index(request):
    return HttpResponse("Bienvenido al módulo de socios de MyONG.")

#Detalle socio

def detalle_socio(request):
    socio = {
        'nombre': 'Ana',
        'apellidos': 'Martínez López',
        'dni': '12345678A',
        'direccion': 'Calle Mayor, 12, 2ºA',
        'ciudad': 'Valdepeñas',
        'provincia': 'Ciudad Real',
        'pais': 'España',
    }
    return render(request, 'socios/detalle.html', {'socio': socio})