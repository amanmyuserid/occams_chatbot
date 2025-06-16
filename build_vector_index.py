# Step-by-step modular pipeline to generate embeddings and store in FAISS

import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# ========================
# CONFIGURATION
# ========================
INPUT_DIR = "site_data"
OUTPUT_DIR = "vector_index"
MODEL_NAME = "BAAI/bge-small-en-v1.5"
VECTOR_DIM = 384  # This is known for BGE-small
INDEX_FILE = os.path.join(OUTPUT_DIR, "faiss_index.bin")
META_FILE = os.path.join(OUTPUT_DIR, "metadata.json")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ========================
# Load Embedding Model
# ========================
print("[+] Loading model...")
model = SentenceTransformer(MODEL_NAME)

# ========================
# Load and Prepare Data
# ========================
print("[+] Reading chunks...")
all_texts = []
all_metadata = []

for file in os.listdir(INPUT_DIR):
    if not file.endswith(".json"):
        continue

    filepath = os.path.join(INPUT_DIR, file)
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    for chunk in data.get("flat_chunks", []):
        text = chunk.get("chunk_text", "").strip()
        if not text:
            continue

        all_texts.append(text)
        all_metadata.append({
            "url": data.get("url"),
            "section": data.get("section"),
            "subsection": data.get("subsection"),
            "source": data.get("source"),
            "heading_path": chunk.get("heading_path", [])
        })

print(f"[✓] Total chunks to embed: {len(all_texts)}")

# ========================
# Generate Embeddings
# ========================
print("[+] Generating embeddings...")
embeddings = model.encode(all_texts, normalize_embeddings=True)
embeddings_np = np.array(embeddings).astype("float32")

# ========================
# Store in FAISS Index
# ========================
print("[+] Creating FAISS index...")
index = faiss.IndexFlatL2(VECTOR_DIM)
index.add(embeddings_np)
faiss.write_index(index, INDEX_FILE)
print(f"[✓] FAISS index saved to {INDEX_FILE}")

# ========================
# Save Metadata
# ========================
with open(META_FILE, "w", encoding="utf-8") as f:
    json.dump(all_metadata, f, indent=2, ensure_ascii=False)
print(f"[✓] Metadata saved to {META_FILE}")