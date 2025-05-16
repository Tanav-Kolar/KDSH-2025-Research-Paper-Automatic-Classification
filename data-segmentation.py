import os
import re
import json

#Paths for input and output.
INPUT_DIR  = 'data/raw_text/papers'
OUTPUT_DIR = 'data/sections'

#Regex patterns for section headers.
SECTION_PATTERNS = {
    'abstract':     r'^\s*(?:\d+\s*(?:[.)])?\s*)?Abstract\s*:?\s*$',
    'introduction': r'^\s*(?:\d+\s*(?:[.)])?\s*)?Introduction\s*:?\s*$',
    'related_work': r'^\s*(?:\d+\s*(?:[.)])?\s*)?Related\s+Work\s*:?\s*$',
    'methodology':  r'^\s*(?:\d+\s*(?:[.)])?\s*)?Methodology\s*:?\s*$',
    'experiments':  r'^\s*(?:\d+\s*(?:[.)])?\s*)?Experiments\s*:?\s*$',
    'results':      r'^\s*(?:\d+\s*(?:[.)])?\s*)?Results\s*:?\s*$',
    'conclusion':   r'^\s*(?:\d+\s*(?:[.)])?\s*)?Conclusion\s*:?\s*$',
}

#Pre-compile regex patterns for efficiency.
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

def main():
    if not os.path.isdir(INPUT_DIR):
        print(f"Error: input folder not found: {INPUT_DIR}")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    txts = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith('.txt')]
    if not txts:
        print(f"No .txt files in {INPUT_DIR}")
        return

    for fn in txts:
        in_path = os.path.join(INPUT_DIR, fn)
        raw = open(in_path, encoding='utf-8').read()
        segs = segment_sections(raw)

        base = os.path.splitext(fn)[0]
        out_path = os.path.join(OUTPUT_DIR, base + '.json')
        with open(out_path, 'w', encoding='utf-8') as fo:
            json.dump(segs, fo, indent=2)

        print(f"Segmented {fn} → {base}.json")

if __name__ == '__main__':
    main()



