# 🧠 Role-Based AI Query Assistant (RAG System)

This project implements a **Role-Aware Retrieval-Augmented Generation (RAG)** system with:

- PDF document ingestion & embedding
- Vector search using FAISS
- HuggingFace `flan-t5-base` model for answering queries
- Role-based access filtering (Manager vs Employee)
- Flask REST API backend
- Streamlit frontend with feedback collection and viewer
- SQLite feedback database

---

## 🚀 Features

- Load and embed PDFs by role (`manager`, `employee`)
- Retrieve top-k relevant chunks per user query with role-based filtering
- Generate natural language answers citing document sources
- Collect and view user feedback (role-based)
- Simple, clean UI with Streamlit
- Modular, extensible architecture

---

## 📁 Project Structure

```plaintext
.
├── app.py                  # Flask API backend
├── create_bin.py           # Build and save FAISS index and embeddings
├── document_loader.py      # PDF loading and chunking utility
├── embedding_store.py      # FAISS index & embedding model handling
├── rag_engine.py           # Query answering pipeline using embeddings + LLM
├── front_end.py            # Streamlit UI with feedback system
├── feedback.db             # SQLite DB for feedback (auto-created)
├── vectorstore/            # FAISS index and doc map files
└── data/
    ├── manager/            # Manager PDFs
    └── employee/           # Employee PDFs

---

## 🧩 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/jagrutijain109/AIQuerySystem.git

### 2. Install Dependencies

It is recommended to use a virtual environment to keep dependencies isolated.

```bash
pip install -r requirements.txt
