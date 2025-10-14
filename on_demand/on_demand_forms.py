# on_demand/forms.py
from django import forms


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