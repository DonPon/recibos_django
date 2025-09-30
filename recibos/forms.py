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

class ReciboOnDemandForm(forms.Form):
    titulo = forms.ChoiceField(
        choices=[('SR.', 'SR.'), ('SRA.', 'SRA.')],
        label='Título',
        help_text='Seleccione el título del inquilino (ej. SR., SRA.).'
    )
    name = forms.CharField(max_length=255, label='Nombre del inquilino', help_text='Ingrese el nombre completo del inquilino.')
    precio = forms.CharField(max_length=255, label='Monto', help_text='Ingrese el monto del ej. "6,500.00"')
    tipo_recibo = forms.ChoiceField(
        choices=[('deposito', 'DEPÓSITO'), ('anticipo', 'ANTICIPO'), ('apartado', 'APARTADO'), ('renta', 'RENTA'), ('devolucion de deposito', 'DEVOLUCIÓN DE DEPÓSITO')],
        label='Tipo de Recibo',
        help_text='Seleccione el tipo de recibo.'
    )
    propiedad = forms.ChoiceField(
        choices=[
            ('Noche de Paz #14, Colonia Granjas Navidad, Delegación Cuajimalpa, C.P. 05219', 
             'Noche de Paz #14, Colonia Granjas Navidad, Delegación Cuajimalpa, C.P. 05219'),
            ('2do. Retorno de Loma del Recuerdo # 70, Colonia Lomas de Vista Hermosa, Delegación Cuajimalpa, C.P. 05100', 
             '2do. Retorno de Loma del Recuerdo # 70, Colonia Lomas de Vista Hermosa, Delegación Cuajimalpa, C.P. 05100')
        ],
        label='Propiedad',
        help_text='Seleccione el número de la propiedad.'
    )
    local = forms.CharField(max_length=255, label='Local/depto.', help_text='Ingrese sólo el número o letra del local o departamento (ej. 5D, C, etc.)')

class ConvenioTerminacionEntregaForm(forms.Form):
    titulo = forms.ChoiceField(
        choices=[('SR.', 'SR.'), ('SRA.', 'SRA.')],
        label='Título',
        help_text='Seleccione el título del inquilino (ej. SR., SRA.).'
    )
    name = forms.CharField(max_length=255, label='Nombre del inquilino', help_text='Ingrese el nombre completo del inquilino.')
    propiedad = forms.ChoiceField(
        choices=[
            ('Noche de Paz #14, Colonia Granjas Navidad, Delegación Cuajimalpa, C.P. 05219', 
             'Noche de Paz #14, Colonia Granjas Navidad, Delegación Cuajimalpa, C.P. 05219'),
            ('2do. Retorno de Loma del Recuerdo # 70, Colonia Lomas de Vista Hermosa, Delegación Cuajimalpa, C.P. 05100', 
             '2do. Retorno de Loma del Recuerdo # 70, Colonia Lomas de Vista Hermosa, Delegación Cuajimalpa, C.P. 05100')
        ],
        label='Propiedad',
        help_text='Seleccione la propiedad.'
    )
    local = forms.CharField(max_length=255, label='Local/depto.', help_text='Ingrese sólo el número o letra del local o departamento (ej. 5D, C, etc.)')
    comienzo_contrato = forms.CharField(max_length=255, label='Fecha de inicio del contrato', help_text='(ej. 15/05/2023).')
    terminacion_contrato = forms.CharField(max_length=255, label='Fecha de terminación del contrato', help_text='(ej. 14/05/2024).')


# authentication/forms.py
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)