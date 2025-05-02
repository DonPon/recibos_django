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
from dotenv import load_dotenv
from num2words import num2words
from django.views import View

from .models import Tenant, Contract
from .forms import LoginForm, MonthForm, TenantForm, LocalComercialForm, DepartamentoForm, ReciboOnDemandForm
from .src.src_email import send_email
from .src.src_pdf_utils import create_recibo_pdf, send_emails_recibos, create_contract_pdf, send_emails_contracts, send_emails_recibos_on_demand
from .src.src_dates import parse_date_string, flag_one_month_to_date
from django.views.generic.base import ContextMixin

load_dotenv()

dias = 40

class EnvContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ENV'] = os.getenv('ENV')
        return context


class LoginPageView(EnvContextMixin, FormView):
    template_name = 'authentication/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('generate_pdfs')

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
        )
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, 'Contraseña incorrecta.')
            return self.form_invalid(form)


class GeneratePDFsView(LoginRequiredMixin, EnvContextMixin, FormView):
    template_name = 'recibos/generate_pdfs.html'
    form_class = MonthForm
    success_url = reverse_lazy('pdf_generated')

    def form_valid(self, form):
        month = form.cleaned_data['month']
        current_year = datetime.datetime.now().year
        tenants = Tenant.objects.all()
        files = []

        for tenant in tenants:
            day = tenant.dia
            price = tenant.precio
            price_letters = num2words(price.split('.')[0].replace(',', ''), lang='es')
            servicios = tenant.servicios
            local = tenant.local
            subject = f"CDMX, a {day} de {month.lower()}\nde {current_year}"
            text = f"Recibí de parte del SR. {(tenant.name).upper()}, la cantidad de ${price} ({price_letters.upper()} PESOS 00/100 M.N.), " \
                   f"por concepto de {servicios.lower()} del local {local}, del inmueble ubicado en Calle Noche de Paz # 14 Colonia Granjas Navidad, " \
                   f"Delegación Cuajimalpa, C.P. 05219, correspondiente al mes de {month.upper()} de {current_year}."

            file_path = create_recibo_pdf(subject, text, month, tenant.name)
            files.append(file_path)

        time.sleep(1)
        send_emails_recibos(files, month)
        return super().form_valid(form)

class PdfGeneratedView(LoginRequiredMixin, EnvContextMixin, TemplateView):
    template_name = 'recibos/pdf_generated.html'

# ------ Send every month and send invoice

class AutomaticGeneratePDFsViewEveryMonth(EnvContextMixin, View):

    def get(self, request, *args, **kwargs):
        today = datetime.datetime.now()

        # Only execute if is day of the month
        if today.day != 1:
            return JsonResponse({"message": "No es el primer día del mes. No se generarán PDFs."}, status=200)

        month_dict = {
            1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril', 5: 'mayo', 6: 'junio',
            7: 'julio', 8: 'agosto', 9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'
        }
        month = month_dict[datetime.datetime.now().month]
        current_year = datetime.datetime.now().year
        tenants = Tenant.objects.all()
        files = []

        for tenant in tenants:
            day = tenant.dia
            price = tenant.precio
            price_letters = num2words(price.split('.')[0].replace(',', ''), lang='es')
            servicios = tenant.servicios
            local = tenant.local
            subject = f"CDMX, a {day} de {month.lower()}\nde {current_year}"
            text = f"Recibí de parte del SR. {(tenant.name).upper()}, la cantidad de ${price} ({price_letters.upper()} PESOS 00/100 M.N.), " \
                   f"por concepto de {servicios.lower()} del local {local}, del inmueble ubicado en Calle Noche de Paz # 14 Colonia Granjas Navidad, " \
                   f"Delegación Cuajimalpa, C.P. 05219, correspondiente al mes de {month.upper()} de {current_year}."

            file_path = create_recibo_pdf(subject, text, month, tenant.name)
            files.append(file_path)

        time.sleep(1)
        send_emails_recibos(files, month)
        return JsonResponse({"message": "PDFs generados y correos enviados correctamente."}, status=200)

# -------------------------------------TENANTS-------------------------------------------------------------------
class TenantListView(LoginRequiredMixin, EnvContextMixin, ListView):
    model = Tenant
    template_name = 'recibos/update_tenants.html'
    context_object_name = 'tenants'

class UpdateTenantView(LoginRequiredMixin, EnvContextMixin, UpdateView):
    model = Tenant
    form_class = TenantForm
    template_name = 'recibos/update_tenant.html'
    success_url = reverse_lazy('update_success')
    context_object_name = 'editing_tenant'
    slug_field = 'name'  # Tell Django to use 'name' field for lookup
    slug_url_kwarg = 'tenant_name'  # Match 'tenant_name' in the URL to 'name'

    def form_valid(self, form):
        tenant = form.save(commit=False)
        tenant.precio = "{:,.2f}".format(float(tenant.precio.replace(',', '')))
        tenant.servicios = tenant.servicios.lower()
        tenant.save()
        return super().form_valid(form)

