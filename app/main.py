from app.loaders.git_loader import GitLoader
from app.loaders.file_scanner import FileScanner
from app.parsers.code_parser import CodeParser
from app.chunkers.code_chunker import CodeChunker
from app.embeddings.embedder import Embedder
from app.vectorstore.chroma_client import ChromaManager

import uuid

REPO_URL = "https://github.com/tu_repo.git"

LOCAL_REPO = "./repos/project"

def main():

    GitLoader.clone_repository(
        REPO_URL,
        LOCAL_REPO
    )

    files = FileScanner.scan_repository(LOCAL_REPO)

    print(f"Archivos encontrados: {len(files)}")

    embedder = Embedder()

    chroma = ChromaManager()

    for file in files:

        document = CodeParser.parse_file(file)

        if not document:
            continue

        chunks = CodeChunker.chunk_document(document)

        for chunk in chunks:

            embedding = embedder.generate_embedding(
                chunk.content
            )

            chroma.collection.add(
                ids=[str(uuid.uuid4())],
                documents=[chunk.content],
                embeddings=[embedding],
                metadatas=[chunk.metadata]
            )

            print(f"Indexado: {file}")

if __name__ == "__main__":
    main()