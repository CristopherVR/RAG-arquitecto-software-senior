from sentence_transformers import SentenceTransformer

class Embedder:

    def __init__(self):

        print("Cargando modelo de embeddings...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        print("Modelo cargado")

    def generate_embedding(self, text):

        embedding = self.model.encode(text)

        return embedding.tolist()