# on_demand/views.py
import time
import datetime
import logging

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from num2words import num2words
from django.views.generic.edit import FormView

from on_demand.on_demand_forms import ConvenioTerminacionEntregaForm, ReciboOnDemandForm
from src.src_pdf_utils import create_recibo_pdf, create_terminacion_entrega_pdf, send_emails_recibos_on_demand
from src.src_dates import parse_date_string

from recibos_django.mixins import EnvContextMixin, to_email, dias

# get a logger; using the 'recibos' name will write to the same handlers
logger = logging.getLogger('recibos')



# ----------------------------------- RECIBO ON DEMAND (1 SOLA VEZ) ---------------------------------------------

class OnDemand_GenerateReciboView(LoginRequiredMixin, EnvContextMixin, FormView):
    template_name = 'terminacion_entrega/generate_recibo_una_sola_vez.html'
    form_class = ReciboOnDemandForm
    success_url = reverse_lazy('recibos:pdf_generated')

    def post(self, request, *args, **kwargs):
        logger.debug("OnDemand_GenerateReciboView.post called for user %s", request.user)
        form = self.get_form()
        if form.is_valid():
            logger.debug("Recibo form valid: %r", form.cleaned_data)
            return self.form_valid(form)
        else:
            logger.warning("Recibo form invalid: %s", form.errors)
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

        logger.info("generating recibo PDF for %s (%s)", tenant_name, concepto)
        file_path = create_recibo_pdf(subject, text, month, tenant_name)
        logger.debug("PDF created at %s", file_path)
        time.sleep(1)
        logger.info("sending email to %s", self.request.user.email)
        send_emails_recibos_on_demand(files=[file_path], concepto=concepto, name=tenant_name, to_email=self.request.user.email)
        logger.debug("email send call completed")
        return super().form_valid(form)

# ------------------------CONVENIO DE TERMINACIÓN Y ENTREGA (1 SOLA VEZ) -----------------------------------------

class OnDemand_GenerateConvenioTerminacionEntregaView(LoginRequiredMixin, EnvContextMixin, FormView): 
    template_name = 'terminacion_entrega/generate_terminacion_entrega_una_sola_vez.html'
    form_class = ConvenioTerminacionEntregaForm
    success_url = reverse_lazy('recibos:pdf_generated')

    def post(self, request, *args, **kwargs):
        logger.debug("OnDemand_GenerateConvenioTerminacionEntregaView.post called for user %s", request.user)
        form = self.get_form()
        if form.is_valid():
            logger.debug("Convenio form valid: %r", form.cleaned_data)
            return self.form_valid(form)
        else:
            logger.warning("Convenio form invalid: %s", form.errors)
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
        titulo = data['titulo'].replace('.', '')
        tenant_name = data['name']
        local = data['local']
        subject = f"CIUDAD DE MÉXICO, A {day} DE {month.upper()} DE {current_year}\n"
        fecha_hoy = f"{day} DE {month} DE {current_year}"
        comienzo_contrato = data['comienzo_contrato']
        terminacion_contrato = data['terminacion_contrato']
        duracion_contrato = datetime.datetime.strptime(terminacion_contrato, '%d/%m/%Y').year - datetime.datetime.strptime(comienzo_contrato, '%d/%m/%Y').year

        propiedad = data['propiedad']
        property_type = 'local' if propiedad == 'Noche de Paz #14, Colonia Granjas Navidad, Delegación Cuajimalpa, C.P. 05219' else 'departamento'
        
        item_dict = {
            'titulo_arrendatario': titulo,
            'subject': subject,
            'nombre_arrendatario': (tenant_name).upper(),
            'local': local,
            'propiedad': propiedad,
            'property_type': property_type,
            'fecha_hoy': fecha_hoy,
            'duracion_contrato': f'{duracion_contrato} AÑO(S)',
            'comienzo_contrato': comienzo_contrato,
            'terminacion_contrato': terminacion_contrato,
        }

        logger.info("creating convenio PDF for %s", tenant_name)
        file_path = create_terminacion_entrega_pdf(item_dict)
        logger.debug("convenio PDF generated: %s", file_path)
        time.sleep(1)
        logger.info("sending convenio email to %s", self.request.user.email)
        send_emails_recibos_on_demand(files=[file_path], concepto='Convenio_Terminacion_Entrega', name=tenant_name, to_email=self.request.user.email)
        logger.debug("convenio email send call completed")
        return super().form_valid(form)
