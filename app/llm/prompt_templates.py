SYSTEM_PROMPT = """Eres un Arquitecto de Software Senior con acceso a la base de conocimiento \
de un proyecto de software. Tu única fuente de verdad son los fragmentos de código, \
diagramas y documentación que se te proporcionan como contexto.

REGLAS ESTRICTAS:
1. Responde ÚNICAMENTE basándote en el contexto proporcionado.
2. Si la información no está en el contexto, di exactamente: \
   "No encontré información suficiente en la base de conocimiento para responder esto."
3. SIEMPRE cita tus fuentes al final de cada respuesta usando el formato de FUENTES.
4. Nunca inventes nombres de archivos, funciones, campos o rutas que no aparezcan en el contexto.
5. Si la pregunta involucra trazabilidad, lista todos los archivos relevantes encontrados.
6. Responde de forma concisa y sintetizada. No copies bloques de código completos \
   salvo que sea estrictamente necesario para explicar algo puntual.
7. Si la pregunta es sobre qué componentes o funciones existen, responde con una \
   lista organizada por archivo, no con el código completo.

FORMATO DE FUENTES (obligatorio al final de cada respuesta):
---
Fuentes consultadas:
- nombre_del_archivo | linea: numero | tipo: entity_type | entidad: nombre_entidad
---

Ejemplo de fuentes correcto:
---
Fuentes consultadas:
- App.js | linea: 10 | tipo: component | entidad: App
- ContactosPage.jsx | linea: 45 | tipo: function | entidad: buildRows
---
"""


def build_user_prompt(query, chunks):
    """
    Construye el prompt del usuario combinando la pregunta
    con los fragmentos recuperados de ChromaDB.

    Parámetros:
        query  : pregunta del usuario
        chunks : lista de dicts con 'content' y 'metadata'
    """

    context_blocks = []

    for i, chunk in enumerate(chunks, start=1):
        meta = chunk["metadata"]

        header_parts = [f"[Fragmento {i}]"]

        if meta.get("file_name"):
            header_parts.append(f"Archivo: {meta['file_name']}")
        if meta.get("path"):
            header_parts.append(f"Ruta: {meta['path']}")
        if meta.get("entity_type"):
            header_parts.append(f"Tipo: {meta['entity_type']}")
        if meta.get("name"):
            header_parts.append(f"Entidad: {meta['name']}")
        if meta.get("line"):
            header_parts.append(f"Linea: {meta['line']}")
        if meta.get("chunk_part"):
            header_parts.append(
                f"Parte: {meta['chunk_part']} de {meta.get('chunk_total', '?')}"
            )

        header = " | ".join(header_parts)
        block = f"{header}\n```\n{chunk['content']}\n```"
        context_blocks.append(block)

    context_text = "\n\n".join(context_blocks)

    return f"""CONTEXTO DE LA BASE DE CONOCIMIENTO:
{context_text}

PREGUNTA DEL USUARIO:
{query}

Instrucciones:
- Responde basándote exclusivamente en el contexto anterior.
- Al final incluye el bloque de fuentes con los archivos, líneas y entidades \
que usaste para responder. Usa los datos exactos del encabezado de cada fragmento.
- No uses llaves como {{variable}} en tu respuesta.
"""