Modular I/O: Load and save JSON, plus CLI prompts to update any data file.

Resume Variants: Easily extendable for different templates.

LLM Integration: Hooks for OpenAI or HuggingFace inference to enrich or draft JSON entries.

Detailed Method Comments: Each function includes docstrings for GitHub collaboration.

resume_cli.py, a single script that:

    --update — Interactively edit any JSON section.

    --generate — Build data/resume.pdf from JSON.

    --section <name> --text "<your text>" --api <openai|huggingface> — Convert free-text into structured JSON for that section.

First Run Recommendation:

    Populate your /data/*.json (you can start with the placeholders).

    Run python resume_cli.py --generate to get your first resume.pdf.

    Later, use --update or --section flows to refine.

    USAGE:
# Prompt to update your JSON data interactively:
python resume_generator.py --update
# Enrich input data via an LLM (requires env var OPENAI_API_KEY or HF_API_TOKEN):
python resume_generator.py --api openai
# Generate the PDF:
python resume_generator.py --generate

