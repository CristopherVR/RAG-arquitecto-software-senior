from app.embeddings.embedder import Embedder
from app.vectorstore.chroma_client import ChromaManager

class SemanticSearch:

    def __init__(self):

        self.embedder = Embedder()

        self.chroma = ChromaManager()

    def search(self, query, top_k=5):

        query_embedding = self.embedder.generate_embedding(
            query
        )

        results = self.chroma.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        return results