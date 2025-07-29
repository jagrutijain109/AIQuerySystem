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

### 2. Install Dependencies

It is recommended to use a virtual environment to keep dependencies isolated.

```bash
pip install -r requirements.txt

3. Prepare Your Documents
Place your PDF documents inside the data folder organized by role. For example:

plaintext
Copy
Edit
data/
├── employee/
│   └── example_employee_doc.pdf
└── manager/
    └── confidential_policy.pdf

4. Build FAISS Index
Run the following script to load, embed, and index your documents:

python create_bin.py
This will generate the FAISS index files inside the vectorstore/ directory.

5. Start Backend Flask API
Launch the Flask API server with:
python app.py
By default, the API will run on http://localhost:5000.

6. Start Frontend Streamlit App (In a New Terminal)
Run the frontend app with:

bash
Copy
Edit
streamlit run front_end.py
This will open a web UI in your browser where you can:

Select your role (Manager or Employee)

Ask questions in natural language

View AI-generated answers with source citations

Provide feedback on the responses

If you are a Manager, view all submitted feedback

🧠 Usage
API Endpoint: /ask
Send a POST request with JSON body:
{
  "query": "What is the leave policy?",
  "role": "Employee"
}
Example response:
{
  "response": "According to employee_handbook.pdf, the leave policy states..."
}
🛠️ How Role Filtering Works
Employee role: Access restricted to documents inside the employee folder.

Manager role: Access to documents in both manager and employee folders.

This ensures users see only content relevant to their permissions.

📝 Feedback System
All user feedback is stored in a local SQLite database feedback.db.

Users submit feedback about the helpfulness of AI responses.

Managers can review all feedback through the Streamlit frontend.


