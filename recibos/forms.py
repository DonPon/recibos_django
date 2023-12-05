# forms.py
from django import forms
from .models import Tenant

class MonthForm(forms.Form):
    month = forms.CharField(label='Enter the Month', max_length=255)

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['name', 'dia', 'precio', 'precio_en_letra', 'servicios', 'local']