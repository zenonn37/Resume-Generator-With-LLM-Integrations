import os
import json
import argparse
from resume_generator import call_llm

data_dir = os.path.join(os.path.dirname(__file__), 'data')

section_map = {
    'personal': ['name','email','phone','linkedin','summary'],
    'skills': None,
    'projects': None,
    'education': None,
    'certifications': None
}

def write_section(section, content):
    """Save JSON content to the corresponding data file."""
    filename = f"{section}.json"
    data = json.loads(content)
    with open(os.path.join(data_dir, filename), 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Updated {filename}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--api', choices=['openai','huggingface'], required=True)
    parser.add_argument('--section', choices=section_map.keys(), required=True)
    parser.add_argument('text', help='Raw text to structure')
    args = parser.parse_args()

    prompt = f"Convert the following into a JSON array or object for the '{args.section}' section of a professional resume: {args.text}"  
    output = call_llm(args.api, prompt)
    write_section(args.section, output)

if __name__ == '__main__':
    main()
