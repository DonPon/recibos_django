from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files import File
import fpdf
import datetime
#import yaml
import os
import smtplib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from django.http import HttpResponse
from email import encoders
from django.conf import settings
import io
from .src_email import *
from .strings import *


def create_pdf_email(subject, text, month, name):
    # Create a new PDF document.
    pdf = fpdf.FPDF(format='Letter')

    # Set slightly larger margins
    pdf.set_margins(left=30, top=30, right=30)

    # Add a new page.
    pdf.add_page()

    # Set font for title
    pdf.set_font('Arial', 'B', 20)

    # Add the title text
    pdf.cell(0, 8, 'RECIBO', align='C')

    # Add a newline
    pdf.ln(20)

    # Reset font for body text
    pdf.set_font('Arial', '', 14)

    # Add the subject text
    pdf.multi_cell(0, 8, subject, align='R')

    # Add a newline
    pdf.ln(20)

    # Add the body text
    pdf.multi_cell(0, 8, text, align='J')

    # Add 5 new lines
    for i in range(7):
        pdf.ln(8)

    # Draw a signature line
    pdf.set_line_width(0.4)
    pdf.line(pdf.get_x() + 35, pdf.get_y(), pdf.get_x() + 120, pdf.get_y())

    # Add a newline
    pdf.ln(1)

    # Add signature text
    pdf.set_font('Arial', '', 14)
    pdf.multi_cell(0, 8, f'SRA. GABRIELA SEGURA\nLEYVA', align='C')

    # Specify the folder path
    '''folder_path = "C:/Users/4PF26LA_RS5/Desktop/Recibos/"

    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)'''

    # Define the filename
    filename = f"Recibo_{month.upper()}_{name.upper()}.pdf"

    # Create the full filepath using MEDIA_ROOT
    #filepath = os.path.join(settings.MEDIA_ROOT, filename)
    pdf.output(name=filename)
    #pdf_content = ContentFile(pdf.output(name=filename).encode('latin-1'))

    return filename



def send_emails(files, month):
    # Compose the email
    subject = f"Recibos {month.upper()}"
    body = f"Recibos para el mes de {month}"
    #from_email = "projects.franz@gmail.com"
    #to_email = "gabysurel@yahoo.com.mx"
    #cc_email = "franzeckermann@gmail.com"

    # Create a multipart message
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = from_email
    message['To'] = to_email
    message['Cc'] = cc_email
    message.attach(MIMEText(body, 'plain'))

    for file_path in files:

        with open(file_path, 'rb') as f:
            file_content = f.read()

        # Create a MIMEApplication with the file content
        attachment = MIMEApplication(file_content, _subtype="pdf")

        # Extract the filename from the file path
        filename = file_path.split('/')[-1]  # Adjust this based on your file paths
        attachment.add_header('Content-Disposition', 'attachment', filename=filename)
        
        # Attach the file to the email
        message.attach(attachment)

    # Connect to the SMTP server and send the email
    #smtp_server = 'smtp.gmail.com'
    #smtp_port = 587
    #smtp_username = 'projects.franz@gmail.com'
    #smtp_password = 'ugcx uano rucc rdko'


    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        recipients = [to_email, cc_email]
        server.sendmail(from_email, recipients, message.as_string())

    # Delete the files
    for file_path in files:
        default_storage.delete(file_path)

    for file_path_2 in files:
        os.remove(file_path_2)
        
#tenant1 = Tenant(name='JOSE ANTONIO HURTADO LOPEZ', dia='01', precio='6,580.00', precio_en_letra='SEIS MIL QUINIENTOS OCHENTA', servicios='renta y mantenimiento', local='26-C')
#tenant2 = Tenant(name='IRWING ARTURO PE?A VARGAS', dia='15', precio='10,500.00', precio_en_letra='DIEZ MIL QUINIENTOS', servicios='renta', local='5-B')
#tenant3 = Tenant(name='FRANCISCO SANCHEZ GALEANA', dia='15', precio='7,505.00', precio_en_letra='SIETE MIL QUINIENTOS CINCO', servicios='renta, mantenimiento, agua y luz', local='26')


def create_contract_pdf(text):

    contract, signatures = constructor_contract()
    
    class MyPDF(FPDF):
        def header(self):
            # Your header implementation here (if any)
            pass

        def footer(self):
            # Set font for the footer
            self.set_font('Helvetica', 'I', 10)

            # Position at 15 mm from bottom
            self.set_y(-15)

            # Add a page number as a footnote
            footnote_text = f"{self.page_no()}"
            self.cell(0, 10, footnote_text, 0, 0, 'R')

    # Create a new PDF document.
    pdf = MyPDF(format='Legal')
    # Set slightly larger margins
    pdf.set_margins(left=30, top=15, right=30)
    #Add a new page.
    pdf.add_page()
    # Reset font for body text
    pdf.set_font('Helvetica', '', 12)

    for item in contract:
        if '%TITLE%' in item:
            pdf.cell(0, 6, item.replace('%TITLE%',''), align='C', markdown=True)
            pdf.ln(2)
        else:
            pdf.multi_cell(0, 6, item, align='J', markdown=True)

    with pdf.table(text_align="CENTER") as table:
        for data_row in signatures:
            row = table.row()
            for datum in data_row:
                row.cell(datum)

    filename = f"sample_contrato.pdf"
    pdf.output(name=filename)
    return filename


def create_contract_from_md_files():
    contract, signatures = constructor_contract_2()

    class MyPDF(fpdf.FPDF):
        def header(self):
            # Your header implementation here (if any)
            pass

        def footer(self):
            # Set font for the footer
            self.set_font('Helvetica', 'I', 10)

            # Position at 15 mm from bottom
            self.set_y(-15)

            # Add a page number as a footnote
            footnote_text = f"{self.page_no()}"
            self.cell(0, 10, footnote_text, 0, 0, 'R')

    # Create a new PDF document.
    pdf = MyPDF(format='Legal')
    # Set slightly larger margins
    pdf.set_margins(left=30, top=15, right=30)
    #Add a new page.
    pdf.add_page()
    # Reset font for body text
    pdf.set_font('Helvetica', '', 12)

    for item in contract:
        if '%TITLE%' in item:
            pdf.ln(8)
            pdf.cell(0, 6, item.replace('%TITLE%',''), align='C', markdown=True)
            pdf.ln(8)
        else:
            pdf.multi_cell(0, 6, item, align='J', markdown=True)

    with pdf.table(text_align="CENTER") as table:
        for data_row in signatures:
            row = table.row()
            for datum in data_row:
                row.cell(datum)


    filename = f"sample_contrato.pdf"
    pdf.output(name=filename)
    #pdf_content = ContentFile(pdf.output(name=filename).encode('latin-1'))
    return filename