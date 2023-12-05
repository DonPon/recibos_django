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

import tempfile


def create_pdf(subject, text, month, name):
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

    # Save the document.
    # Specify the folder path
    folder_path = "C:/Users/4PF26LA_RS5/Desktop/Recibos/"
    # Check if the folder exists
    if not os.path.exists(folder_path):
        # Create the folder if it doesn't exist
        os.makedirs(folder_path)

    filename = f"C:/Users/4PF26LA_RS5/Desktop/Recibos/Recibo_{month.upper()}_{name}.pdf"
    pdf.output(filename)

def create_pdf_download(request, subject, text, month, name):
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
    folder_path = "C:/Users/4PF26LA_RS5/Desktop/Recibos/"

    # Create the folder if it doesn't exist
    #if not os.path.exists(folder_path):
    #    os.makedirs(folder_path)

    # Define the filename
    filename = f"Recibo_{month.upper()}_{name}.pdf"

    # Create the full filepath
    filepath = os.path.join(folder_path, filename)

    # Save the document
    pdf.output(filename)

    # Open the file for reading in binary mode
    with open(filename, 'rb') as file:
        # Create an HttpResponse with the file's content for download
        response = HttpResponse(file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename={filename}'

    # Delete the file
    #os.remove(filename)

    return filename


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
    filename = f"Recibo_{month.upper()}_{name}.pdf"

    # Create the full filepath
    #filepath = os.path.join(folder_path, filename)

    # Save the document
    pdf.output(filename)

    return(filename)



    #return HttpResponse("Email sent successfully!")

def send_emails(files, month):
    # Compose the email
    subject = f"Recibos_{month.upper()}"
    body = f"Recibos para el mes de {month}"
    from_email = "franzeckermann@gmail.com"
    to_email = "franzeckermann@gmail.com"

    # Create a multipart message
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = from_email
    message['To'] = to_email
    message.attach(MIMEText(body, 'plain'))

    for attachment_path in files:
        with open(attachment_path, 'rb') as file:
            attachment = MIMEApplication(file.read(), _subtype="pdf")
            attachment.add_header('Content-Disposition', 'attachment', filename=attachment_path)
            message.attach(attachment)

    # Connect to the SMTP server and send the email
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'franzeckermann@gmail.com'
    smtp_password = 'emak djiq houm atdb'

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(from_email, to_email, message.as_string())

    # Delete the file
    for filename in files:
        os.remove(filename)

