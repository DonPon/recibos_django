# admin.py
from django.contrib import admin
from .models import Tenant, Contract

admin.site.register(Tenant)
admin.site.register(Contract)
