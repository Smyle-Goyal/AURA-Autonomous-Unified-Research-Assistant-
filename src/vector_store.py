from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
DB_DIR = "./local_qdrant"
COLLECTION_NAME = "aura_papers"

def store_chunks(chunks):
    """Stores document chunks into local persistent Qdrant."""
    qdrant = QdrantVectorStore.from_documents(
        documents=chunks, 
        embedding=embedding_model, 
        path=DB_DIR,
        collection_name=COLLECTION_NAME,
    )
    return qdrant

def get_retriever():
    """Returns the retriever to fetch relevant chunks based on queries."""
    qdrant = QdrantVectorStore.from_existing_collection(
        embedding=embedding_model,
        path=DB_DIR,
        collection_name=COLLECTION_NAME,
    )
    return qdrant.as_retriever(search_kwargs={"k": 4})