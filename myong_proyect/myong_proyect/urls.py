"""
URL configuration for myong_proyect project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
# nuevos imports
from drf_spectacular.views import (
   SpectacularAPIView,      # Descarga del schema
   SpectacularSwaggerView,  # Interfaz Swagger UI
   SpectacularRedocView,    # Interfaz ReDoc
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('socios/', include('socios.urls')),
    path('api/', include('socios.urls_api')),
    # RUTAS DE DOCUMENTACIÓN

    # OpenAPI schema (descarga JSON/YAML)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Swagger UI
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # ReDoc
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
