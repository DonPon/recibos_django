
from django.urls import path
from .views import *

urlpatterns = [
    # ... your other URL patterns
    path('', generate_pdfs, name='generate_pdfs'),
    path('update_tenants/', update_tenants, name='update_tenants'),
    path('update_tenants/<str:tenant_name>/', update_tenants, name='update_tenant'),
    path('update_success/', update_success, name='update_success'),
]