from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_pdf_report(incidents, maintenance):
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"report_{now}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "FlightOps Incident Dashboard – Report")
    y -= 30

    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Datum: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    y -= 40

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Aktive Incidents:")
    y -= 20
    c.setFont("Helvetica", 11)

    for i in incidents:
        c.drawString(60, y, f"- {i['system']} | {i['priority']} | {i['message']}")
        y -= 15

    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Geplante Wartungen:")
    y -= 20
    c.setFont("Helvetica", 11)

    for m in maintenance:
        c.drawString(60, y, f"- {m['system']} | {m['window']} | {m['note']}")
        y -= 15

    c.save()
