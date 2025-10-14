from django.db import models

class Tenant(models.Model):
    name = models.CharField(max_length=255)
    dia = models.CharField(max_length=255)
    precio = models.CharField(max_length=255)
    precio_en_letra = models.CharField(max_length=255)
    servicios = models.CharField(max_length=255)
    local = models.CharField(max_length=255)

