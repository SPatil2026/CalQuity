"""
Generate a sample PDF for testing the application.
Run: python generate_sample_pdf.py
"""
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import os

def create_sample_pdf():
    pdf_dir = "pdfs"
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
    
    filename = os.path.join(pdf_dir, "sample_document.pdf")
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Page 1
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1*inch, height - 1*inch, "Sample Research Document")
    c.setFont("Helvetica", 12)
    c.drawString(1*inch, height - 1.5*inch, "This is a sample document for testing the AI Search Chat application.")
    c.drawString(1*inch, height - 2*inch, "Artificial Intelligence (AI) is transforming how we interact with technology.")
    c.drawString(1*inch, height - 2.5*inch, "Machine learning algorithms can process vast amounts of data efficiently.")
    c.drawString(1*inch, height - 3*inch, "Natural language processing enables computers to understand human language.")
    c.showPage()
    
    # Page 2
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, height - 1*inch, "Applications of AI")
    c.setFont("Helvetica", 12)
    c.drawString(1*inch, height - 1.5*inch, "AI is used in healthcare for diagnosis and treatment recommendations.")
    c.drawString(1*inch, height - 2*inch, "In finance, AI helps detect fraud and automate trading decisions.")
    c.drawString(1*inch, height - 2.5*inch, "Autonomous vehicles rely on AI for navigation and decision-making.")
    c.showPage()
    
    c.save()
    print(f"Sample PDF created: {filename}")

if __name__ == "__main__":
    # Note: Requires reportlab - install with: pip install reportlab
    try:
        create_sample_pdf()
    except ImportError:
        print("Please install reportlab: pip install reportlab")
