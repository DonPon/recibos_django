import time

from django.shortcuts import render, redirect, get_object_or_404
from .models import Tenant, Contract
from .forms import *
import datetime
from .src.src_pdf_utils import *


def generate_pdfs(request):
    if request.method == 'POST':
        form = MonthForm(request.POST)
        if form.is_valid():
            month = form.cleaned_data['month']
            current_year = datetime.datetime.now().year

            tenants = Tenant.objects.all()
            files = []
            for tenant in tenants:
                day = tenant.dia
                price = tenant.precio
                price_letters = tenant.precio_en_letra
                servicios = tenant.servicios
                local = tenant.local

                subject = f"CDMX, a {day} de {month.lower()}\nde {current_year}"
                text = f"Recibí de parte del SR. {(tenant.name).upper()}, la cantidad de ${price} ({price_letters.upper()} PESOS 00/100 M.N.), " \
                    f"por concepto de {servicios.lower()} del local {local}, del inmueble ubicado en Calle Noche de Paz # 14 Colonia Granjas Navidad, " \
                    f"Delegación Cuajimalpa, C.P. 05219, correspondiente al mes de {month.upper()} de {current_year}."

                # Create and save the PDF (replace with your PDF creation logic)
                #create_pdf(subject, text, month, tenant.name)
                #file_path = create_pdf_reportlab(subject, text, month, tenant.name)
                file_path =  create_pdf_email(subject, text, month, tenant.name)
                files.append(file_path)

            time.sleep(1)
            send_emails(files, month)


                #response = create_pdf_download(request, subject, text, month, tenant.name)

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


                if not ',' in tenant.precio:
                    tenant.precio = "{:,.2f}".format(float(tenant.precio))

                elif ',' in tenant.precio:
                    precio_temp = tenant.precio
                    tenant.precio = "{:,.2f}".format(float(precio_temp.replace(',','')))

                tenant.precio_en_letra = tenant.precio_en_letra.upper()
                tenant.servicios = tenant.servicios.lower()
                if 'PESOS' in tenant.precio_en_letra:
                    tenant.precio_en_letra = tenant.precio_en_letra.replace('PESOS', '')

                tenant.save()

                return redirect('update_success')  # Redirect to a success page
        else:
            # Transform data before rendering the form
            # tenant.name = tenant.name.upper()
            # tenant.precio_en_letra = tenant.precio_en_letra.upper()
            # tenant.servicios = tenant.servicios.lower()
            # if 'PESOS' in tenant.precio_en_letra:
            #    tenant.precio_en_letra = tenant.precio_en_letra.replace('PESOS', '')

            # if not '.00' in tenant.precio:
            #     tenant.precio = f'{tenant.precio}.00'

            # tenant.save()

            form = TenantForm(instance=tenant)

        return render(request, 'recibos/update_tenant.html', {'form': form, 'editing_tenant': tenant})
    else:
        # Display the list of tenants
        return render(request, 'recibos/update_tenants.html', {'tenants': tenants})


def update_success(request):
    return render(request, 'recibos/update_success.html')

def contracts_update_success(request):
    return render(request, 'contratos/update_success.html')

def add_tenant(request):
    if request.method == 'POST':
        form = TenantForm(request.POST)

        if form.is_valid():
            # Transform data before saving
            name = form.cleaned_data['name'].upper()
            precio_en_letra = form.cleaned_data['precio_en_letra'].upper()
            servicios = form.cleaned_data['servicios'].lower()
            local = form.cleaned_data['local']
            dia = form.cleaned_data['dia']
            precio = form.cleaned_data['precio']

            if 'PESOS' in precio_en_letra:
                precio_en_letra = precio_en_letra.replace('PESOS', '')


            precio = "{:,.2f}".format(float(precio.replace(',','')))


            # Create a new instance of your model and set the fields
            new_tenant = Tenant(
                name=name,
                precio_en_letra=precio_en_letra,
                servicios=servicios,
                dia=dia,
                precio=precio,
                local=local
                # Add other fields as needed
            )

            # Save the new instance
            new_tenant.save()
            return redirect('update_tenants')  # Redirect to the same page after adding a tenant
    else:
        form = TenantForm()

    return render(request, 'recibos/add_tenant.html', {'form': form})


