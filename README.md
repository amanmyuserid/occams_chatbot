# Occams Advisory Chatbot

A conversational Q\&A system that exclusively uses content from the Occams Advisory website.  It uses a vector database (FAISS) for retrieval and Google Gemini for final answer generation, presented via a simple Streamlit UI.

---

## 📁 Repository Structure

```
├── .gitignore
├── clean_md_file.py           # Cleans raw HTML/Markdown content (removes nav, footers, duplicates)
├── crawler_and_extractor.py   # Crawls Occams Advisory site and extracts structured page content
├── vector_embedding.py        # Generates vector embeddings (FAISS index + metadata.json)
├── metadata.json              # Chunk metadata for vector embeddings (title + content)
├── retriever_with_full_context.py  # Retrieves top-K chunks and their full children context
├── gemini_qa.py               # Builds prompt from retrievals and calls Google Gemini for final answer
├── streamlit_ui.py            # Streamlit app: three-column UI (Query | Retrieved Content | Final Answer)
├── requirements.txt           # Python dependencies
```

---

## 🚀 Quickstart

1. **Clone the repo**

   ```bash
   git clone https://github.com/yourusername/occams-chatbot.git
   cd occams-chatbot
   ```

2. **Install dependencies**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure environment**

   * Create a `.env` in the project root:

     ```ini
     GOOGLE_API_KEY=your_google_api_key_here
     ```

4. **Generate embeddings**

   ```bash
   python vector_embedding.py
   ```

   * This will:

     * Crawl raw JSON in `cleaned/`
     * Flatten & chunk content into `metadata.json`
     * Build and save `qwen3_faiss.index`

5. **Run the Streamlit UI**

   ```bash
   streamlit run streamlit_ui.py --server.port 8501
   ```

   * Open [http://localhost:8501](http://localhost:8501) to interact.

---

## 🗂 Script Details

### `clean_md_file.py`

* Cleans repetitive or template HTML/Markdown segments.
* Prepares raw page dumps for structured extraction.

### `crawler_and_extractor.py`

* Recursively crawls all pages under Occams Advisory.
* Extracts headings, paragraphs, and nesting into JSON files under `cleaned/`.

### `vector_embedding.py`

* Loads a quantized Qwen3 embedding model via llama.cpp.
* Flattens and token-chunks all `{title, content}` pairs.
* Saves `metadata.json` and builds a FAISS L2 index (`qwen3_faiss.index`).

### `retriever_with_full_context.py`

* Loads `metadata.json` & FAISS index.
* Embeds a query and retrieves top-K chunks with scores.
* Looks up each chunk’s original JSON node and returns its full `children` subtree.

### `gemini_qa.py`

* Imports the retrieval function.
* Formats retrieved chunks into a structured prompt.
* Calls the `gemini-2.5-flash-preview-05-20` model via Google GenAI SDK.
* Returns a concise final answer.

### `streamlit_ui.py`

* Self-contained Streamlit application.
* Three-column layout:

  1. **Query** input
  2. **Retrieved Content** with titles, snippets, and children
  3. **Final Answer** from Gemini

---


## 📜 License

MIT © Your Name
