from django.shortcuts import render
from .models import Socio

# Create your views here.
from django.http import HttpResponse

def index(request):
    return HttpResponse("Bienvenido al módulo de socios de MyONG.")

