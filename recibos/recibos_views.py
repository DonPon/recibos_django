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

from recibos.recibos_models import Tenant
from recibos.recibos_forms import LoginForm, MonthForm, TenantForm
from src.src_email import send_email
from src.src_pdf_utils import create_recibo_pdf, send_emails_recibos
from src.src_dates import parse_date_string, flag_one_month_to_date

from recibos_django.mixins import EnvContextMixin, to_email, dias



class LoginPageView(EnvContextMixin, FormView):
    template_name = 'authentication/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('recibos:generate_pdfs')

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
    success_url = reverse_lazy('recibos:pdf_generated')

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
        send_emails_recibos(files=files, month=month, to_email=self.request.user.email)
        return super().form_valid(form)

class PdfGeneratedView(LoginRequiredMixin, EnvContextMixin, TemplateView):
    template_name = 'recibos/pdf_generated.html'

# ------ Send every month and send invoice

class Recibos_AutomaticGeneratePDFsViewEveryMonth(EnvContextMixin, View):

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
        send_emails_recibos(files=files, month=month, to_email=to_email)
        return JsonResponse({"message": "PDFs generados y correos enviados correctamente."}, status=200)

# -------------------------------------TENANTS-------------------------------------------------------------------
class Recibos_TenantListView(LoginRequiredMixin, EnvContextMixin, ListView):
    model = Tenant
    template_name = 'recibos/update_tenants.html'
    context_object_name = 'tenants'

class Recibos_UpdateTenantView(LoginRequiredMixin, EnvContextMixin, UpdateView):
    model = Tenant
    form_class = TenantForm
    template_name = 'recibos/update_tenant.html'
    success_url = reverse_lazy('recibos:update_success')
    context_object_name = 'editing_tenant'
    slug_field = 'name'  # Tell Django to use 'name' field for lookup
    slug_url_kwarg = 'tenant_name'  # Match 'tenant_name' in the URL to 'name'

    def form_valid(self, form):
        tenant = form.save(commit=False)
        tenant.precio = "{:,.2f}".format(float(tenant.precio.replace(',', '')))
        tenant.servicios = tenant.servicios.lower()
        tenant.save()
        return super().form_valid(form)

class Recibos_UpdateSuccessView(LoginRequiredMixin, EnvContextMixin, TemplateView):
    template_name = 'recibos/update_success.html'

class Recibos_AddTenantView(LoginRequiredMixin, EnvContextMixin, CreateView):
    model = Tenant
    form_class = TenantForm
    template_name = 'recibos/add_tenant.html'
    success_url = reverse_lazy('recibos:update_tenants')

    def form_valid(self, form):
        tenant = form.save(commit=False)
        tenant.name = tenant.name.upper()
        tenant.servicios = tenant.servicios.lower()
        tenant.precio = "{:,.2f}".format(float(tenant.precio.replace(',', '')))
        tenant.save()
        return super().form_valid(form)

class Recibos_DeleteTenantView(LoginRequiredMixin, EnvContextMixin, DeleteView):
    model = Tenant
    template_name = 'recibos/delete_tenant.html'
    success_url = reverse_lazy('recibos:generate_pdfs')
    slug_field = 'name'  # Specify the model field to use for lookup
    slug_url_kwarg = 'tenant_name'  # Match this to the URL parameter
    context_object_name = 'tenant'



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
