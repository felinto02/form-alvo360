import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
import tempfile
import os

def gerar_pdf_qrcode(cliente_id):
    # Define o link com base no cliente_id
    link = f"https://alvo360.onrender.com/{cliente_id}"

    # Gera o QR Code com o link
    qr = qrcode.make(link)
    qr_image = BytesIO()
    qr.save(qr_image, format='PNG')
    qr_image.seek(0)

    # Cria um arquivo temporário para armazenar a imagem do QR Code
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        temp_file.write(qr_image.getvalue())
        temp_file_path = temp_file.name  # Caminho do arquivo temporário

    # Cria um objeto PDF em memória
    pdf_buffer = BytesIO()
    pdf = canvas.Canvas(pdf_buffer, pagesize=A4)

    # Configurações do PDF
    largura, altura = A4
    pdf.setFont("Helvetica", 12)  # Define a fonte para o texto
    pdf.drawString(100, altura - 100, f"QR Code para o cliente {cliente_id}")

    # Insere a imagem do QR Code no PDF a partir do arquivo temporário
    pdf.drawImage(temp_file_path, 100, altura - 300, width=150, height=150)

    # Salva o PDF
    pdf.save()
    pdf_buffer.seek(0)

    # Remove o arquivo temporário após gerar o PDF
    os.remove(temp_file_path)

    return pdf_buffer
