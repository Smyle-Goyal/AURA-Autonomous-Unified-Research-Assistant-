import streamlit as st
import os
from src.ingestion import extract_text_with_metadata, chunk_documents
from src.vector_store import store_chunks

st.title("AURA - Research Assistant")

uploaded_file = st.file_uploader("Upload a Research Paper (PDF)", type="pdf")

if uploaded_file is not None:
    # Save file temporarily to data/
    file_path = os.path.join("data", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.info("Extracting and Chunking text...")
    raw_docs = extract_text_with_metadata(file_path, uploaded_file.name)
    chunks = chunk_documents(raw_docs)
    
    st.info(f"Storing {len(chunks)} chunks in Qdrant...")
    store_chunks(chunks)
    
    st.success("Paper ingested! Ready for questions.")