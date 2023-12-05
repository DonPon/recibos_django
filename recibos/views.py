from django.shortcuts import render, redirect
from .models import Tenant
from .forms import *
import datetime
from .src.src_pdf_utils import create_pdf


def generate_pdfs(request):
    if request.method == 'POST':
        form = MonthForm(request.POST)
        if form.is_valid():
            month = form.cleaned_data['month']
            current_year = datetime.datetime.now().year

            tenants = Tenant.objects.all()

            for tenant in tenants:
                day = tenant.dia
                price = tenant.precio
                price_letters = tenant.precio_en_letra
                servicios = tenant.servicios
                local = tenant.local

                subject = f"CDMX, a {day} de {month}\nde {current_year}"
                text = f"Recibí de parte del SR. {tenant.name}, la cantidad de ${price} ({price_letters.upper()} PESOS 00/100 M.N.), " \
                    f"por concepto de {servicios} del local {local}, del inmueble ubicado en Calle Noche de Paz # 14 Colonia Granjas Navidad, " \
                    f"Delegación Cuajimalpa, C.P. 05219, correspondiente al mes de {month.upper()} de {current_year}."

                # Create and save the PDF (replace with your PDF creation logic)
                create_pdf(subject, text, month, tenant.name)

            return render(request, 'recibos/pdf_generated.html', {'month': month})

    else:
        form = MonthForm()

    return render(request, 'recibos/generate_pdfs.html', {'form': form})


def update_tenants(request, tenant_name=None):
    tenants = Tenant.objects.all()

    if tenant_name:
        # Get the tenant instance
        tenant = Tenant.objects.get(name=tenant_name)

        if request.method == 'POST':
            form = TenantForm(request.POST, instance=tenant)
            if form.is_valid():
                # Save the changes
                form.save()
                return redirect('update_success')  # Redirect to a success page
        else:
            form = TenantForm(instance=tenant)

        return render(request, 'recibos/update_tenant.html', {'form': form, 'editing_tenant': tenant})
    else:
        # Display the list of tenants
        return render(request, 'recibos/update_tenants.html', {'tenants': tenants})



def update_success(request):
    return render(request, 'recibos/update_success.html')

