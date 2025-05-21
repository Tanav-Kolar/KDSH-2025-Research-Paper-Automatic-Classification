import os
import json
import pandas as pd

#Paths
META_CSV      = 'data/metadata.csv'
SEGMENTS_DIR  = 'data/sections/reference'
OUTPUT_DIR    = 'data/labeled_sections/reference'

#load metadata into a pandas dataframe
meta = pd.read_csv(META_CSV, dtype=str).fillna('')
meta.set_index('paper_id', inplace=True)

os.makedirs(OUTPUT_DIR, exist_ok=True)

for fname in os.listdir(SEGMENTS_DIR):
    if not fname.lower().endswith('.json'):
        continue

    pid = os.path.splitext(fname)[0]
    seg_path = os.path.join(SEGMENTS_DIR, fname)
    data = json.load(open(seg_path, encoding='utf-8'))

    if pid not in meta.index:
        raise KeyError(f"No metadata row for paper_id={pid}")

    row = meta.loc[pid]
    # parse CSV fields
    is_ref     = row['is_reference'].lower() in ('1','true','yes')
    ref_cat    = row['ref_category'].strip().lower()    
    venue      = row['venue_label'].strip()            

    # attach
    data['is_reference'] = is_ref
    data['ref_category'] = ref_cat if ref_cat else None
    # Stage-1 label: is_publishable
    data['is_publishable'] = int((not is_ref) or (ref_cat=='publishable'))
    # Stage-2 label: only for publishable cases
    data['venue']         = venue if data['is_publishable']==1 and venue else None

    # write out
    out_path = os.path.join(OUTPUT_DIR, fname)
    with open(out_path, 'w', encoding='utf-8') as fo:
        json.dump(data, fo, indent=2)

    print(f"[OK] {pid} → publishable={data['is_publishable']} , venue={data['venue']}")

print("All papers labeled and saved to", OUTPUT_DIR)

