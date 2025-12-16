# export_pdf.py
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

def export_to_pdf(results, filename="Cleanup_Report.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 22)
    c.drawString(50, height - 80, "Clean Impact for the Waves")

    c.setFont("Helvetica", 14)
    c.drawString(50, height - 110,
                 "SDG 14 – Marine Pollution Reduction Report")

    c.setFont("Helvetica-Oblique", 12)
    c.drawString(50, height - 140,
                 f"Generated: {datetime.now().strftime('%B %d, %Y  %I:%M %p')}")

    c.line(50, height - 150, 560, height - 150)

    c.setFont("Helvetica", 14)
    y = height - 190

    data = [
        f"Volunteers: {results['volunteers']}",
        f"Trash Bags: {results['bags']}",
        f"Waste Removed: {results['waste_kg']:.1f} kg",
        f"Plastic Reduced: {results['plastic_reduction']:.1f} kg",
        f"Marine Animals Helped: {results['animals_helped']}",
    ]

    for line in data:
        c.drawString(50, y, line)
        y -= 25

    c.setFont("Helvetica-Oblique", 12)
    c.drawString(50, 40, "Thank you for protecting marine life!")

    c.save()
    return filename
