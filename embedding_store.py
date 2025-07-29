import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
import os
import pickle
from document_loader import chunk_text

# class EmbeddingStore:
#     def __init__(self, model_name="all-MiniLM-L6-v2", index_path="vectorstore/faiss_index.bin"):
#         self.model = SentenceTransformer(model_name)
#         self.index_path = index_path
#         self.index = None
#         self.doc_map = []
    

#     def build_index(self, documents):
#         vectors = []
#         self.doc_map = []
#         for doc_name, text in documents:
#             chunks = chunk_text(text)
#             chunk_vectors = self.model.encode(chunks, batch_size=8, show_progress_bar=True)
#             vectors.extend(chunk_vectors)
#             self.doc_map.extend([(doc_name, chunk) for chunk in chunks])
#         vectors_np = np.array(vectors).astype("float32")
#         self.index = faiss.IndexFlatL2(vectors_np.shape[1])
#         self.index.add(vectors_np)
#         self.save_index()

#     def save_index(self):
#         if not os.path.exists("vectorstore"):
#             os.makedirs("vectorstore")
#         faiss.write_index(self.index, self.index_path)
#         with open(self.index_path + ".map", "wb") as f:
#             pickle.dump(self.doc_map, f)

#     def load_index(self):
#         self.index = faiss.read_index(self.index_path)
#         with open(self.index_path + ".map", "rb") as f:
#             self.doc_map = pickle.load(f)

#     def query(self, user_query, k=3):
#         vector = self.model.encode([user_query]).astype("float32")
#         D, I = self.index.search(vector, k)
#         results = [self.doc_map[i] for i in I[0]]
#         return results

class EmbeddingStore:
    def __init__(self, model_name="all-MiniLM-L6-v2", index_path="vectorstore/faiss_index.bin"):
        self.model = SentenceTransformer(model_name)
        self.index_path = index_path
        self.index = None
        self.doc_map = []  # will store tuples: (role, filename, chunk_text)
    
    def build_index(self, documents_by_role):
        vectors = []
        self.doc_map = []
        for role, documents in documents_by_role.items():
            for doc_name, text in documents:
                chunks = chunk_text(text)
                for chunk in chunks:
                    vectors.append(self.model.encode(chunk))
                # Save role, filename, chunk
                    self.doc_map.append((role, doc_name, chunk))
        vectors_np = np.array(vectors).astype("float32")
        self.index = faiss.IndexFlatL2(vectors_np.shape[1])
        self.index.add(vectors_np)
        self.save_index()


    # def build_index(self, role_docs_dict):
    #     vectors = []
    #     self.doc_map = []
    #     for role, documents in role_docs_dict.items():
    #         for doc_name, text in documents:
    #             chunks = chunk_text(text)
    #             for chunk in chunks:
    #                 vectors.append(self.model.encode(chunk))
    #                 self.doc_map.append((role, doc_name, chunk))
    #     vectors_np = np.array(vectors).astype("float32")
    #     self.index = faiss.IndexFlatL2(vectors_np.shape[1])
    #     self.index.add(vectors_np)
    #     self.save_index()
    
    def save_index(self):
        if not os.path.exists("vectorstore"):
            os.makedirs("vectorstore")
        faiss.write_index(self.index, self.index_path)
        with open(self.index_path + ".map", "wb") as f:
            pickle.dump(self.doc_map, f)

    def load_index(self):
        self.index = faiss.read_index(self.index_path)
        with open(self.index_path + ".map", "rb") as f:
            self.doc_map = pickle.load(f)

    # def query(self, user_query, user_role=None, k=3):
    #     vector = self.model.encode([user_query]).astype("float32")
    #     D, I = self.index.search(vector, k*5)  # search more to filter by role

    #     results = []
    #     for i in I[0]:
    #         role, doc_name, chunk = self.doc_map[i]
    #         if user_role is None or role == user_role:
    #             results.append((doc_name, chunk))
    #             if len(results) >= k:
    #                 break
    #     return results

    def query(self, user_query, user_role=None, k=3):
    # Role access control
        role_access = {
            "Manager": ["manager", "employee"],
            "Employee": ["employee"],
        }
        allowed_roles = role_access.get(user_role, [])

        vector = self.model.encode([user_query]).astype("float32")
    # Search more results than needed, to filter later
        D, I = self.index.search(vector, k * 5)

        results = []
        for i in I[0]:
        # doc_map must store role, filename, chunk text
            role, doc_name, chunk = self.doc_map[i]
            if role in allowed_roles:
                results.append((doc_name, chunk))
                if len(results) >= k:
                    break
        return results

