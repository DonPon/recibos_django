import os
import time
import logging
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

# Configure logger
logger = logging.getLogger('recibos')



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
            logger.info(f"✓ User '{user.username}' logged in successfully")
            login(self.request, user)
            return super().form_valid(form)
        else:
            logger.warning(f"✗ Failed login attempt for username: {form.cleaned_data['username']}")
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

        logger.info(f"=== GeneratePDFsView.form_valid() START ===")
        logger.info(f"Month: {month}, Year: {current_year}")
        logger.info(f"Total tenants found: {tenants.count()}")

        for tenant in tenants:
            logger.debug(f"Processing tenant: {tenant.name} (Local: {tenant.local})")
            day = tenant.dia
            price = tenant.precio
            price_letters = num2words(price.split('.')[0].replace(',', ''), lang='es')
            servicios = tenant.servicios
            local = tenant.local
            subject = f"CDMX, a {day} de {month.lower()}\nde {current_year}"
            text = f"Recibí de parte del SR. {(tenant.name).upper()}, la cantidad de ${price} ({price_letters.upper()} PESOS 00/100 M.N.), " \
                   f"por concepto de {servicios.lower()} del local {local}, del inmueble ubicado en Calle Noche de Paz # 14 Colonia Granjas Navidad, " \
                   f"Delegación Cuajimalpa, C.P. 05219, correspondiente al mes de {month.upper()} de {current_year}."

            try:
                file_path = create_recibo_pdf(subject, text, month, tenant.name)
                logger.info(f"✓ PDF created successfully for {tenant.name}")
                logger.info(f"  - File path: {file_path}")
                logger.info(f"  - File name: {os.path.basename(file_path)}")
                logger.debug(f"  - Full path: {os.path.abspath(file_path)}")
                logger.debug(f"  - File exists: {os.path.exists(file_path)}")
                logger.debug(f"  - File size: {os.path.getsize(file_path)} bytes")
                files.append(file_path)
            except Exception as e:
                logger.error(f"✗ Failed to create PDF for {tenant.name}: {str(e)}", exc_info=True)
                continue

        logger.info(f"Total PDF files created: {len(files)}")

        time.sleep(1)
        
        recipient_email = self.request.user.email
        sender_email = os.getenv('FROM_EMAIL')
        logger.info(f"Email configuration:")
        logger.info(f"  - Sender: {sender_email}")
        logger.info(f"  - Recipient: {recipient_email}")
        logger.info(f"  - Files to send: {len(files)}")
        
        try:
            logger.debug(f"Attempting to send emails with {len(files)} PDF attachments...")
            send_emails_recibos(files=files, month=month, to_email=recipient_email)
            logger.info(f"✓ Emails sent successfully to {recipient_email}")
            logger.info(f"=== GeneratePDFsView.form_valid() END (SUCCESS) ===")
        except Exception as e:
            logger.error(f"✗ Failed to send emails: {str(e)}", exc_info=True)
            logger.info(f"=== GeneratePDFsView.form_valid() END (FAILED) ===")
            
        return super().form_valid(form)

class PdfGeneratedView(LoginRequiredMixin, EnvContextMixin, TemplateView):
    template_name = 'recibos/pdf_generated.html'

# ------ Send every month and send invoice