class UpdateSuccessView(LoginRequiredMixin, EnvContextMixin, TemplateView):
    template_name = 'recibos/update_success.html'

class AddTenantView(LoginRequiredMixin, EnvContextMixin, CreateView):
    model = Tenant
    form_class = TenantForm
    template_name = 'recibos/add_tenant.html'
    success_url = reverse_lazy('update_tenants')

    def form_valid(self, form):
        tenant = form.save(commit=False)
        tenant.name = tenant.name.upper()
        tenant.servicios = tenant.servicios.lower()
        tenant.precio = "{:,.2f}".format(float(tenant.precio.replace(',', '')))
        tenant.save()
        return super().form_valid(form)

class DeleteTenantView(LoginRequiredMixin, EnvContextMixin, DeleteView):
    model = Tenant
    template_name = 'recibos/delete_tenant.html'
    success_url = reverse_lazy('generate_pdfs')
    slug_field = 'name'  # Specify the model field to use for lookup
    slug_url_kwarg = 'tenant_name'  # Match this to the URL parameter
    context_object_name = 'tenant'

# ----------------------------------------CONTRACTS--------------------------------------------------------------
class ContractListView(LoginRequiredMixin, EnvContextMixin, ListView):
    model = Contract
    template_name = 'contratos/all_contracts.html'
    context_object_name = 'contracts'

    def get(self, request, *args, **kwargs):
        if 'download_contract' in request.GET:
            tenant_name = request.GET.get('tenant_name')
            contract = get_object_or_404(Contract, nombre_arrendatario=tenant_name)
            # logic to generate and return the PDF file
            create_contract_pdf(item_dict=contract)
            return
        return super().get(request, *args, **kwargs)

class UpdateContractView(LoginRequiredMixin, EnvContextMixin, UpdateView):
    model = Contract
    form_class = LocalComercialForm
    template_name = 'contratos/update_contract.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('contracts_update_success')

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

class AddContractView(LoginRequiredMixin, EnvContextMixin, CreateView):
    model = Contract
    #form_class = ContractForm
    template_name = 'contratos/add_contract.html'
    success_url = reverse_lazy('all_contracts')

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

class DeleteContractView(LoginRequiredMixin, EnvContextMixin, DeleteView):
    model = Contract
    template_name = 'contratos/delete_contract.html'
    success_url = reverse_lazy('generate_pdfs')
    pk_url_kwarg = 'id'


class CreateContractPDFView(LoginRequiredMixin, EnvContextMixin, TemplateView):
    template_name = 'contratos/pdf_generated.html'

    def get(self, request, *args, **kwargs):
        contract_id = kwargs.get('contract_id')
        contract = Contract.objects.filter(id=contract_id).values().first()
        contract_file_path = create_contract_pdf(item_dict=contract)
        send_emails_contracts(contract_file_path, contract['nombre_arrendatario'])

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contract_id'] = kwargs.get('contract_id')
        return context


class ReminderView(EnvContextMixin, TemplateView):

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
                send_email("Próximo Vencimiento de Contrato", body)

                expiring_contracts.append({
                    'nombre_arrendatario': contract.nombre_arrendatario,
                    'fecha_vencimiento_contrato': contract.fecha_vencimiento_contrato,
                    'local': contract.local,
                    'renta': contract.renta,
                })
        return JsonResponse({'expiring_contracts': expiring_contracts}, status=200)

# ----------------------------------- RECIBO ON DEMAND (1 SOLA VEZ) ---------------------------------------------

class GenerateReciboUnaSolaVezOnDemandView(LoginRequiredMixin, EnvContextMixin, FormView):
    template_name = 'recibos/generate_recibo_una_sola_vez.html'
    form_class = ReciboOnDemandForm
    success_url = reverse_lazy('pdf_generated')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        data = form.cleaned_data
        current_year = datetime.datetime.now().year
        day = datetime.datetime.now().day
        meses = [
            "ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
            "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"
        ]
        month = meses[(datetime.datetime.now().month) - 1]
        tenant_name = data['name']
        precio = "{:,.2f}".format(float(data['precio'].replace(',', '')))
        price_letters = num2words(precio.split('.')[0].replace(',', ''), lang='es')
        concepto = data['tipo_recibo'].replace('_', ' ')
        local = data['local']
        subject = f"CDMX, a {day} de {month.lower()}\nde {current_year}"
        titulo = data['titulo']
        propiedad = data['propiedad']
        property_type = 'local' if propiedad == 'Noche de Paz #14, Colonia Granjas Navidad, Delegación Cuajimalpa, C.P. 05219' else 'departamento'
        text = f"Recibí de parte {'del SR.' if titulo == 'SR.' else 'de la SRA.'} {(tenant_name).upper()}, la cantidad de ${precio} ({price_letters.upper()} PESOS 00/100 M.N.), " \
               f"por concepto de {concepto.upper()} del {property_type} {local}, del inmueble ubicado en calle {propiedad}."

        file_path = create_recibo_pdf(subject, text, month, tenant_name)
        time.sleep(1)
        send_emails_recibos_on_demand([file_path], concepto, tenant_name)
        return super().form_valid(form)

