import streamlit as st
import os
from src.ingestion import extract_text_with_metadata, chunk_documents
from src.vector_store import store_chunks, get_retriever
from src.llm_chain import generate_answer

st.title("AURA- Autonomous Unified Research Assistant ")

uploaded_file = st.file_uploader("Upload a Research Paper (PDF)", type="pdf")

if uploaded_file is not None:
    file_path = os.path.join("data", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.info("Extracting and Chunking text...")
    raw_docs = extract_text_with_metadata(file_path, uploaded_file.name)
    chunks = chunk_documents(raw_docs)
    
    st.info(f"Storing {len(chunks)} chunks in Qdrant...")
    store_chunks(chunks)
    
    st.success("Paper ingested! Ready for questions.")

# Question input always visible
question = st.text_input("Ask a question about your uploaded paper:")

if question:
    with st.spinner("Thinking..."):
        retriever = get_retriever()
        retrieved_chunks = retriever.invoke(question)
        answer = generate_answer(question, retrieved_chunks)
    
    st.markdown("### Answer")
    st.write(answer)