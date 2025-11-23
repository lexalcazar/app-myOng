from django.urls import path

from . import views 

urlpatterns = [
    path('', views.index, name='index'),  # Página principal de socios
    #path('detalle/', detalle_socio, name='detalle_socio'),  # Detalle del socio
]