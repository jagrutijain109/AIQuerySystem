from transformers import pipeline
from embedding_store import EmbeddingStore

rag_model = pipeline("text2text-generation", model="google/flan-t5-base")

embedding_store = EmbeddingStore()
embedding_store.load_index()


def answer_query(user_query, user_role=None):
    top_docs = embedding_store.query(user_query, user_role=user_role)
    context = "\n\n".join([f"From {doc[0]}:\n{doc[1]}" for doc in top_docs])
    
    prompt = f"Use the context below to answer the question. Cite filenames where necessary.\n\nContext:\n{context}\n\nQuestion: {user_query}\n\nAnswer:"
    
    response = rag_model(prompt, max_new_tokens=200, do_sample=True)[0]['generated_text']
    return response

