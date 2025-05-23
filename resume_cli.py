# resume_cli.py
"""
Unified Resume CLI Tool

Generates PDF resumes, updates JSON data, and converts free-text into structured JSON via LLM.

Usage:
  1. Populate initial JSON files in /data (or use --section to auto-generate via AI).
  2. Generate PDF: python resume_cli.py --generate
  3. Update any section interactively: python resume_cli.py --update
  4. Convert free-text to JSON for a section: python resume_cli.py --section personal --text "Your details here" --api openai
Sections: personal, skills, projects, education, certifications
"""
import os
import json
import argparse
import requests
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import textwrap

data_dir = os.path.join(os.path.dirname(__file__), 'data')

# ------------ JSON I/O Utilities ------------
def load_json(filename):
    try:
        with open(os.path.join(data_dir, filename), 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {} if filename.endswith('.json') else []

def save_json(filename, data):
    with open(os.path.join(data_dir, filename), 'w') as f:
        json.dump(data, f, indent=2)

# ------------ Drawing Utility ------------
def draw_paragraph(c, text, x, y, max_width, line_height=12):
    for line in textwrap.wrap(text, width=int(max_width/6)):
        c.drawString(x, y, line)
        y -= line_height
    return y

# ------------ Interactive Updater ------------
def interactive_update():
    files = ['personal.json','skills.json','projects.json','education.json','certs.json']
    for fname in files:
        data = load_json(fname)
        print(f"\n--- {fname} ---")
        if isinstance(data, dict):
            for k,v in data.items():
                val = input(f"{k} [{v}]: ")
                if val.strip(): data[k] = val.strip()
        elif isinstance(data, list):
            print("Entries:")
            for i,item in enumerate(data,1): print(f" {i}. {item}")
            if input("Add new? (y/n):").lower()=='y':
                ent = input("New JSON or text:")
                try: data.append(json.loads(ent))
                except: data.append(ent)
        save_json(fname, data)
    print("Interactive update complete.")

# ------------ LLM Conversion ------------
def call_llm(api_type, prompt, **kwargs):
    if api_type=='openai':
        import openai
        openai.api_key = os.getenv('OPENAI_API_KEY')
        resp = openai.ChatCompletion.create(
            model=kwargs.get('model','gpt-3.5-turbo'),
            messages=[{'role':'user','content':prompt}]
        )
        return resp.choices[0].message.content.strip()
    elif api_type=='huggingface':
        token=os.getenv('HF_API_TOKEN'); headers={"Authorization":f"Bearer {token}"}
        url=kwargs.get('endpoint','https://api-inference.huggingface.co/models/gpt2')
        r=requests.post(url,headers=headers,json={"inputs":prompt})
        return r.json()[0].get('generated_text','')
    else:
        raise ValueError("Unsupported API")

def section_to_json(section, text, api):
    prompt=f"Convert the following into JSON for '{section}': {text}"
    out=call_llm(api,prompt)
    fname = {'certifications':'certs.json'}.get(section,f"{section}.json")
    data=json.loads(out)
    save_json(fname, data)
    print(f"Updated {fname} via {api}.")

# ------------ PDF Generation ------------
def generate_pdf():
    files = {
        'personal':'personal.json',
        'skills':'skills.json',
        'projects':'projects.json',
        'education':'education.json',
        'certifications':'certs.json'
    }
    data = {k: load_json(v) for k,v in files.items()}
    c=canvas.Canvas(os.path.join(data_dir,'resume.pdf'),pagesize=letter)
    w,h=letter; y=h-50
    # Header
    c.setFont("Helvetica-Bold",18); c.drawString(50,y,data['personal'].get('name',''))
    y-=25; c.setFont("Helvetica",10)
    cnt=f"Email:{data['personal'].get('email','')} | Phone:{data['personal'].get('phone','')}"
    c.drawString(50,y,cnt); y-=30
    # Summary
    c.setFont("Helvetica-Bold",12); c.drawString(50,y,"PROFESSIONAL SUMMARY"); y-=15
    c.setFont("Helvetica",10); y=draw_paragraph(c,data['personal'].get('summary',''),50,y,500); y-=10
    # Skills
    c.setFont("Helvetica-Bold",12); c.drawString(50,y,"TECHNICAL SKILLS"); y-=15
    c.setFont("Helvetica",10)
    for s in data['skills']: c.drawString(60,y,f"• {s}"); y-=12
    y-=10
    # Projects
    c.setFont("Helvetica-Bold",12); c.drawString(50,y,"PROJECTS"); y-=15; c.setFont("Helvetica",10)
    for p in data['projects']:
        c.setFont("Helvetica-Bold",10); c.drawString(60,y,p.get('title','')); y-=12
        c.setFont("Helvetica",10); y=draw_paragraph(c,p.get('description',''),70,y,470); y-=8
    # Education
    c.setFont("Helvetica-Bold",12); c.drawString(50,y,"EDUCATION"); y-=15; c.setFont("Helvetica",10)
    for e in data['education']:
        c.drawString(60,y,f"{e.get('degree')} | {e.get('institution')} | {e.get('location')}"); y-=12
        dt=f"{e.get('start')} - {e.get('end')}" + (f" | {e.get('notes')}" if e.get('notes') else "")
        c.drawString(70,y,dt); y-=20
    # Certifications
    c.setFont("Helvetica-Bold",12); c.drawString(50,y,"CERTIFICATIONS"); y-=15; c.setFont("Helvetica",10)
    for ctf in data['certifications']: c.drawString(60,y,f"• {ctf}"); y-=12
    c.save(); print("Generated resume.pdf in data directory.")

# ------------ CLI Entrypoint ------------
def main():
    p=argparse.ArgumentParser()
    p.add_argument('--update',action='store_true')
    p.add_argument('--generate',action='store_true')
    p.add_argument('--section',choices=['personal','skills','projects','education','certifications'])
    p.add_argument('--text',help='Free-text for section conversion')
    p.add_argument('--api',choices=['openai','huggingface'])
    args=p.parse_args()

    if args.update: interactive_update()
    elif args.generate: generate_pdf()
    elif args.section and args.text and args.api: section_to_json(args.section,args.text,args.api)
    else: print("Use --help for options.")

if __name__=='__main__': main()
