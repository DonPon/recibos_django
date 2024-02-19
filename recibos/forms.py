# forms.py
from django import forms
from .models import Tenant, Contract

class MonthForm(forms.Form):
    month = forms.CharField(label='Enter the Month', max_length=255)

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['name', 'dia', 'precio', 'precio_en_letra', 'servicios', 'local']

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['nombre_arrendatario', 'ine_arrendatario', 'fecha_inicio_contrato', 
                  'fecha_vencimiento_contrato', 'dia_de_pago', 'precio','precio_en_letra','servicios','local']
