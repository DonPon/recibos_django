from django.urls import path
from on_demand.views import OnDemand_GenerateConvenioTerminacionEntregaView, OnDemand_GenerateReciboView

app_name = 'on_demand'

urlpatterns = [
    path('generate-recibo-on-demand/', OnDemand_GenerateReciboView.as_view(), name='generate_recibo_on_demand'),
    path('generate-terminacion-entrega-una-sola-vez/', OnDemand_GenerateConvenioTerminacionEntregaView.as_view(), name='generate_terminacion_entrega_una_sola_vez'),
]