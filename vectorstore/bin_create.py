from document_loader import load_documents_from_folder
from embedding_store import EmbeddingStore

docs = load_documents_from_folder("data")  # assuming your PDFs are in `data/`
store = EmbeddingStore()
store.build_index(docs)
