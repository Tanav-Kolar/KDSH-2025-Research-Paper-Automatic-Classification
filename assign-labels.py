import os, json
import pandas as pd

# 1) Paths
SECTIONS_DIR    = 'data/sections'         # your segmented JSONs
META_CSV        = 'data/metadata.csv'     # the file above
LABELED_DIR     = 'data/labeled_sections' # output

# 2) Load metadata
meta = pd.read_csv(META_CSV, dtype={'paper_id': str})
meta.set_index('paper_id', inplace=True)

# 3) Ensure output folder
os.makedirs(LABELED_DIR, exist_ok=True)

# 4) Iterate papers
for fname in os.listdir(SECTIONS_DIR):
    if not fname.endswith('.json'):
        continue
    pid = os.path.splitext(fname)[0]
    seg = json.load(open(os.path.join(SECTIONS_DIR, fname), encoding='utf-8'))

    # 5) Lookup metadata row (will KeyError if missing)
    row = meta.loc[pid]

    # 6) Assign Stage-1 label
    #    - training set (is_reference=False) → we assume publishable=1 by default
    #      *or* if you also have non-publishable examples in training, swap logic here
    is_pub = 1 if (not row['is_reference']) or (row['ref_category']=='publishable') else 0
    seg['is_publishable'] = int(is_pub)

    # 7) Assign Stage-2 label
    seg['venue'] = row['venue_label'] if row.get('venue_label') and is_pub else None

    # 8) Save out
    out_path = os.path.join(LABELED_DIR, f"{pid}.json")
    with open(out_path, 'w', encoding='utf-8') as fo:
        json.dump(seg, fo, indent=2)

    print(f"Labeled {pid}: publishable={seg['is_publishable']}, venue={seg['venue']}")
