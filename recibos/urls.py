from django.urls import path
from .views import (
    LoginPageView, GeneratePDFsView, TenantListView, UpdateTenantView,
    AddTenantView, DeleteTenantView, ContractListView, UpdateContractView,
    AddContractView, DeleteContractView, ReminderView, UpdateSuccessView,
    PdfGeneratedView, CreateContractPDFView, AutomaticGeneratePDFsViewEveryMonth
)

urlpatterns = [
    path('', GeneratePDFsView.as_view(), name='generate_pdfs'),
    path('pdf_generated/', PdfGeneratedView.as_view(), name='pdf_generated'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('update_tenants/', TenantListView.as_view(), name='update_tenants'),
    path('update/<str:tenant_name>/', UpdateTenantView.as_view(), name='update_tenant'),
    path('update_success/', UpdateSuccessView.as_view(), name='update_success'),
    path('add/', AddTenantView.as_view(), name='add_tenant'),
    path('<str:tenant_name>/delete/', DeleteTenantView.as_view(), name='delete_tenant'),
    path('contracts/all-contracts/', ContractListView.as_view(), name='all_contracts'),
    path('contracts/update/<uuid:id>/', UpdateContractView.as_view(), name='update_contract'),
    path('contracts/add/', AddContractView.as_view(), name='add_contract'),
    path('contracts/<uuid:id>/delete/', DeleteContractView.as_view(), name='delete_contract'),
    path('contracts/reminder/', ReminderView.as_view(), name='reminder'),
    path('create_contract_pdf/<uuid:contract_id>/', CreateContractPDFView.as_view(), name='create_contract_pdf'),
    path('automatic-invoice-check/', AutomaticGeneratePDFsViewEveryMonth.as_view(), name='automatic-invoice-check'),
]