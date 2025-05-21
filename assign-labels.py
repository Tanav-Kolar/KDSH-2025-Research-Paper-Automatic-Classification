import os, json
import pandas as pd

#Paths
SECTIONS_DIR    = 'data/sections'         
META_CSV        = 'data/metadata.csv'     
LABELED_DIR     = 'data/labeled_sections' 

meta = pd.read_csv(META_CSV, dtype={'paper_id': str})
meta.set_index('paper_id', inplace=True)

os.makedirs(LABELED_DIR, exist_ok=True)

#Iterate over all JSON files in the sections directory and assign labels based on metadata.
for fname in os.listdir(SECTIONS_DIR):
    if not fname.endswith('.json'):
        continue
    pid = os.path.splitext(fname)[0]
    seg = json.load(open(os.path.join(SECTIONS_DIR, fname), encoding='utf-8'))


    row = meta.loc[pid]

    # Assign Stage-1 label
    is_pub = 1 if (not row['is_reference']) or (row['ref_category']=='publishable') else 0
    seg['is_publishable'] = int(is_pub)

    #Assign Stage-2 labels
    seg['venue'] = row['venue_label'] if row.get('venue_label') and is_pub else None

    out_path = os.path.join(LABELED_DIR, f"{pid}.json")
    with open(out_path, 'w', encoding='utf-8') as fo:
        json.dump(seg, fo, indent=2)

    print(f"Labeled {pid}: publishable={seg['is_publishable']}, venue={seg['venue']}")
