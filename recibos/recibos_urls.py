from django.urls import path
from recibos.recibos_views import (
    LoginPageView, GeneratePDFsView, Recibos_TenantListView, Recibos_UpdateTenantView,
    Recibos_AddTenantView, Recibos_DeleteTenantView, PdfGeneratedView, Recibos_UpdateSuccessView, Recibos_AutomaticGeneratePDFsViewEveryMonth)

app_name = 'recibos'

urlpatterns = [
    path('', GeneratePDFsView.as_view(), name='generate_pdfs'),
    path('pdf_generated/', PdfGeneratedView.as_view(), name='pdf_generated'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('update_tenants/', Recibos_TenantListView.as_view(), name='update_tenants'),
    path('update/<str:tenant_name>/', Recibos_UpdateTenantView.as_view(), name='update_tenant'),
    path('update_success/', Recibos_UpdateSuccessView.as_view(), name='update_success'),
    path('add/', Recibos_AddTenantView.as_view(), name='add_tenant'),
    path('<str:tenant_name>/delete/', Recibos_DeleteTenantView.as_view(), name='delete_tenant'),
    path('automatic-invoice-check/', Recibos_AutomaticGeneratePDFsViewEveryMonth.as_view(), name='automatic-invoice-check'),
]
