import streamlit as st
from retriever_with_full_context import retrieve
from gemini_qa import answer_query_with_gemini

st.set_page_config(page_title="Occams Advisory Q&A", layout="wide")
st.title("Occams Advisory Q&A Interface")

# ─── Session State Init ──────────────────────────────────────────────────────────
for key in ("hits", "answer", "query"):
    if key not in st.session_state:
        st.session_state[key] = [] if key == "hits" else ""

# ─── Three-Column Layout ─────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)

with col1:
    st.header("Query")
    st.session_state.query = st.text_area(
        "Enter your question here:", 
        value=st.session_state.query, 
        height=200
    )
    if st.button("Submit Query"):
        query = st.session_state.query.strip()
        st.session_state.hits = []
        st.session_state.answer = ""

        if not query:
            st.warning("Please enter a query before submitting.")
        else:
            # 1) Retrieve step
            with st.spinner("Retrieving documents…"):
                try:
                    st.session_state.hits = retrieve(query)
                except Exception as e:
                    st.error(f"Retrieval error: {e}")
                    st.session_state.hits = []

            # 2) LLM answer step
            if st.session_state.hits:
                with st.spinner("Generating final answer…"):
                    try:
                        st.session_state.answer = answer_query_with_gemini(query)
                    except Exception as e:
                        st.error(f"LLM error: {e}")
                        st.session_state.answer = ""
            else:
                st.info("No documents retrieved; skipping LLM step.")

with col2:
    st.header("Retrieved Content")
    if st.session_state.hits:
        for i, hit in enumerate(st.session_state.hits, start=1):
            st.subheader(f"{i}. {hit['title']}")
            st.write(hit["content"])
            if hit.get("children"):
                st.markdown("**Children:**")
                for child in hit["children"]:
                    st.markdown(f"- **{child.get('title','')}**: {child.get('content','')}")
    else:
        st.write("No retrieval results yet.")

with col3:
    st.header("Final Answer")
    if st.session_state.answer:
        st.write(st.session_state.answer)
    else:
        st.write("Awaiting submission…")