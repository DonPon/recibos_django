from django.db import models

class Tenant(models.Model):
    name = models.CharField(max_length=255)
    dia = models.CharField(max_length=255)
    precio = models.CharField(max_length=255)
    precio_en_letra = models.CharField(max_length=255)
    servicios = models.CharField(max_length=255)
    local = models.CharField(max_length=255)


class Contract(models.Model):
    nombre_arrendatario = models.CharField(max_length=255)
    ine_arrendatario = models.CharField(max_length=255)
    curp_arrendatario = models.CharField(max_length=255)
    celular_arrendatario = models.CharField(max_length=255)
    fecha_inicio_contrato = models.CharField(max_length=255)
    fecha_vencimiento_contrato = models.CharField(max_length=255)

    renta = models.CharField(max_length=255, default="")
    iva = models.CharField(max_length=255, default="")
    total = models.CharField(max_length=255, default="")
    deposito = models.CharField(max_length=255, default="")
    mantenimiento = models.CharField(max_length=255, default="")
    dia_de_pago = models.CharField(max_length=255)

    local = models.CharField(max_length=255)