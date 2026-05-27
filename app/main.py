from app.loaders.git_loader import GitLoader
from app.loaders.file_scanner import FileScanner
from app.chunkers.code_chunker import CodeChunker
from app.embeddings.embedder import Embedder
from app.vectorstore.chroma_client import ChromaManager
from app.config import REPO_URL, LOCAL_REPO
import uuid

def main():

    GitLoader.clone_repository(REPO_URL, LOCAL_REPO)

    files = FileScanner.scan_repository(LOCAL_REPO)
    print(f"Archivos encontrados: {len(files)}")

    embedder = Embedder()
    chroma = ChromaManager()

    for file in files:
        chunks = FileScanner.parse_file(file)          # ← usa el nuevo FileScanner
        chunks = CodeChunker.chunk_documents(chunks)   # ← chunking semántico

        for chunk in chunks:
            embedding = embedder.generate_embedding(chunk.content)

            chroma.collection.add(
                ids=[str(uuid.uuid4())],
                documents=[chunk.content],
                embeddings=[embedding],
                metadatas=[chunk.metadata]
            )

        print(f"Indexado: {file}")

    print("Ingesta completa.")

if __name__ == "__main__":
    main()