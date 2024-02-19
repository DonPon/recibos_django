
from django.urls import path
from .views import *

urlpatterns = [
    # ... your other URL patterns
    path('', generate_pdfs, name='generate_pdfs'),
    path('update_tenants/', update_tenants, name='update_tenants'),
    path('update/<str:tenant_name>/', update_tenants, name='update_tenant'),
    path('update_success/', update_success, name='update_success'),
    path('add/', add_tenant, name='add_tenant'),
    path('<str:tenant_name>/delete/', delete_tenant, name='delete_tenant'),
    path('contracts/all-contracts/', all_contracts, name='all_contracts'),
    path('contracts/update/<str:tenant_name>/', all_contracts, name='update_contract'),
    path('contracts/add/', add_contract, name='add_contract'),
    path('contracts/<str:tenant_name>/delete/', delete_contract, name='delete_contract'),
    path('contracts/update_success/', contracts_update_success, name='contracts_update_success'),
    path('contracts/reminder/', reminder, name='reminder'),
]