from io import BytesIO
import pdfkit

def generate_pdf_from_html(html_content):
    """
    Génère un fichier PDF à partir de HTML et retourne un flux binaire.
    """
    options = {
        'page-size': 'A4',
        'encoding': 'UTF-8',
        'quiet': ''
    }
    pdf_buffer = BytesIO()
    pdfkit.from_string(html_content, pdf_buffer, options=options)
    pdf_buffer.seek(0)
    return pdf_buffer
