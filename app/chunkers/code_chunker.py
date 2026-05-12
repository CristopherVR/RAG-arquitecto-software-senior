from app.models.document import DocumentChunk

class CodeChunker:

    CHUNK_SIZE = 1500

    @staticmethod
    def chunk_document(document):

        content = document.content

        chunks = []

        start = 0

        while start < len(content):

            end = start + CodeChunker.CHUNK_SIZE

            chunk_content = content[start:end]

            chunks.append(
                DocumentChunk(
                    content=chunk_content,
                    metadata=document.metadata
                )
            )

            start = end

        return chunks