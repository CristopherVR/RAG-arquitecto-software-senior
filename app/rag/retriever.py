from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(
    path="./chroma_db"
)


def get_collection():
    return client.get_or_create_collection(
        name="architecture_knowledge"
    )


def search_documents(question):

    collection = get_collection()

    embedding = model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=5,
        include=["documents", "metadatas", "distances"]
    )

    print("\n🔎 PREGUNTA:", question)
    print("📄 DOCUMENTOS:", results.get("documents"))
    print("📌 METADATAS:", results.get("metadatas"))
    print("📏 DISTANCIAS:", results.get("distances"))

    return results