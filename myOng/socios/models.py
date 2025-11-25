from django.db import models

# Create your models here.
class Socio(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos=models.CharField(max_length=200)
    fecha_nacimiento=models.DateField()
    telefono=models.DecimalField(max_digits=5, decimal_places=0)
    email = models.EmailField()
    fecha_alta = models.DateField(auto_now_add=True)
    menor_edad=models.BooleanField()
    IBAN=models.CharField(max_length=34, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"
   


