import uuid

from app.loaders.csv_loader import CSVLoader
from app.loaders.git_loader import GitLoader
from app.loaders.file_scanner import FileScanner
from app.chunkers.code_chunker import CodeChunker
from app.embeddings.embedder import Embedder
from app.vectorstore.chroma_client import ChromaManager
from app.config import REPO_URL, LOCAL_REPO
from app.models.document import DocumentChunk

from app.loaders.drawio_loader import DrawioLoader
from app.loaders.excel_loader import ExcelLoader


def ingest_repository(repo_url=None, local_repo=None):

    repo_url = repo_url or REPO_URL
    local_repo = local_repo or LOCAL_REPO

    print("\n🚀 INICIANDO INGESTA RAG\n")

    # Por ahora lo dejamos apagado para que no clone otra vez
    GitLoader.clone_repository(repo_url, local_repo)

    files = FileScanner.scan_repository(local_repo)

    print(f"📂 Archivos encontrados: {len(files)}")

    embedder = Embedder()
    chroma = ChromaManager()

    documents = []
    metadatas = []
    ids = []
    embeddings = []

    for i, file_path in enumerate(files, start=1):

        print(f"\n📂 Procesando archivo {i}/{len(files)}: {file_path}")

        extension = file_path.lower()

        try:
            if extension.endswith((".drawio", ".xml")):
                chunks = DrawioLoader.load_drawio(file_path)

            elif extension.endswith(".xlsx"):
                chunks = ExcelLoader.load_excel(file_path)

            elif extension.endswith(".csv"):
                chunks = CSVLoader.load_csv(file_path)

            else:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                document = DocumentChunk(
                    content=content,
                    metadata={
                        "source": file_path,
                        "file": file_path,
                        "type": "code"
                    }
                )

                chunks = CodeChunker.chunk_document(document)

        except Exception as e:
            print(f"❌ No se pudo procesar el archivo: {file_path}")
            print(e)
            continue

        print(f"✂ Chunks encontrados: {len(chunks)}")

        for chunk in chunks:

            text = chunk.content

            if not text.strip():
                continue

            print("🧠 Generando embedding...")

            embedding = embedder.generate_embedding(text)

            print("✅ Embedding generado")

            documents.append(text)
            embeddings.append(embedding)
            metadatas.append(chunk.metadata)
            ids.append(str(uuid.uuid4()))

    print(f"\n🧠 Indexando {len(documents)} chunks...")

    if documents:
        chroma.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

        print("✅ INGESTA COMPLETA")
    else:
        print("❌ No se generaron documentos para indexar")


if __name__ == "__main__":
    ingest_repository()