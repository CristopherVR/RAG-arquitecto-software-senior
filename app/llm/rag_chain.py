from app.retrieval.semantic_search import SemanticSearch
from app.llm.llm_client import LLMClient
from app.llm.prompt_templates import SYSTEM_PROMPT, build_user_prompt


class RAGChain:

    def __init__(self, top_k=3):
        """
        Parámetros:
            top_k : número de fragmentos a recuperar de ChromaDB por consulta
        """

        self.search_engine = SemanticSearch()
        self.llm = LLMClient()
        self.top_k = top_k
        self.history = []       # Memoria de conversación

    # -------------------------------------------------------------------------

    def query(self, user_question):
        """
        Pipeline RAG completo:
        1. Recuperar fragmentos relevantes de ChromaDB
        2. Construir prompt con contexto + historial
        3. Enviar al LLM y retornar respuesta con fuentes
        """

        # 1. RECUPERACIÓN
        results = self.search_engine.search(user_question, top_k=self.top_k)

        chunks = self._parse_results(results)

        if not chunks:
            return {
                "answer": "No encontré información suficiente en la base de conocimiento para responder esto.",
                "sources": [],
                "chunks_used": 0
            }

        # 2. CONSTRUCCIÓN DEL PROMPT
        # Incluir historial reciente para memoria de contexto (últimas 3 rondas)
        history_text = self._build_history_text()

        full_question = (
            f"{history_text}\n\nPregunta actual: {user_question}"
            if history_text
            else user_question
        )

        user_prompt = build_user_prompt(full_question, chunks)

        # 3. GENERACIÓN
        answer = self.llm.generate(SYSTEM_PROMPT, user_prompt)

        # 4. GUARDAR EN HISTORIAL
        self.history.append({
            "question": user_question,
            "answer": answer
        })

        # 5. EXTRAER FUENTES DEL METADATA
        sources = self._extract_sources(chunks)

        return {
            "answer": answer,
            "sources": sources,
            "chunks_used": len(chunks)
        }

    def reset_history(self):
        """Limpia el historial de conversación."""
        self.history = []

    # -------------------------------------------------------------------------
    # Métodos privados
    # -------------------------------------------------------------------------

    def _parse_results(self, results):
        """
        Convierte el formato de respuesta de ChromaDB a una lista de dicts
        con 'content' y 'metadata'.
        """

        chunks = []

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]

        for doc, meta in zip(documents, metadatas):
            if doc:
                chunks.append({
                    "content": doc,
                    "metadata": meta or {}
                })

        return chunks

    def _build_history_text(self):
        """
        Construye un resumen del historial reciente (últimas 3 rondas)
        para incluir como contexto de conversación.
        """

        if not self.history:
            return ""

        recent = self.history[-3:]
        lines = ["Historial de conversación reciente:"]

        for i, turn in enumerate(recent, start=1):
            lines.append(f"  [{i}] Usuario: {turn['question']}")
            # Incluir solo las primeras 200 chars de la respuesta anterior
            short_answer = turn["answer"][:200].replace("\n", " ")
            lines.append(f"       Asistente: {short_answer}...")

        return "\n".join(lines)

    def _extract_sources(self, chunks):
        """
        Extrae y deduplica las fuentes de los chunks recuperados.
        Retorna una lista de dicts con la información de cada fuente.
        """

        seen = set()
        sources = []

        for chunk in chunks:
            meta = chunk["metadata"]
            path = meta.get("path", "desconocido")

            if path in seen:
                continue
            seen.add(path)

            sources.append({
                "file": meta.get("file_name", "desconocido"),
                "path": path,
                "entity_type": meta.get("entity_type", ""),
                "name": meta.get("name", ""),
                "line": meta.get("line", ""),
            })

        return sources