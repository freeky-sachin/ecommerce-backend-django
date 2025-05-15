from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_invoice(payment):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "INVOICE")

    # Payment Info
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"User: {payment.user.email}")
    c.drawString(50, height - 120, f"Amount Paid: ₹{payment.amount}")
    c.drawString(50, height - 140, f"Currency: {payment.currency}")
    c.drawString(50, height - 160, f"Payment Status: {payment.status}")
    c.drawString(50, height - 180, f"Payment ID: {payment.payment_intent}")
    c.drawString(50, height - 200, f"Date: {payment.created_at.strftime('%Y-%m-%d %H:%M:%S')}")

    # Extra Context
    if payment.rental:
        c.drawString(50, height - 240, f"Rental Product: {payment.rental.product.name}")
    if payment.subscription:
        c.drawString(50, height - 240, f"Subscription Box: {payment.subscription.box_type}")

    # Footer
    c.drawString(50, 50, "Thank you for your purchase!")

    c.save()
    buffer.seek(0)
    return buffer
