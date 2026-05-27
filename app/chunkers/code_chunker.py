from app.models.document import DocumentChunk


CHUNK_SIZE = 1500       # Tamaño máximo por chunk (caracteres)
CHUNK_OVERLAP = 150     # Solapamiento entre chunks para no perder contexto


class CodeChunker:

    @staticmethod
    def chunk_document(document):
        """
        Recibe un DocumentChunk y lo divide si su contenido supera CHUNK_SIZE.

        Estrategia semántica:
        1. Si el bloque cabe entero → se retorna tal cual, sin cortar.
        2. Si es muy largo → se divide por líneas respetando el límite,
           con solapamiento entre chunks para no perder contexto en los bordes.

        Esto evita el problema del corte ciego a mitad de una función.
        """

        content = document.content

        # Si cabe entero, no hay nada que dividir
        if len(content) <= CHUNK_SIZE:
            return [document]

        lines = content.splitlines(keepends=True)
        chunks = []
        current_lines = []
        current_size = 0
        part = 1

        for line in lines:
            line_size = len(line)

            # Si agregar esta línea supera el límite, cerrar chunk actual
            if current_size + line_size > CHUNK_SIZE and current_lines:

                chunk_content = "".join(current_lines)

                chunks.append(DocumentChunk(
                    content=chunk_content,
                    metadata={
                        **document.metadata,
                        "chunk_part": part,
                        "chunk_total": "?",     # se actualiza al final
                    }
                ))

                part += 1

                # Solapamiento: conservar las últimas líneas del chunk anterior
                overlap_lines = _get_overlap_lines(current_lines, CHUNK_OVERLAP)
                current_lines = overlap_lines + [line]
                current_size = sum(len(l) for l in current_lines)

            else:
                current_lines.append(line)
                current_size += line_size

        # Último chunk
        if current_lines:
            chunks.append(DocumentChunk(
                content="".join(current_lines),
                metadata={
                    **document.metadata,
                    "chunk_part": part,
                    "chunk_total": "?",
                }
            ))

        # Actualizar chunk_total ahora que sabemos cuántos son
        total = len(chunks)
        for chunk in chunks:
            chunk.metadata["chunk_total"] = total

        return chunks

    @staticmethod
    def chunk_documents(documents):
        """
        Procesa una lista de DocumentChunk y retorna todos los chunks resultantes.
        Útil para pasar directamente la salida de un parser.
        """

        result = []
        for doc in documents:
            result.extend(CodeChunker.chunk_document(doc))
        return result


# -------------------------------------------------------------------------
# Helpers privados
# -------------------------------------------------------------------------

def _get_overlap_lines(lines, max_chars):
    """
    Retorna las últimas líneas de una lista hasta alcanzar max_chars.
    Se usa para el solapamiento entre chunks.
    """

    overlap = []
    size = 0

    for line in reversed(lines):
        if size + len(line) > max_chars:
            break
        overlap.insert(0, line)
        size += len(line)

    return overlap