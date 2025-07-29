
import fitz 
import os

def load_documents_by_role(base_folder="data", max_pages=50):
    """
    Load documents from subfolders named after roles.
    Returns: dict with role as key and list of (filename, text) as value
    """
    role_docs = {}
    for role in os.listdir(base_folder):
        role_folder = os.path.join(base_folder, role)
        if os.path.isdir(role_folder):
            documents = []
            for filename in os.listdir(role_folder):
                if filename.endswith(".pdf"):
                    file_path = os.path.join(role_folder, filename)
                    try:
                        doc = fitz.open(file_path)
                        text = ""

                        for i, page in enumerate(doc):
                            if i >= max_pages:
                                break
                            text += page.get_text()

                        documents.append((filename, text))
                        doc.close()
                    except Exception as e:
                        print(f"Error loading {filename}: {e}")
            role_docs[role] = documents
    return role_docs

def chunk_text(text, chunk_size=1000, overlap=200, max_chunks=200):
    chunks = []
    start = 0
    text_length = len(text)
    chunk_count = 0

    while start < text_length and chunk_count < max_chunks:
        end = min(start + chunk_size, text_length)
        chunk = text[start:end]
        chunks.append(chunk)
        chunk_count += 1
        start += chunk_size - overlap  

    return chunks