class Recibos_AutomaticGeneratePDFsViewEveryMonth(EnvContextMixin, View):

    def get(self, request, *args, **kwargs):
        today = datetime.datetime.now()
        logger.info(f"=== Recibos_AutomaticGeneratePDFsViewEveryMonth.get() START ===")
        logger.info(f"Current date: {today.strftime('%Y-%m-%d %H:%M:%S')}, Day of month: {today.day}")

        # Only execute if is day of the month
        if today.day != 1:
            logger.info(f"✗ Skipped - Not the 1st day of month (Current day: {today.day})")
            logger.info(f"=== Recibos_AutomaticGeneratePDFsViewEveryMonth.get() END (SKIPPED) ===")
            return JsonResponse({"message": "No es el primer día del mes. No se generarán PDFs."}, status=200)

        month_dict = {
            1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril', 5: 'mayo', 6: 'junio',
            7: 'julio', 8: 'agosto', 9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'
        }
        month = month_dict[datetime.datetime.now().month]
        current_year = datetime.datetime.now().year
        tenants = Tenant.objects.all()
        files = []

        logger.info(f"✓ Scheduled task triggered on 1st day of month")
        logger.info(f"Month: {month}, Year: {current_year}")
        logger.info(f"Total tenants found: {tenants.count()}")

        for tenant in tenants:
            logger.debug(f"Processing tenant: {tenant.name} (Local: {tenant.local})")
            day = tenant.dia
            price = tenant.precio
            price_letters = num2words(price.split('.')[0].replace(',', ''), lang='es')
            servicios = tenant.servicios
            local = tenant.local
            subject = f"CDMX, a {day} de {month.lower()}\nde {current_year}"
            text = f"Recibí de parte del SR. {(tenant.name).upper()}, la cantidad de ${price} ({price_letters.upper()} PESOS 00/100 M.N.), " \
                   f"por concepto de {servicios.lower()} del local {local}, del inmueble ubicado en Calle Noche de Paz # 14 Colonia Granjas Navidad, " \
                   f"Delegación Cuajimalpa, C.P. 05219, correspondiente al mes de {month.upper()} de {current_year}."

            try:
                file_path = create_recibo_pdf(subject, text, month, tenant.name)
                logger.info(f"✓ PDF created successfully for {tenant.name}")
                logger.info(f"  - File path: {file_path}")
                logger.info(f"  - File size: {os.path.getsize(file_path)} bytes")
                files.append(file_path)
            except Exception as e:
                logger.error(f"✗ Failed to create PDF for {tenant.name}: {str(e)}", exc_info=True)
                continue

        logger.info(f"Total PDF files created: {len(files)}")

        time.sleep(1)
        
        logger.info(f"Email configuration:")
        logger.info(f"  - Recipient: {to_email}")
        logger.info(f"  - Files to send: {len(files)}")
        
        try:
            logger.debug(f"Attempting to send emails with {len(files)} PDF attachments...")
            send_emails_recibos(files=files, month=month, to_email=to_email)
            logger.info(f"✓ Emails sent successfully to {to_email}")
            logger.info(f"=== Recibos_AutomaticGeneratePDFsViewEveryMonth.get() END (SUCCESS) ===")
            return JsonResponse({"message": "PDFs generados y correos enviados correctamente."}, status=200)
        except Exception as e:
            logger.error(f"✗ Failed to send emails: {str(e)}", exc_info=True)
            logger.info(f"=== Recibos_AutomaticGeneratePDFsViewEveryMonth.get() END (FAILED) ===")
            return JsonResponse({"message": f"Error al enviar correos: {str(e)}"}, status=500)

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
        original_name = tenant.name
        tenant.precio = "{:,.2f}".format(float(tenant.precio.replace(',', '')))
        tenant.servicios = tenant.servicios.lower()
        tenant.save()
        logger.info(f"✓ Tenant updated successfully: {original_name}")
        logger.debug(f"  - Price: {tenant.precio}, Services: {tenant.servicios}")
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
        logger.info(f"✓ New tenant created successfully: {tenant.name}")
        logger.debug(f"  - Local: {tenant.local}, Price: {tenant.precio}, Services: {tenant.servicios}")
        return super().form_valid(form)

class Recibos_DeleteTenantView(LoginRequiredMixin, EnvContextMixin, DeleteView):
    model = Tenant
    template_name = 'recibos/delete_tenant.html'
    success_url = reverse_lazy('recibos:update_tenants')
    slug_field = 'name'
    slug_url_kwarg = 'tenant_name'
    context_object_name = 'tenant'

    def get_template_names(self):
        if self.request.headers.get('HX-Request'):
            return ['recibos/partials/delete_tenant_modal.html']
        return [self.template_name]

