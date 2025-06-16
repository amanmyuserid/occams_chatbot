#!/usr/bin/env python3
"""
vector_embedding.py

1. Recursively load all JSON files under cleaned/
2. Flatten title/content/children into docs
3. Chunk any doc >25k tokens
4. Save metadata.json for retrieval-time use
5. Embed + index each chunk one by one, printing progress
6. Save FAISS index to disk at the end
"""

import os
import json
from llama_cpp import Llama
import llama_cpp
import numpy as np
import faiss
import tiktoken  # pip install tiktoken

# ────────────────────────────────────────────────────────────────────────────────
# Constants
MAX_TOKENS   = 25_000
CLEANED_DIR  = "cleaned"         # root of your JSON hierarchy
META_PATH    = "metadata.json"
INDEX_PATH   = "qwen3_faiss.index"

# ─── 1. Load the quantized GGUF model with embedding support ───────────────────
llm = Llama.from_pretrained(
    repo_id="Qwen/Qwen3-Embedding-0.6B-GGUF",
    filename="Qwen3-Embedding-0.6B-Q8_0.gguf",
    n_threads=4,
    embedding=True,
    pooling_type=llama_cpp.LLAMA_POOLING_TYPE_MEAN,
    verbose=False
)

# ─── 2. Token encoder ───────────────────────────────────────────────────────────
encoder = tiktoken.get_encoding("cl100k_base")

def count_tokens(text: str) -> int:
    return len(encoder.encode(text))

def chunk_text(text: str) -> list[str]:
    """Split text into sub-texts each ≤ MAX_TOKENS tokens."""
    tokens = encoder.encode(text)
    chunks = []
    for i in range(0, len(tokens), MAX_TOKENS):
        sub = tokens[i : i + MAX_TOKENS]
        chunks.append(encoder.decode(sub))
    return chunks

# ─── 3. Load & flatten JSON trees ───────────────────────────────────────────────
def flatten_node(node: dict, out: list[dict]):
    raw_title = node.get("title")
    title = str(raw_title).strip() if raw_title is not None else ""

    raw_content = node.get("content")
    if isinstance(raw_content, list):
        content = "\n".join(str(x) for x in raw_content).strip()
    else:
        content = str(raw_content or "").strip()

    if title and content:
        out.append({"title": title, "content": content})

    for child in node.get("children") or []:
        flatten_node(child, out)

def load_all_docs(root_dir: str) -> list[dict]:
    docs = []
    for dirpath, _, files in os.walk(root_dir):
        for fn in files:
            if fn.lower().endswith(".json"):
                path = os.path.join(dirpath, fn)
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                flatten_node(data, docs)
    return docs

# ─── 4. Chunk oversized documents ───────────────────────────────────────────────
def prepare_chunks(docs: list[dict]) -> list[dict]:
    out = []
    for doc in docs:
        title, content = doc["title"], doc["content"]
        if count_tokens(content) <= MAX_TOKENS:
            out.append(doc)
        else:
            for sub in chunk_text(content):
                out.append({"title": title, "content": sub})
    return out

# ─── 5. Embed texts ─────────────────────────────────────────────────────────────
def embed_texts(texts: list[str]) -> np.ndarray:
    resp = llm.create_embedding(input=texts)
    embs = [item["embedding"] for item in resp["data"]]
    dims = {len(e) for e in embs}
    if len(dims) != 1:
        raise ValueError(f"Inconsistent embedding sizes: {dims}")
    return np.vstack(embs).astype(np.float32)

# ─── 6. Main: load, chunk, dump metadata, embed+index, save ────────────────────
if __name__ == "__main__":
    # 6.1 Load & flatten your JSON files
    raw_docs = load_all_docs(CLEANED_DIR)
    print(f"Loaded {len(raw_docs)} raw documents")

    # 6.2 Chunk any that exceed MAX_TOKENS
    docs = prepare_chunks(raw_docs)
    print(f"After chunking: {len(docs)} total docs to embed")

    # 6.3 Dump metadata.json for retrieval use
    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)
    print(f"Wrote {META_PATH} with {len(docs)} entries")

    # 6.4 Build list of (title+content) strings
    inputs = [f"{d['title']}\n\n{d['content']}" for d in docs]

    # 6.5 Embed + index one chunk at a time, printing a counter
    counter = 1
    index = None
    print("Indexing:", end=" ", flush=True)

    for chunk_txt in inputs:
        emb = embed_texts([chunk_txt])  # shape (1, D)

        if index is None:
            dim = emb.shape[1]
            index = faiss.IndexFlatL2(dim)

        index.add(emb)
        print(counter, end=" ", flush=True)
        counter += 1

    print()  # newline after counters

    # 6.6 Save the built index to disk
    faiss.write_index(index, INDEX_PATH)
    print(f"Saved FAISS index with {index.ntotal} vectors to '{INDEX_PATH}'")