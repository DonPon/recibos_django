# recibos/forms.py
from django import forms
from recibos.models import Tenant


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


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)