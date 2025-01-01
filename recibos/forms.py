# forms.py
from django import forms
from .models import Tenant, Contract


class MonthForm(forms.Form):
    month = forms.CharField(label='Enter the Month', max_length=255)

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['name', 'dia', 'precio', 'servicios', 'local']
        # fields = ['name', 'dia', 'precio', 'precio_en_letra', 'servicios', 'local']
        widgets = {
            'precio': forms.TextInput(attrs={'placeholder': 'Ej. 6,500.00'}),
            'dia': forms.TextInput(attrs={'placeholder': 'Ej. 05'}),
            'servicios': forms.TextInput(attrs={'placeholder': 'Ej. renta y mantenimiento'}),
        }

# class ContractForm(forms.ModelForm):
#     class Meta:
#         model = Contract
#         fields = [
#             'nombre_arrendatario',
#             'ine_arrendatario',
#             'curp_arrendatario',
#             'celular_arrendatario',
#             'fecha_inicio_contrato',
#             'fecha_vencimiento_contrato',
#             'renta',
#             'iva',
#             'total',
#             'deposito',
#             'mantenimiento',
#             'dia_de_pago',
#             'local'
#         ]

class BaseContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = '__all__'
        widgets = {
            'fecha_inicio_contrato': forms.TextInput(attrs={'placeholder': 'Ej. 15/05/2025'}),
            'fecha_vencimiento_contrato': forms.TextInput(attrs={'placeholder': 'Ej. 15/05/2026'}),
            'iva': forms.TextInput(attrs={'placeholder': 'Ej. 1,500.00'}),
        }

class LocalComercialForm(BaseContractForm):
    class Meta(BaseContractForm.Meta):
        labels = {
            'local': 'Local',
        }

    def __init__(self, *args, **kwargs):
        super(LocalComercialForm, self).__init__(*args, **kwargs)
        self.fields['contract_type'].initial = 'local_comercial'

class DepartamentoForm(BaseContractForm):
    class Meta(BaseContractForm.Meta):
        exclude = ['giro']
        labels = {
            'local': 'Departamento',
        }
    
    def __init__(self, *args, **kwargs):
        super(DepartamentoForm, self).__init__(*args, **kwargs)
        self.fields['contract_type'].initial = 'departamento'

# authentication/forms.py
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)