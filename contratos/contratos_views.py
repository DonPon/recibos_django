# contratos/views.py
from django.shortcuts import render
import os
import time
import datetime
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseServerError, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from num2words import num2words
from django.views import View

from contratos.contratos_models import Contract
from contratos.contratos_forms import LocalComercialForm, DepartamentoForm
from src.src_email import send_email
from src.src_pdf_utils import create_contract_pdf, send_emails_contracts
from src.src_dates import parse_date_string, flag_one_month_to_date

from recibos_django.mixins import EnvContextMixin, to_email, dias

# ----------------------------------------CONTRACTS--------------------------------------------------------------
class Contratos_ContractListView(LoginRequiredMixin, EnvContextMixin, ListView):
    model = Contract
    template_name = 'contratos/all_contracts.html'
    context_object_name = 'contracts'

    def get(self, request, *args, **kwargs):
        if 'download_contract' in request.GET:
            tenant_name = request.GET.get('contratos:tenant_name')
            contract = get_object_or_404(Contract, nombre_arrendatario=tenant_name)
            # logic to generate and return the PDF file
            create_contract_pdf(item_dict=contract)
            return
        return super().get(request, *args, **kwargs)

class Contratos_UpdateContractView(LoginRequiredMixin, EnvContextMixin, UpdateView):
    model = Contract
    form_class = LocalComercialForm
    template_name = 'contratos/update_contract.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('contratos:contracts_update_success')

    def get_form_class(self):
        contract_type = self.request.GET.get('contract_type') or self.request.POST.get('contract_type')
        if contract_type == 'local_comercial':
            return LocalComercialForm
        elif contract_type == 'departamento':
            return DepartamentoForm
        return LocalComercialForm  # Default form if type is not specified

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contract_type'] = self.request.GET.get('contract_type') or self.request.POST.get('contract_type')
        return context

    def form_valid(self, form):
        contract = form.save(commit=False)
        contract.nombre_arrendatario = contract.nombre_arrendatario.upper()
        contract.nombre_arrendatario = contract.nombre_arrendatario.upper()
        contract.ine_arrendatario = contract.ine_arrendatario.upper()
        contract.curp_arrendatario = contract.curp_arrendatario.upper()
        contract.celular_arrendatario = contract.celular_arrendatario
        contract.fecha_inicio_contrato = contract.fecha_inicio_contrato
        contract.fecha_vencimiento_contrato = contract.fecha_vencimiento_contrato
        contract.renta = "{:,.2f}".format(float(contract.renta.replace(',', '')))
        contract.iva = "{:,.2f}".format(float(contract.iva.replace(',', '')))
        contract.total = "{:,.2f}".format(float(contract.total.replace(',', '')))
        contract.deposito = "{:,.2f}".format(float(contract.deposito.replace(',', '')))
        contract.mantenimiento = "{:,.2f}".format(float(contract.mantenimiento.replace(',', '')))
        contract.dia_de_pago = contract.dia_de_pago
        contract.save()
        return super().form_valid(form)

class Contratos_AddContractView(LoginRequiredMixin, EnvContextMixin, CreateView):
    model = Contract
    #form_class = ContractForm
    template_name = 'contratos/add_contract.html'
    success_url = reverse_lazy('contratos:all_contracts')

    def get_form_class(self):
        contract_type = self.request.GET.get('contract_type') or self.request.POST.get('contract_type')
        self.contract_type = contract_type
        if contract_type == 'local_comercial':
            return LocalComercialForm
        elif contract_type == 'departamento':
            return DepartamentoForm
        return LocalComercialForm
        


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contract_type'] = self.request.GET.get('contract_type') or self.request.POST.get('contract_type')
        return context

    def form_valid(self, form):
        contract = form.save(commit=False)
        contract.contract_type = self.request.GET.get('contract_type') or self.request.POST.get('contract_type')
        contract.nombre_arrendatario = contract.nombre_arrendatario.upper()
        contract.ine_arrendatario = contract.identificacion_arrendatario.upper()
        contract.curp_arrendatario = contract.curp_arrendatario.upper()
        contract.celular_arrendatario = contract.celular_arrendatario
        contract.fecha_inicio_contrato = contract.fecha_inicio_contrato
        contract.fecha_vencimiento_contrato = contract.fecha_vencimiento_contrato
        contract.renta = "{:,.2f}".format(float(contract.renta.replace(',', '')))
        contract.iva = "{:,.2f}".format(float(contract.iva.replace(',', '')))
        contract.total = "{:,.2f}".format(float(contract.total.replace(',', '')))
        contract.deposito = "{:,.2f}".format(float(contract.deposito.replace(',', '')))
        contract.mantenimiento = "{:,.2f}".format(float(contract.mantenimiento.replace(',', '')))
        contract.dia_de_pago = contract.dia_de_pago
        contract.save()
        print(contract.__dict__)
        contract_file_path = create_contract_pdf(item_dict=contract.__dict__)
        send_emails_contracts(contract_file_path, contract.__dict__['nombre_arrendatario'])
        return super().form_valid(form)

class Contratos_DeleteContractView(LoginRequiredMixin, EnvContextMixin, DeleteView):
    model = Contract
    template_name = 'contratos/delete_contract.html'
    success_url = reverse_lazy('recibos:generate_pdfs')
    pk_url_kwarg = 'id'

class Contratos_CreateContractPDFView(LoginRequiredMixin, EnvContextMixin, TemplateView):
    template_name = 'contratos/pdf_generated.html'

    def get(self, request, *args, **kwargs):
        contract_id = kwargs.get('contract_id')
        contract = Contract.objects.filter(id=contract_id).values().first()
        contract_file_path = create_contract_pdf(item_dict=contract)
        send_emails_contracts(file_path=contract_file_path, identifier=contract['nombre_arrendatario'], to_email=self.request.user.email)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contract_id'] = kwargs.get('contract_id')
        return context

class Contratos_ReminderView(EnvContextMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        expiring_contracts = []
        contracts = Contract.objects.all()

        for contract in contracts:
            vencimiento = parse_date_string(contract.fecha_vencimiento_contrato)
            if flag_one_month_to_date(vencimiento, dias):
                body = f"Hola,\n\nEl siguiente contrato está próximo a vencer en {dias} días:\n\n" \
                       f"Arrendatario: {contract.nombre_arrendatario}\n" \
                       f"Vencimiento: {contract.fecha_vencimiento_contrato}\n" \
                       f"Local: {contract.local}\n" \
                       f"Monto renta: ${contract.renta} MXN\n\n" \
                       f"Ver contrato aquí: https://recibos-django.onrender.com/contracts/all-contracts/"
                send_email(subject="Próximo Vencimiento de Contrato", body=body, to_email=to_email)

                expiring_contracts.append({
                    'nombre_arrendatario': contract.nombre_arrendatario,
                    'fecha_vencimiento_contrato': contract.fecha_vencimiento_contrato,
                    'local': contract.local,
                    'renta': contract.renta,
                })
        return JsonResponse({'expiring_contracts': expiring_contracts}, status=200)