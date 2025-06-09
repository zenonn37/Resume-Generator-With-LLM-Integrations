```markdown
# Resume CLI Generator

A simple, extensible command-line tool to build professional PDF resumes from structured JSON data. Includes interactive editing, AI-powered text-to-JSON conversion, and customizable templates—ideal for software engineers, security specialists, and contractors.

## Features

- **JSON-driven**: Keep your personal, skills, projects, education, and certifications data in `/data/*.json`
- **PDF Output**: One-command resume generation (`--generate`) produces a polished `resume.pdf`
- **Interactive Editing**: Update any section on the fly (`--update`)
- **AI Enrichment**: Convert free-text into structured JSON via OpenAI or Hugging Face (`--section`)
- **Modular & Extendable**: Plug in custom templates or data sources to suit your workflow

## Getting Started

### Prerequisites

- Python 3.7+
- `reportlab` for PDF generation
- (Optional) `openai` or `requests` for AI integration

```bash
pip install reportlab openai requests
```

### Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/resume-cli.git
   cd resume-cli
   ```

2. **Populate data files**  
   Place your JSON files in the `/data` directory:
   - `personal.json`
   - `skills.json`
   - `projects.json`
   - `education.json`
   - `certs.json`  
   *(Use provided placeholders as starting point)*

3. **Configure AI (optional)**
   - For OpenAI: Set `OPENAI_API_KEY` in environment
   - For Hugging Face: Set `HF_API_TOKEN`

### Usage

```bash
# 1. Interactive update of all sections
python resume_cli.py --update

# 2. Generate the PDF resume
python resume_cli.py --generate

# 3. Convert free-text into JSON (e.g. personal section)
python resume_cli.py --section personal \
    --text "Alex Morgan, a cybersecurity engineer with expertise..." \
    --api openai
```

## Customization

- **Templates**: Swap/extend `draw_paragraph` and layout code in `resume_cli.py`
- **New Sections**: Add JSON files + rendering blocks for certifications/languages/publications
- **Output Formats**: Integrate other libraries for Word/HTML exports

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/YourFeature`
3. Commit changes: `git commit -m "Add YourFeature"`
4. Push branch: `git push origin feature/YourFeature`
5. Open pull request

## License

Released under [MIT License](LICENSE). Use, modify, and distribute freely.
```
