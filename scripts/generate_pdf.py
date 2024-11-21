from io import BytesIO
from weasyprint import HTML

def generate_pdf_from_html(html_content):
    """
    Génère un fichier PDF à partir de HTML et retourne un flux binaire.
    """
    pdf_buffer = BytesIO()
    HTML(string=html_content).write_pdf(pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer
