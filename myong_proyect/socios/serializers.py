from rest_framework import serializers

from socios.dni_utils import check_dni
from .models import Socio, Direccion, Tutor, Pago

class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields = '__all__'

class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = '__all__'

class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'

class SocioSerializer(serializers.ModelSerializer):
    """Serializer para lectura: incluye relaciones anidadas"""
    direccion = DireccionSerializer(read_only=True)
    tutor_legal = TutorSerializer(many=True, read_only=True)
    
    class Meta:
        model = Socio
        fields = '__all__'

class SocioCreateSerializer(serializers.ModelSerializer):
    """Serializer para escritura: permite crear socio con dirección"""
    direccion = DireccionSerializer()

    class Meta:
        model = Socio
        exclude = ['fecha_registro']

    def validate_documento_identidad(self, value):
        validator = DNIValidatorSerializer(data={"documento": value})

        if not validator.is_valid():
            raise serializers.ValidationError(
                validator.errors["documento"][0]
            )

        return value

    def create(self, validated_data):
        direccion_data = validated_data.pop('direccion')
        tutores = validated_data.pop('tutor_legal', [])

        direccion = Direccion.objects.create(**direccion_data)
        socio = Socio.objects.create(direccion=direccion, **validated_data)

        if tutores:
            socio.tutor_legal.set(tutores)

        return socio

# ---------------------------------------------------------------
# serializer para validar el dni 
# ---------------------------------------------------------------


class DNIValidatorSerializer(serializers.Serializer):

    documento = serializers.CharField() # Campo para recibir el documento a validar

    def validate_documento(self, value): # Método de validación para el campo documento
        resultado = check_dni(value)

        if not resultado["valido"]: # Si el DNI no es válido, lanzamos una excepción con el error correspondiente
            raise serializers.ValidationError(resultado["error"])

        return value