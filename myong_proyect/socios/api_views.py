from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import date
from rest_framework import status
from socios.dni_utils import check_dni

from .models import Socio, Pago
from .serializers import SocioSerializer, SocioCreateSerializer, PagoSerializer
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
class SocioViewSet(viewsets.ModelViewSet):
    """
    Gestión completa de socios de la ONG.
    
    Permite crear, consultar, actualizar y eliminar socios.
    Incluye validación automática de DNI y gestión de direcciones anidadas.
    """

    queryset = Socio.objects.select_related('direccion').prefetch_related('tutor_legal')

    def get_serializer_class(self):
        """Usa diferente serializer según la acción"""
        if self.action in ['create', 'update', 'partial_update']:
            return SocioCreateSerializer
        return SocioSerializer
   
    @extend_schema(
        summary="Validar DNI/NIE",
        description="Comprueba si un DNI o NIE español tiene un formato válido y si la letra de control es correcta usando el algoritmo módulo 23.",
        responses={
            200: {
                "description": "DNI validado correctamente",
                "examples": [
                    {
                        "dni": "12345678Z",
                        "valido": True,
                        "letra_correcta": "Z"
                 }
                ]
            },
            400: {
                "description": "Error en la petición",
                "examples": [
                    {
                        "error": "Debe proporcionar un DNI"
                    }
                ]
            }
        }
    )

    @action(detail=False, methods=['post'])
    def check_dni(self, request):
        """
        Valida el formato y letra de un DNI/NIE español.
        
        Usa el algoritmo módulo 23 para verificar la letra de control.
        No requiere autenticación.
        """
        dni = request.data.get("dni")

        if not dni:
            return Response({"error": "Debe proporcionar un DNI"})

        letras = "TRWAGMYFPDXBNJZSQVHLCKE"
        numero = int(dni[:-1])
        letra = dni[-1].upper()

        letra_correcta = letras[numero % 23]

        return Response({
            "dni": dni,
            "valido": letra == letra_correcta,
            "letra_correcta": letra_correcta
        })
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="year",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                required=False,
                default=2024,
                description="Año de consulta para el historial de pagos"
            )
        ]
    )
    @action(detail=True, methods=['get'])
    def pagos(self, request, pk=None):
        """
        Devuelve el historial de pagos de un socio.
        """
        year = request.query_params.get('year', date.today().year)

        pagos = Pago.objects.filter(socio__id=pk, anio=year).order_by('mes')

        return Response({
            "socio": pk,
            "year": year,
            "pagos": PagoSerializer(pagos, many=True).data
        })




#-----------------------------------------------------------------
# endpoint para validar el dni
#-------------------------------------------------------------------


@api_view(['POST'])
def endpoint_check_dni(request):
    documento = request.data.get('documento')
    if not documento:
        return Response(
            {
                "error": "No se proporcionó el campo 'documento'"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    resultado = check_dni(documento)

    # DNI incorrecto
    if not resultado['valido']:
        return Response(
            resultado,
            status=status.HTTP_400_BAD_REQUEST,
            
        )

    # DNI correcto
    return Response(
        resultado,
        status=status.HTTP_200_OK
    
    )


    

class PagoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet de solo lectura para consultar pagos.
    Soporta filtrado por socio y año mediante query params.
    """
    serializer_class = PagoSerializer
    
    def get_queryset(self):
        queryset = Pago.objects.select_related('socio')
        
        # Filtrado opcional por parámetros URL
        socio_id = self.request.query_params.get('socio')
        year = self.request.query_params.get('year', date.today().year)
        
        if socio_id:
            queryset = queryset.filter(socio__id=socio_id)
        
        return queryset.filter(anio=year)

# Endpoint funcional adicional (alternativa a acciones de ViewSet)
@api_view(['GET'])
def pagos_por_socio(request, socio_id):
    """
    Endpoint personalizado para obtener pagos de un socio específico.
    Accesible en: /api/socios/<uuid>/pagos/
    """
    year = request.query_params.get('year', date.today().year)
    pagos = Pago.objects.filter(socio__id=socio_id, anio=year).order_by('mes')
    
    return Response({
        'socio_id': str(socio_id),
        'year': year,
        'pagos': PagoSerializer(pagos, many=True).data,
        'total_meses': pagos.count(),
        'total_pagado': sum(p.monto for p in pagos if p.pagado),
    })