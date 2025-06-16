import streamlit as st
from retriever_with_full_context import retrieve
from gemini_qa import answer_query_with_gemini

# Set wide layout for three columns
st.set_page_config(page_title="Occams Advisory Q&A", layout="wide")

st.title("Occams Advisory Q&A Interface")

# Initialize session state
def init_state():
    if "hits" not in st.session_state:
        st.session_state.hits = []
    if "answer" not in st.session_state:
        st.session_state.answer = ""
    if "query" not in st.session_state:
        st.session_state.query = ""

init_state()

# Create three columns of equal width
col1, col2, col3 = st.columns(3)

# Column 1: Query Input
with col1:
    st.header("Query")
    st.session_state.query = st.text_area("Enter your question here:", value=st.session_state.query, height=200)
    if st.button("Submit Query"):
        # Retrieve and answer
        query = st.session_state.query.strip()
        if query:
            # Retrieve top-K documents
            st.session_state.hits = retrieve(query)
            # Generate final answer via Gemini
            st.session_state.answer = answer_query_with_gemini(query)

# Column 2: Retrieved Content
with col2:
    st.header("Retrieved Content")
    if st.session_state.hits:
        for i, hit in enumerate(st.session_state.hits, start=1):
            st.subheader(f"{i}. {hit['title']}")
            st.write(hit['content'])
            # Show children if available
            children = hit.get('children', [])
            if children:
                st.markdown("**Children:**")
                for child in children:
                    st.markdown(f"- **{child.get('title', '')}**: {child.get('content', '')}")
    else:
        st.write("No retrieval results yet.")

# Column 3: LLM Answer
with col3:
    st.header("Final Answer")
    if st.session_state.answer:
        st.write(st.session_state.answer)
    else:
        st.write("Awaiting submission...")
