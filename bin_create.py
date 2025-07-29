from document_loader import load_documents_by_role
from embedding_store import EmbeddingStore

role_docs = load_documents_by_role("data")

store = EmbeddingStore()
store.build_index(role_docs)  
