from django.core.files.storage import default_storage
import fpdf
import datetime
from .src_email import send_email
from .strings import constructor_contract_local_comercial, constructor_contract_departamento, constructor_convenio_terminacion_entrega


class BasePDF(fpdf.FPDF):
    def header(self):
        # Si quieres meter logo o encabezado fijo, lo haces aquí
        pass

    def footer(self):
        self.set_font('Helvetica', 'I', 10)
        self.set_y(-15)
        self.cell(0, 10, str(self.page_no()), 0, 0, 'R')

def base_generate_pdf(item_dict, constructor_fn, filename_prefix="contrato"):
    """
    Genera un PDF genérico con un constructor y un prefijo de nombre de archivo.
    """
    contract, signatures = constructor_fn(item_dict=item_dict)

    pdf = BasePDF(format='Legal')
    pdf.set_margins(left=30, top=15, right=30)
    pdf.add_page()
    pdf.set_font('Helvetica', '', 12)

    for item in contract:
        if '%TITLE%' in item:
            pdf.cell(0, 6, item.replace('%TITLE%', ''), align='C', markdown=True, center=True)
            pdf.ln(2)
        else:
            pdf.multi_cell(0, 6, item, align='J', markdown=True)

    with pdf.table(text_align="CENTER") as table:
        for data_row in signatures:
            row = table.row()
            for datum in data_row:
                row.cell(datum)

    filename = f"{filename_prefix}_{item_dict['nombre_arrendatario'].replace(' ', '_').replace('.','_')}.pdf"
    pdf.output(name=filename)
    return filename

def create_contract_pdf(item_dict):
    """
    Genera contrato PDF en base al tipo.
    """
    if item_dict['contract_type'] == 'local_comercial':
        return base_generate_pdf(item_dict, constructor_contract_local_comercial, filename_prefix="contrato")
    elif item_dict['contract_type'] == 'departamento':
        return base_generate_pdf(item_dict, constructor_contract_departamento, filename_prefix="contrato")
    else:
        raise KeyError("Invalid contract_type")
    
def create_terminacion_entrega_pdf(item_dict):
    """
    Genera PDF para convenio de terminación/entrega.
    """
    return base_generate_pdf(item_dict, constructor_convenio_terminacion_entrega, filename_prefix="terminacion_entrega")

def create_recibo_pdf(subject, text, month, name):
    """
    Create a PDF document for an email receipt.
    Args:
        subject (str): The subject text to be included in the PDF.
        text (str): The body text to be included in the PDF.
        month (str): The month to be included in the filename.
        name (str): The name to be included in the filename.
    Returns:
        str: The filename of the created PDF document.
    """
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

    # Define the filename
    filename = f"Recibo_{month.upper()}_{name.upper()}.pdf"
    pdf.output(name=filename)

    return filename

def send_emails_recibos(files, month, to_email):
    """
    Wrapper for the `send_email` function to send receipts for a specific month.
    Args:
        files (list): List of file paths to be attached to the email.
        month (str): The month for which the receipts are being sent.
        to_email (str): The recipient's email address.
    """
    # Compose the email
    subject = f"Recibos {month.upper()}"
    body = f"Recibos para el mes de {month}"

    if isinstance(files, str):
        files = [files]

    send_email(subject=subject, body=body, to_email=to_email, file_paths=files)

def old_create_contract_pdf(item_dict):
    """
    Generates a PDF contract based on the provided item dictionary.
    Args:
        item_dict (dict): A dictionary containing contract details. Must include a 'contract_type' key 
                          with values 'local_comercial' or 'departamento'.
    Returns:
        str: The filename of the generated PDF.
    Raises:
        KeyError: If 'contract_type' is not in item_dict or has an invalid value.
        Exception: For any other errors during PDF creation.
    """
    # define constructor functions depending on the contract type
    if item_dict['contract_type'] == 'local_comercial':
        contract, signatures = constructor_contract_local_comercial(item_dict=item_dict)
    elif item_dict['contract_type'] == 'departamento':
        contract, signatures = constructor_contract_departamento(item_dict=item_dict)

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
    # Add a new page.
    pdf.add_page()
    # Reset font for body text
    pdf.set_font('Helvetica', '', 12)

    for item in contract:
        if '%TITLE%' in item:
            pdf.cell(0, 6, item.replace('%TITLE%', ''), align='C', markdown=True, center=True)
            pdf.ln(2)
        else:
            pdf.multi_cell(0, 6, item, align='J', markdown=True)

    with pdf.table(text_align="CENTER") as table:
        for data_row in signatures:
            row = table.row()
            for datum in data_row:
                row.cell(datum)

    filename = f"contrato_{item_dict['nombre_arrendatario'].replace(' ', '_').replace('.','_')}.pdf"
    pdf.output(name=filename)
    return filename

def old_create_terminacion_entrega_pdf(item_dict):
    """
    Generates a PDF termination of delivery based on the provided item dictionary.
    Args:
        item_dict (dict): A dictionary containing contract details. Must include a 'contract_type' key 
                          with values 'local_comercial' or 'departamento'.
    Returns:
        str: The filename of the generated PDF.
    Raises:
        KeyError: If 'contract_type' is not in item_dict or has an invalid value.
        Exception: For any other errors during PDF creation.
    """
    # define constructor
    contract, signatures = constructor_convenio_terminacion_entrega(item_dict=item_dict)


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
    # Add a new page.
    pdf.add_page()
    # Reset font for body text
    pdf.set_font('Helvetica', '', 12)

    for item in contract:
        if '%TITLE%' in item:
            pdf.cell(0, 6, item.replace('%TITLE%', ''), align='C', markdown=True, center=True)
            pdf.ln(2)
        else:
            pdf.multi_cell(0, 6, item, align='J', markdown=True)

    with pdf.table(text_align="CENTER") as table:
        for data_row in signatures:
            row = table.row()
            for datum in data_row:
                row.cell(datum)

    filename = f"contrato_{item_dict['nombre_arrendatario'].replace(' ', '_').replace('.','_')}.pdf"
    pdf.output(name=filename)
    return filename

def send_emails_contracts(file_path, identifier, to_email):
    """
    Wrapper for the `send_email` function to send contracts via email.
    Args:
        file_path (str or list): Path(s) to the contract file(s) to be attached to the email.
        identifier (str): Identifier for the contract, used in the email subject and body.
        to_email (str): The recipient's email address.
    """
    # Compose the email
    subject = f"Contrato {identifier.upper()}"
    body = f"Copia de contrato de {identifier.upper()}"

    if isinstance(file_path, str):
        file_path = [file_path]

    send_email(subject=subject, body=body, to_email=to_email, file_paths=file_path)

def send_emails_recibos_on_demand(files, concepto, name, to_email):
    """
    Wrapper for the `send_email` function to send receipts on demand.
    Args:
        files (list): List of file paths to be attached to the email.
        concepto (str): The concept or reason for the receipt.
        name (str): The name of the recipient.
        to_email (str): The recipient's email address.
    """
    # Compose the email
    subject = f"Recibo {concepto.upper()} - {name.upper()}"
    body = f"Recibo {concepto.upper()} - {name.upper()}."

    if isinstance(files, str):
        files = [files]

    send_email(subject=subject, body=body, to_email=to_email, file_paths=files)