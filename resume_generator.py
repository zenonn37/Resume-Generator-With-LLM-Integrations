import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import textwrap

# Utility to load JSON data from a file

def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

# Draw a wrapped paragraph

def draw_paragraph(c, text, x, y, max_width, line_height=12):
    for line in textwrap.wrap(text, width=int(max_width / 6)):  # approx chars per line
        c.drawString(x, y, line)
        y -= line_height
    return y

# Main resume generation

def generate_resume(data_files, output_path):
    # Load data
    personal = load_json(data_files['personal'])
    skills = load_json(data_files['skills'])
    projects = load_json(data_files['projects'])
    education = load_json(data_files['education'])
    certs = load_json(data_files['certifications'])

    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    y = height - 50

    # Header
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y, personal['name'])
    y -= 25
    c.setFont("Helvetica", 10)
    contact = f"Email: {personal['email']} | Phone: {personal['phone']} | LinkedIn: {personal['linkedin']}"
    c.drawString(50, y, contact)
    y -= 30

    # Summary
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "PROFESSIONAL SUMMARY")
    y -= 15
    c.setFont("Helvetica", 10)
    y = draw_paragraph(c, personal['summary'], 50, y, max_width=500)
    y -= 10

    # Technical Skills
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "TECHNICAL SKILLS")
    y -= 15
    c.setFont("Helvetica", 10)
    for skill in skills:
        c.drawString(60, y, f"• {skill}")
        y -= 12
    y -= 10

    # Projects
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "RELEVANT PROJECTS")
    y -= 15
    c.setFont("Helvetica", 10)
    for proj in projects:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(60, y, proj['title'])
        y -= 12
        c.setFont("Helvetica", 10)
        y = draw_paragraph(c, proj['description'], 70, y, max_width=470)
        y -= 8

    # Education
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "EDUCATION")
    y -= 15
    c.setFont("Helvetica", 10)
    for edu in education:
        line = f"{edu['degree']} | {edu['institution']} | {edu['location']}"
        c.drawString(60, y, line)
        y -= 12
        details = f"{edu['start']} - {edu['end']}" + (f" | {edu.get('notes')}" if edu.get('notes') else "")
        c.drawString(70, y, details)
        y -= 20

    # Certifications
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "CERTIFICATIONS")
    y -= 15
    c.setFont("Helvetica", 10)
    for cert in certs:
        c.drawString(60, y, f"• {cert}")
        y -= 12

    # Save PDF
    c.save()

# Example usage
if __name__ == '__main__':
    data_files = {
        'personal': 'data/personal.json',
        'skills': 'data/skills.json',
        'projects': 'data/projects.json',
        'education': 'data/education.json',
        'certifications': 'data/certs.json'
    }
    generate_resume(data_files, 'resume.pdf')
