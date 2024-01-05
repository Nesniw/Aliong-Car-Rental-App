from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph,  Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(data):
    pdf_filename = 'booking_report.pdf'

    # Create PDF with landscape orientation
    doc = SimpleDocTemplate(pdf_filename, pagesize=landscape(letter))
    
    # Content
    content = []

    # Header
    table_headers = ["ID Booking", "ID Mobil", "Username", "Tanggal Pinjam", "Lama Pinjam", "Tanggal Kembali", "Harga per Hari", "Denda", "Total Biaya", "Status Booking"]
    content.append(table_headers)

    # Data rows
    for row_data in data:
        # Pilih data yang ingin dimasukkan ke dalam PDF
        selected_data = [row_data[0], row_data[1], row_data[2], row_data[3], row_data[4], row_data[6], row_data[7], row_data[8],  row_data[9], row_data[10]]
        content.append(selected_data)

    # Create table
    table = Table(content)

    # Add style to table
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    table.setStyle(style)

    # Build PDF
    doc.build([Paragraph("<b>Data Booking / Transaksi</b>", getSampleStyleSheet()['Title']), Spacer(1, 12), table])

    return pdf_filename