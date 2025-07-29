from transformers import pipeline
from embedding_store import EmbeddingStore

# rag_model = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.1", device=0)
# ✅ Free, open-access model that works on CPU
rag_model = pipeline("text2text-generation", model="google/flan-t5-base")

embedding_store = EmbeddingStore()
embedding_store.load_index()

# def answer_query(user_query):
#     top_docs = embedding_store.query(user_query)
#     context = "\n\n".join([f"From {doc[0]}:\n{doc[1]}" for doc in top_docs])
    
#     prompt = f"Use the context below to answer the question. Cite filenames where necessary.\n\nContext:\n{context}\n\nQuestion: {user_query}\n\nAnswer:"
    
#     response = rag_model(prompt, max_new_tokens=200, do_sample=True)[0]['generated_text']
#     return response

def answer_query(user_query, user_role=None):
    top_docs = embedding_store.query(user_query, user_role=user_role, k=3)
    if not top_docs:
        return f"No accessible documents found for role '{user_role}'."
    context = "\n\n".join([f"From {doc[0]}:\n{doc[1]}" for doc in top_docs])

    prompt = f"Use the context below to answer the question. Cite filenames where necessary.\n\nContext:\n{context}\n\nQuestion: {user_query}\n\nAnswer:"

    response = rag_model(prompt, max_new_tokens=200, do_sample=True)[0]['generated_text']
    return response
