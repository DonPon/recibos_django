from django.db import models
import uuid

class Contract(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    CONTRACT_TYPE_CHOICES = [
        ('local_comercial', 'Local Comercial'),
        ('departamento', 'Departamento'),
    ]

    TITLE_CHOICES = [
        ('SR', 'Sr.'),
        ('SRA', 'Sra.'),
    ]

    NATIONALITY_CHOICES = [
        ('MX', 'México'),
        ('AR', 'Argentina'),
        ('BO', 'Bolivia'),
        ('CL', 'Chile'),
        ('CO', 'Colombia'),
        ('CR', 'Costa Rica'),
        ('CU', 'Cuba'),
        ('DO', 'República Dominicana'),
        ('EC', 'Ecuador'),
        ('SV', 'El Salvador'),
        ('GT', 'Guatemala'),
        ('HN', 'Honduras'),
        ('NI', 'Nicaragua'),
        ('PA', 'Panamá'),
        ('PY', 'Paraguay'),
        ('PE', 'Perú'),
        ('PR', 'Puerto Rico'),
        ('UY', 'Uruguay'),
        ('VE', 'Venezuela'),
        ('ES', 'España'),
        ('US', 'Estados Unidos'),
        ('CA', 'Canadá'),
        ('BR', 'Brasil'),
        ('FR', 'Francia'),
        ('DE', 'Alemania'),
        ('IT', 'Italia'),
        ('JP', 'Japón'),
        ('CN', 'China'),
        ('IN', 'India'),
        ('RU', 'Rusia'),
        ('GB', 'Reino Unido'),
        ('AU', 'Australia'),
    ]

    IDENTIFICATION_CHOICES = [
        ("IFE","IFE"),
        ("INE","INE"),
        ("pasaporte","Pasaporte"),
        ("tarjeta de residente","Tarjeta de residente"),
    ]

    DIA_DE_PAGO_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
        ('13', '13'),
        ('14', '14'),
        ('15', '15'),
        ('16', '16'),
        ('17', '17'),
        ('18', '18'),
        ('19', '19'),
        ('20', '20'),
        ('21', '21'),
        ('22', '22'),
        ('23', '23'),
        ('24', '24'),
        ('25', '25'),
        ('26', '26'),
        ('27', '27'),
        ('28', '28'),
        ('29', '29'),
        ('30', '30'),
        ('31', '31'),
    ]
    
    titulo_arrendatario = models.CharField(max_length=5, choices=TITLE_CHOICES)
    nombre_arrendatario = models.CharField(max_length=255)
    nacionalidad_arrendatario = models.CharField(max_length=20, choices=NATIONALITY_CHOICES)
    identificacion_arrendatario = models.CharField(max_length=100, default="")
    tipo_de_identificacion = models.CharField(max_length=100, choices=IDENTIFICATION_CHOICES)
    curp_arrendatario = models.CharField(max_length=255)
    celular_arrendatario = models.CharField(max_length=255)
    fecha_inicio_contrato = models.CharField(max_length=255)
    fecha_vencimiento_contrato = models.CharField(max_length=255)
    renta = models.CharField(max_length=255, default="")
    iva = models.CharField(max_length=255, default="")
    total = models.CharField(max_length=255, default="")
    deposito = models.CharField(max_length=255, default="")
    mantenimiento = models.CharField(max_length=255, default="")
    dia_de_pago = models.CharField(max_length=5, choices=DIA_DE_PAGO_CHOICES)
    local = models.CharField(max_length=255)
    giro = models.CharField(max_length=255, default="")
    contract_type = models.CharField(max_length=20, choices=CONTRACT_TYPE_CHOICES)
