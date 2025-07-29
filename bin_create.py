# from document_loader import load_documents_from_folder
# from embedding_store import EmbeddingStore

# docs = load_documents_from_folder("data")  # assuming your PDFs are in `data/`
# store = EmbeddingStore()
# store.build_index(docs)

from document_loader import load_documents_by_role
from embedding_store import EmbeddingStore

# Load documents organized by roles (folders inside data/)
role_docs = load_documents_by_role("data")

store = EmbeddingStore()
store.build_index(role_docs)  # Now expects dict: role -> list of (filename, text)
