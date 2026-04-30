import os
import sys
import django
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Add the project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Load environment variables from .env
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recibos_django.settings')
django.setup()

from contratos.contratos_models import Contract
from recibos.recibos_models import Tenant
from django.contrib.auth.models import User

def create_superuser():
    if not User.objects.filter(is_superuser=True).exists():
        print("Creating superuser...")
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Superuser created: admin / admin123")
    else:
        print("Superuser already exists.")

def seed_tenants():
    print("Seeding Tenants...")
    Tenant.objects.all().delete()
    
    tenants_data = [
        {
            "name": "Juan Pérez",
            "dia": "5",
            "precio": "5000",
            "precio_en_letra": "Cinco mil pesos 00/100 M.N.",
            "servicios": "Agua, Luz",
            "local": "Local 1"
        },
        {
            "name": "María García",
            "dia": "10",
            "precio": "3500",
            "precio_en_letra": "Tres mil quinientos pesos 00/100 M.N.",
            "servicios": "Internet",
            "local": "Depto 202"
        },
        {
            "name": "Roberto Gómez",
            "dia": "1",
            "precio": "7200",
            "precio_en_letra": "Siete mil doscientos pesos 00/100 M.N.",
            "servicios": "Mantenimiento",
            "local": "Local 5"
        }
    ]
    
    for data in tenants_data:
        Tenant.objects.create(**data)
    print(f"Created {len(tenants_data)} tenants.")

def seed_contracts():
    print("Seeding Contracts...")
    Contract.objects.all().delete()
    
    today = datetime.now()
    one_year_later = today + timedelta(days=365)
    
    contracts_data = [
        {
            "titulo_arrendatario": "SR",
            "nombre_arrendatario": "Carlos Slim",
            "nacionalidad_arrendatario": "MX",
            "identificacion_arrendatario": "ABC123456789",
            "tipo_de_identificacion": "INE",
            "curp_arrendatario": "SLIM670101HDFRRN01",
            "celular_arrendatario": "5512345678",
            "fecha_inicio_contrato": today.strftime("%d/%m/%Y"),
            "fecha_vencimiento_contrato": one_year_later.strftime("%d/%m/%Y"),
            "renta": "15000",
            "iva": "2400",
            "total": "17400",
            "deposito": "15000",
            "mantenimiento": "1000",
            "dia_de_pago": "5",
            "local": "Plaza Carso A1",
            "giro": "Telecomunicaciones",
            "contract_type": "local_comercial"
        },
        {
            "titulo_arrendatario": "SRA",
            "nombre_arrendatario": "Ana Silvia",
            "nacionalidad_arrendatario": "MX",
            "identificacion_arrendatario": "XYZ987654321",
            "tipo_de_identificacion": "pasaporte",
            "curp_arrendatario": "SILV800505MDFRRN02",
            "celular_arrendatario": "5587654321",
            "fecha_inicio_contrato": today.strftime("%d/%m/%Y"),
            "fecha_vencimiento_contrato": one_year_later.strftime("%d/%m/%Y"),
            "renta": "8000",
            "iva": "0",
            "total": "8000",
            "deposito": "8000",
            "mantenimiento": "500",
            "dia_de_pago": "15",
            "local": "Depto 101-B",
            "giro": "Habitacional",
            "contract_type": "departamento"
        }
    ]
    
    for data in contracts_data:
        Contract.objects.create(**data)
    print(f"Created {len(contracts_data)} contracts.")

if __name__ == "__main__":
    print("Starting seeding process...")
    try:
        create_superuser()
        seed_tenants()
        seed_contracts()
        print("Seeding completed successfully!")
    except Exception as e:
        print(f"Error during seeding: {e}")
        import traceback
        traceback.print_exc()
