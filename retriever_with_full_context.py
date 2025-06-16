#!/usr/bin/env python3
"""
retrieval.py

Load the FAISS index and metadata.json, embed a query, and retrieve top-k results with scores and their full children subtrees.
"""
import os
import json
import numpy as np
import faiss
from llama_cpp import Llama
import llama_cpp
import tiktoken

# ───────────────────────────────────────────────────────────────────────────────
# Configurations
CLEANED_DIR = "cleaned"             # folder of your original JSON files
META_PATH   = "metadata.json"        # chunk metadata file
INDEX_PATH  = "qwen3_faiss.index"   # FAISS index file
TOP_K       = 5                       # number of results to retrieve

# ─── 1. Load metadata.json ─────────────────────────────────────────────────────
with open(META_PATH, "r", encoding="utf-8") as f:
    docs = json.load(f)
print(f"Loaded {len(docs)} document chunks from {META_PATH}")

# ─── 2. Load FAISS index ─────────────────────────────────────────────────────────
index = faiss.read_index(INDEX_PATH)
print(f"Loaded FAISS index with {index.ntotal} vectors from {INDEX_PATH}")

# ─── 3. Build title -> node mapping ─────────────────────────────────────────────
def build_title_map(root_dir: str) -> dict:
    mapping = {}
    for dirpath, _, files in os.walk(root_dir):
        for fn in files:
            if fn.lower().endswith(".json"):
                path = os.path.join(dirpath, fn)
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                def traverse(node: dict):
                    title = str(node.get("title") or "").strip()
                    if title:
                        mapping[title] = node
                    for child in node.get("children") or []:
                        traverse(child)
                traverse(data)
    return mapping

# Build mapping once at startup
title_map = build_title_map(CLEANED_DIR)

# ─── 4. Initialize tokenizer & model ───────────────────────────────────────────
encoder = tiktoken.get_encoding("cl100k_base")
llm = Llama.from_pretrained(
    repo_id="Qwen/Qwen3-Embedding-0.6B-GGUF",
    filename="Qwen3-Embedding-0.6B-Q8_0.gguf",
    n_threads=4,
    embedding=True,
    pooling_type=llama_cpp.LLAMA_POOLING_TYPE_MEAN,
    verbose=False
)

# ─── 5. Embed query function ─────────────────────────────────────────────────────
def embed_query(query: str) -> np.ndarray:
    resp = llm.create_embedding(input=[query.strip()])
    emb = np.array(resp["data"][0]["embedding"], dtype=np.float32)
    return emb.reshape(1, -1)

# ─── 6. Retrieve function ─────────────────────────────────────────────────────────
def retrieve(query: str, top_k: int = TOP_K) -> list:
    q_emb = embed_query(query)
    distances, indices = index.search(q_emb, top_k)
    results = []
    for dist, idx in zip(distances[0], indices[0]):
        meta    = docs[idx]
        title   = meta["title"]
        content = meta["content"]
        # Fetch the full children subtree from the original JSON
        node     = title_map.get(title, {})
        children = node.get("children", [])
        results.append({
            "score":    float(dist),
            "title":    title,
            "content":  content,
            "children": children
        })
    return results

# ─── 7. CLI interface ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    while True:
        query = input("Enter your query (or 'exit'): ")
        if not query or query.lower() in ('exit', 'quit'):
            break
        hits = retrieve(query)
        print("\nTop results with children:")
        for i, hit in enumerate(hits, 1):
            print(f"{i}. [Score: {hit['score']:.4f}] {hit['title']}\n{hit['content']}\nChildren subtree:")
            print(json.dumps(hit['children'], indent=2))
            print()
