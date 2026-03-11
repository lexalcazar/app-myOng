from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import SocioViewSet, PagoViewSet, endpoint_check_dni, pagos_por_socio

# Crea el router y registra los ViewSets
router = DefaultRouter()
router.register(r'socios', SocioViewSet, basename='socio')      # Genera /api/socios/
router.register(r'pagos', PagoViewSet, basename='pago')  # Genera /api/pagos/

# Las URLs generadas incluyen:
# /socios/          -> list (GET), create (POST)
# /socios/{id}/     -> retrieve (GET), update (PUT/PATCH), destroy (DELETE)

urlpatterns = [
    
    # Endpoint personalizado para pagos por socio
    path('socios/<uuid:socio_id>/pagos/', pagos_por_socio, name='api_pagos_socio'),
    # Endpoint funcional adicional para validar DNI
    path('socios/check-dni/', endpoint_check_dni, name='api_check_dni'),
    path('', include(router.urls)),
]