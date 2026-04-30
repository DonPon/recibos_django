# contratos/urls.py
from django.urls import path
from contratos.contratos_views import (Contratos_ContractListView, Contratos_UpdateContractView, 
                             Contratos_AddContractView, Contratos_DeleteContractView, 
                             Contratos_ReminderView, Contratos_CreateContractPDFView,
                             Contratos_UpdateSuccessView)

app_name = 'contratos'

urlpatterns = [
    path('all-contracts/', Contratos_ContractListView.as_view(), name='all_contracts'),
    path('update/<uuid:id>/', Contratos_UpdateContractView.as_view(), name='update_contract'),
    path('update-success/', Contratos_UpdateSuccessView.as_view(), name='contracts_update_success'),
    path('add/', Contratos_AddContractView.as_view(), name='add_contract'),
    path('<uuid:id>/delete/', Contratos_DeleteContractView.as_view(), name='delete_contract'),
    path('reminder/', Contratos_ReminderView.as_view(), name='reminder'),
    path('create_contract_pdf/<uuid:contract_id>/', Contratos_CreateContractPDFView.as_view(), name='create_contract_pdf'),
]