from fpdf import FPDF
from recibos.src.strings import *


contract = constructor_contract()

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


filename = f"sample_contrato.pdf"
pdf.output(name=filename)
#pdf_content = ContentFile(pdf.output(name=filename).encode('latin-1'))