def delete_tenant(request, tenant_name):
    tenant = get_object_or_404(Tenant, name=tenant_name)

    if request.method == 'POST':
        tenant.delete()
        return redirect('generate_pdfs')  # Redirect to the home page or another appropriate page

    return render(request, 'recibos/delete_tenant.html', {'tenant': tenant})


def all_contracts(request, tenant_name=None):
    contracts = Contract.objects.all()

    if tenant_name:
        # Get the tenant instance
        contract = Contract.objects.get(nombre_arrendatario=tenant_name)

        if request.method == 'POST':
            form = ContractForm(request.POST, instance=contract)
            if form.is_valid():
                # Save the changes
                form.save()
                if not ',' in contract.precio:
                    contract.precio = "{:,.2f}".format(float(contract.precio))

                elif ',' in contract.precio:
                    precio_temp = contract.precio
                    contract.precio = "{:,.2f}".format(float(precio_temp.replace(',','')))

                contract.precio_en_letra = contract.precio_en_letra.upper()
                contract.servicios = contract.servicios.lower()
                if 'PESOS' in contract.precio_en_letra:
                    contract.precio_en_letra = contract.precio_en_letra.replace('PESOS', '')

                contract.save()

                return redirect('contracts_update_success')  # Redirect to a success page
        else:
            # Transform data before rendering the form
            # tenant.name = tenant.name.upper()
            # tenant.precio_en_letra = tenant.precio_en_letra.upper()
            # tenant.servicios = tenant.servicios.lower()
            # if 'PESOS' in tenant.precio_en_letra:
            #    tenant.precio_en_letra = tenant.precio_en_letra.replace('PESOS', '')

            # if not '.00' in tenant.precio:
            #     tenant.precio = f'{tenant.precio}.00'

            # tenant.save()

            form = ContractForm(instance=contract)

        return render(request, 'contratos/update_contract.html', {'form': form, 'editing_tenant': contract})
    else:
        # Display the list of tenants

        return render(request,'contratos/all_contracts.html', {'contracts': contracts})
    

def add_contract(request):
    if request.method == 'POST':
        form = ContractForm(request.POST)

        if form.is_valid():
            # Transform data before saving
            nombre_arrendatario = form.cleaned_data['nombre_arrendatario'].upper()
            ine_arrendatario = form.cleaned_data['ine_arrendatario'].upper()
            precio_en_letra = form.cleaned_data['precio_en_letra'].upper()
            servicios = form.cleaned_data['servicios'].lower()
            local = form.cleaned_data['local']
            dia_de_pago = form.cleaned_data['dia_de_pago']
            fecha_inicio_contrato = form.cleaned_data['fecha_inicio_contrato']
            fecha_vencimiento_contrato = form.cleaned_data['fecha_vencimiento_contrato']
            precio = form.cleaned_data['precio']


            if 'PESOS' in precio_en_letra:
                precio_en_letra = precio_en_letra.replace('PESOS', '')


            precio = "{:,.2f}".format(float(precio.replace(',','')))


            # Create a new instance of your model and set the fields
            new_contract = Contract(
                nombre_arrendatario=nombre_arrendatario,
                ine_arrendatario=ine_arrendatario,
                precio_en_letra=precio_en_letra,
                servicios=servicios,
                dia_de_pago=dia_de_pago,
                precio=precio,
                fecha_inicio_contrato=fecha_inicio_contrato,
                fecha_vencimiento_contrato=fecha_vencimiento_contrato,
                local=local
                # Add other fields as needed
            )

            # Save the new instance
            new_contract.save()
            return redirect('all_contracts')  # Redirect to the same page after adding a tenant
    else:
        form = ContractForm()

    return render(request, 'contratos/add_contract.html', {'form': form})


def delete_contract(request, tenant_name):
    contract = get_object_or_404(Contract, nombre_arrendatario=tenant_name)

    if request.method == 'POST':
        contract.delete()
        return redirect('generate_pdfs')  # Redirect to the home page or another appropriate page

    return render(request, 'contratos/delete_contract.html', {'tenant': contract})