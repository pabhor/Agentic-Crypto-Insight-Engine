import os
import chromadb
from sentence_transformers import SentenceTransformer

class EmbedAgent:
    def __init__(self):
        chroma_dir = os.path.join("storage", "chroma")

        # ✅ For local persistence
        self.client = chromadb.PersistentClient(path=chroma_dir)

        # Create or load collection
        self.collection = self.client.get_or_create_collection("crypto_embeddings")

        # Load embedding model
        self.model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

    def add_texts(self, texts, ids=None):
        embeddings = self.model.encode(texts).tolist()
        self.collection.add(documents=texts, embeddings=embeddings, ids=ids or [str(i) for i in range(len(texts))])

    def query(self, query_text, top_k=5):
        query_emb = self.model.encode([query_text]).tolist()
        results = self.collection.query(query_embeddings=query_emb, n_results=top_k)
        return results
