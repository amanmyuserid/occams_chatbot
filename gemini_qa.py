import os
from dotenv import load_dotenv
from google import genai
from typing import List, Dict

from retriever_with_full_context import retrieve  # assumes retrieval.py in same directory

# ───────────────────────────────────────────────────────────────────────────────
# Setup Gemini client
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables.")
client = genai.Client(api_key=api_key)

# ───────────────────────────────────────────────────────────────────────────────
# Prompt template for final answer
PROMPT_TEMPLATE = """
You are a knowledgeable assistant. Use ONLY the following retrieved information to answer the user query below.

User Query:
""" + "{query}" + """

Retrieved Context:
{context}

Based on the context, provide a clear, concise answer to the query. Do not introduce information not contained in the provided context.
"""

# ───────────────────────────────────────────────────────────────────────────────
def format_context(hits: List[Dict]) -> str:
    """Turn retrieval hits into a text block suitable for the LLM."""
    parts = []
    for i, hit in enumerate(hits, start=1):
        part = [
            f"Document {i}: {hit['title']}",
            f"Content: {hit['content']}"
        ]
        # include children if any
        if hit.get('children'):
            child_lines = []
            for child in hit['children']:
                child_lines.append(f"  - {child.get('title')}: {child.get('content')}")
            part.append("Children:")
            part.extend(child_lines)
        parts.append("\n".join(part))
    return "\n\n".join(parts)

# ───────────────────────────────────────────────────────────────────────────────
def answer_query_with_gemini(query: str) -> str:
    """
    Retrieve top-K documents, build prompt, and call Gemini for final answer.
    """
    # 1. Retrieve top-K hits with score, title, content, children
    hits = retrieve(query)

    # 2. Format the retrieved context
    context = format_context(hits)

    # 3. Build full prompt
    prompt = PROMPT_TEMPLATE.format(query=query, context=context)

    # 4. Call Gemini model
    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-05-20",
        contents=[prompt]
    )

    return response.text

# ───────────────────────────────────────────────────────────────────────────────
# Example usage (to be called from FastAPI endpoint)
if __name__ == '__main__':
    user_query = input("Enter your query: ")
    answer = answer_query_with_gemini(user_query)
    print("\nFinal Answer:\n", answer)