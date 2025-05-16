import os
import re
import json

# Input and output directories

# Current file's directory
current_dir = os.path.dirname(__file__)

# Go up one directory
parent_dir = os.path.dirname(current_dir)

INPUT_DIR  = os.path.join(parent_dir, 'Data/raw_text/Reference')
OUTPUT_DIR = os.path.join(parent_dir, 'Data/Segmented_Reference')

# Regex patterns for section headers
SECTION_PATTERNS = {
    'abstract':     r'^\s*(?:\d+\s*(?:[.)])?\s*)?Abstract\s*:?.*$',
    'introduction': r'^\s*(?:\d+\s*(?:[.)])?\s*)?Introduction\s*:?.*$',
    'related_work': r'^\s*(?:\d+\s*(?:[.)])?\s*)?Related\s+Work\s*:?.*$',
    'methodology':  r'^\s*(?:\d+\s*(?:[.)])?\s*)?Methodology\s*:?.*$',
    'experiments':  r'^\s*(?:\d+\s*(?:[.)])?\s*)?Experiments\s*:?.*$',
    'results':      r'^\s*(?:\d+\s*(?:[.)])?\s*)?Results\s*:?.*$',
    'conclusion':   r'^\s*(?:\d+\s*(?:[.)])?\s*)?Conclusion\s*:?.*$',
}

# Pre-compile regex patterns
HEADER_PATTERNS = [
    (sec, re.compile(pat, re.IGNORECASE | re.MULTILINE))
    for sec, pat in SECTION_PATTERNS.items()
]

# Order of keys in our output JSON
OUTPUT_KEYS = ['title'] + list(SECTION_PATTERNS.keys())

def segment_sections(text):
    matches = []
    for sec, patt in HEADER_PATTERNS:
        for m in patt.finditer(text):
            matches.append((m.start(), sec, m.end()))
    matches.sort(key=lambda x: x[0])

    sections = {k: '' for k in OUTPUT_KEYS}

    if not matches:
        sections['title'] = text.strip()
        return sections

    first_pos = matches[0][0]
    sections['title'] = text[:first_pos].strip()

    for idx, (start, sec, end) in enumerate(matches):
        next_start = matches[idx+1][0] if idx+1 < len(matches) else len(text)
        sections[sec] = text[end:next_start].strip()

    return sections

def process_directory(input_dir, output_dir):
    for root, dirs, files in os.walk(input_dir):
        rel_path = os.path.relpath(root, input_dir)
        out_dir = os.path.join(output_dir, rel_path)
        os.makedirs(out_dir, exist_ok=True)

        for file in files:
            if file.lower().endswith('.txt'):
                in_path = os.path.join(root, file)
                with open(in_path, encoding='utf-8') as f:
                    raw_text = f.read()

                segments = segment_sections(raw_text)
                base_name = os.path.splitext(file)[0]
                out_path = os.path.join(out_dir, base_name + '.json')

                with open(out_path, 'w', encoding='utf-8') as fo:
                    json.dump(segments, fo, indent=2)
                print(f"Segmented {in_path} → {out_path}")
def main():
    if not os.path.isdir(INPUT_DIR):
        print(f"Error: input folder not found: {INPUT_DIR}")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    process_directory(INPUT_DIR, OUTPUT_DIR)

if __name__ == '__main__':
    main()
