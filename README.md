# AURA — Autonomous Understanding & Research Assistant

> Upload a research paper. Ask questions. Get cited answers.

AURA is a local RAG (Retrieval Augmented Generation) chatbot that lets you upload any research paper (PDF) and ask questions about it. It answers strictly from the paper's content and always cites the exact page number.

---

## 🚀 Features

- 📄 Upload any research paper in PDF format
- 🔍 Semantic search across the entire document
- 🤖 AI-generated answers using OpenRouter LLM
- 📌 Every answer cited with source filename and page number
- 💾 Persistent local vector storage with Qdrant
- ⚡ Runs entirely on your machine (no cloud DB needed)

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| PDF Extraction | PyMuPDF (fitz) |
| Text Chunking | LangChain RecursiveCharacterTextSplitter |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` (local, free) |
| Vector Database | Qdrant (local persistent storage) |
| LLM | OpenRouter API (free tier) |

---

## 📁 Project Structure

```
AURA/
│
├── data/                   # Temporarily stores uploaded PDFs
├── local_qdrant/           # Qdrant local persistent vector storage
│
├── src/
│   ├── __init__.py
│   ├── ingestion.py        # PyMuPDF extraction & chunking
│   ├── vector_store.py     # Qdrant embedding & retrieval
│   └── llm_chain.py        # OpenRouter LLM integration
│
├── app.py                  # Streamlit UI
├── requirements.txt
├── .env                    # API keys (never commit this!)
└── .gitignore
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/aura.git
cd aura
```

### 2. Create and activate a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your OpenRouter API key
Create a `.env` file in the root directory:
```
OPENROUTER_API_KEY=sk-or-your-key-here
```
Get a free API key at [openrouter.ai](https://openrouter.ai)

---

## ▶️ Running the App

```bash
streamlit run app.py
```

Then open your browser at `http://localhost:8501`

---

## 💡 How It Works

```
PDF Upload → Extract Text (PyMuPDF) → Chunk Text → Embed Chunks → Store in Qdrant
                                                                         ↓
  Cited Answer ← LLM generates ← Top 4 relevant chunks ← Search with question
```

1. **Ingest** — PDF is read page by page, each chunk tagged with `{source, page}` metadata
2. **Embed** — Chunks converted to vectors using a local HuggingFace model
3. **Store** — Vectors saved persistently to local Qdrant database
4. **Retrieve** — User question embedded and matched against stored vectors
5. **Generate** — Top chunks sent to LLM which answers with page citations

---

## 📌 Example

**Question:** What attention mechanism is used in the Transformer?

**Answer:** The Transformer uses a multi-head self-attention mechanism that allows the model to jointly attend to information from different representation subspaces. *(Source: attention_is_all_you_need.pdf, Page 4)*

---

## 🔜 Roadmap

- [ ] Phase 2 — Multi-paper upload and cross-paper querying
- [ ] Phase 3 — Chat history and conversation memory
- [ ] Phase 4 — Paper summarization in one click
- [ ] Phase 5 — Web-based paper search and auto-ingestion

---

## 📄 License

MIT License — feel free to use and build on this project.
