import fitz  # PyMuPDF
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def extract_text_with_metadata(pdf_path, filename):
    """Extracts text from PDF and attaches page numbers as metadata."""
    doc = fitz.open(pdf_path)
    docs = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        
        if text.strip():
            metadata = {"source": filename, "page": page_num + 1}
            docs.append(Document(page_content=text, metadata=metadata))
            
    return docs

def chunk_documents(documents):
    """Splits documents into smaller chunks for the Vector DB."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len
    )
    chunks = text_splitter.split_documents(documents)
    return chunks