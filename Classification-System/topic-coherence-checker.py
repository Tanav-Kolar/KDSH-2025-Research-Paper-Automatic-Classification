import json
import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load a strong semantic model
model = SentenceTransformer('all-MiniLM-L6-v2')  # Fast + decent performance

REQUIRED_SECTIONS = ['title', 'abstract', 'introduction', 'methodology', 'results', 'conclusion']
SECTIONS_TO_COMPARE = [
    ('abstract', 'introduction'),
    ('introduction', 'methodology'),
    ('methodology', 'results'),
    ('results', 'conclusion')
]

def get_section_embeddings(paper_json):
    embeddings = {}
    for sec in REQUIRED_SECTIONS:
        text = paper_json.get(sec, "").strip()
        embeddings[sec] = model.encode(text) if text else np.zeros((384,))
    return embeddings

def compute_semantic_coherence(embeddings):
    scores = []
    for sec1, sec2 in SECTIONS_TO_COMPARE:
        vec1 = embeddings.get(sec1)
        vec2 = embeddings.get(sec2)
        if vec1 is not None and vec2 is not None:
            sim = cosine_similarity([vec1], [vec2])[0][0]
            scores.append(sim)
    return np.mean(scores) if scores else 0.0

def main():
    base_dir = 'Segmented_Reference'
    results = []

    for category in ['Publishable', 'Non-Publishable']:
        cat_path = os.path.join(base_dir, category)
        for root, _, files in os.walk(cat_path):
            for file in files:
                if file.endswith('.json'):
                    path = os.path.join(root, file)
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            paper = json.load(f)
                        section_embeddings = get_section_embeddings(paper)
                        score = compute_semantic_coherence(section_embeddings)
                        results.append({
                            'category': category,
                            'paper': os.path.relpath(path, base_dir),
                            'coherence_score': round(score, 4)
                        })
                    except Exception as e:
                        print(f"Error processing {path}: {e}")

    for res in results:
        print(f"{res['category']:16} | {res['paper']:60} | Score: {res['coherence_score']}")

if __name__ == '__main__':
    main()
