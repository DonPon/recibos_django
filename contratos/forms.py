# contratos/forms.py
from django import forms
from contratos.models import Contract


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