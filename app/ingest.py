import uuid
import argparse

from app.loaders.git_loader import GitLoader
from app.loaders.file_scanner import FileScanner
from app.chunkers.code_chunker import CodeChunker
from app.embeddings.embedder import Embedder
from app.vectorstore.chroma_client import ChromaManager
from app.config import REPO_URL, LOCAL_REPO


def ingest_repository(repo_url=None, local_repo=None):
    """
    Pipeline completo de ingesta:
    1. Clonar repositorio Git
    2. Escanear archivos soportados
    3. Parsear cada archivo con el parser correcto
    4. Dividir en chunks semánticos
    5. Generar embeddings
    6. Indexar en ChromaDB
    """

    repo_url   = repo_url   or REPO_URL
    local_repo = local_repo or LOCAL_REPO

    print("\n" + "="*50)
    print("  SISTEMA RAG — INGESTA DE CONOCIMIENTO")
    print("="*50)

    # 1. CLONAR
    print(f"\n[1/5] Clonando repositorio...")
    print(f"      URL   : {repo_url}")
    print(f"      Destino: {local_repo}")
    GitLoader.clone_repository(repo_url, local_repo)

    # 2. ESCANEAR
    print(f"\n[2/5] Escaneando archivos...")
    files = FileScanner.scan_repository(local_repo)
    print(f"      Archivos encontrados: {len(files)}")

    if not files:
        print("      No se encontraron archivos soportados. Verifica la ruta.")
        return

    # 3. PARSEAR Y CHUNKEAR
    print(f"\n[3/5] Parseando y dividiendo en chunks...")
    all_chunks = []

    for file in files:
        chunks = FileScanner.parse_file(file)
        chunks = CodeChunker.chunk_documents(chunks)
        all_chunks.extend(chunks)

    print(f"      Total de chunks generados: {len(all_chunks)}")

    # 4. EMBEDDINGS + INDEXADO
    print(f"\n[4/5] Generando embeddings e indexando en ChromaDB...")
    embedder = Embedder()
    chroma   = ChromaManager()

    indexed  = 0
    errors   = 0

    for chunk in all_chunks:
        try:
            embedding = embedder.generate_embedding(chunk.content)

            chroma.collection.add(
                ids=[str(uuid.uuid4())],
                documents=[chunk.content],
                embeddings=[embedding],
                metadatas=[chunk.metadata]
            )

            indexed += 1

        except Exception as e:
            errors += 1
            print(f"      Error indexando chunk de {chunk.metadata.get('file_name', '?')}: {e}")

    # 5. RESUMEN
    print(f"\n[5/5] Ingesta completada")
    print(f"      Chunks indexados : {indexed}")
    print(f"      Errores          : {errors}")
    print(f"      Coleccion ChromaDB: {chroma.collection.name}")
    print("="*50 + "\n")


def ingest_file(file_path):
    """
    Ingesta un archivo individual (Draw.io, Excel, etc.)
    sin necesidad de clonar un repositorio completo.
    """

    print(f"\n[Ingesta de archivo] {file_path}")

    chunks = FileScanner.parse_file(file_path)
    chunks = CodeChunker.chunk_documents(chunks)

    if not chunks:
        print("  No se generaron chunks para este archivo.")
        return

    embedder = Embedder()
    chroma   = ChromaManager()
    indexed  = 0

    for chunk in chunks:
        try:
            embedding = embedder.generate_embedding(chunk.content)
            chroma.collection.add(
                ids=[str(uuid.uuid4())],
                documents=[chunk.content],
                embeddings=[embedding],
                metadatas=[chunk.metadata]
            )
            indexed += 1
        except Exception as e:
            print(f"  Error: {e}")

    print(f"  Chunks indexados: {indexed}")


# -------------------------------------------------------------------------
# Punto de entrada
# -------------------------------------------------------------------------

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Ingesta de conocimiento para el sistema RAG"
    )

    parser.add_argument(
        "--repo",
        type=str,
        help="URL del repositorio Git a clonar (sobreescribe .env)"
    )

    parser.add_argument(
        "--file",
        type=str,
        help="Ruta de un archivo individual a ingestar (Draw.io, Excel, etc.)"
    )

    args = parser.parse_args()

    if args.file:
        ingest_file(args.file)
    else:
        ingest_repository(repo_url=args.repo)