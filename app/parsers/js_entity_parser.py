import re
import os

from app.models.document import DocumentChunk
from app.parsers.dependency_parser import DependencyParser


class JSEntityParser:

    # React Components
    COMPONENT_PATTERN = r"export\s+default\s+function\s+([A-Z][a-zA-Z0-9_]+)"

    # Named functions (const/let/var/function)
    FUNCTION_PATTERN = r"(?:export\s+)?(?:const|let|var|function)\s+([a-z][a-zA-Z0-9_]+)\s*(?:=\s*(?:async\s*)?\(|[({])"

    # Services
    SERVICE_PATTERN = r"const\s+([a-zA-Z0-9_]+Service)\s*="

    # Hooks
    HOOK_PATTERN = r"(useState|useEffect|useRef|useMemo|useCallback|useContext|useReducer)"

    # API Calls
    API_PATTERN = r"api\.(get|post|put|delete|patch)\(['\"]([^'\"]+)['\"]"

    # Relationships
    SERVICE_USAGE_PATTERN = r"\b([A-Za-z][a-zA-Z0-9_]*Service)\b"
    CALLS_API_PATTERN = r"api\.(get|post|put|delete|patch)\(['\"]([^'\"]+)['\"]"

    # -------------------------------------------------------------------------

    @staticmethod
    def extract_block(content, start_index):
        """Extrae el bloque de código completo a partir de un índice dado."""

        brace_count = 0
        block_end = start_index
        inside_block = False

        for i in range(start_index, len(content)):
            char = content[i]

            if char == "{":
                brace_count += 1
                inside_block = True
            elif char == "}":
                brace_count -= 1
                if inside_block and brace_count == 0:
                    block_end = i
                    break

        return content[start_index:block_end + 1]

    @staticmethod
    def extract_relationships(content):
        """
        Extrae relaciones del contenido:
        - Servicios usados
        - API calls
        - Hooks de React
        """

        relationships = []

        # Servicios
        for match in re.finditer(JSEntityParser.SERVICE_USAGE_PATTERN, content):
            relationships.append({
                "type": "USES_SERVICE",
                "target": match.group(1)
            })

        # API calls
        for match in re.finditer(JSEntityParser.CALLS_API_PATTERN, content):
            relationships.append({
                "type": "CALLS_API",
                "method": match.group(1),
                "target": match.group(2)
            })

        # Hooks
        for match in re.finditer(JSEntityParser.HOOK_PATTERN, content):
            relationships.append({
                "type": "USES_HOOK",
                "target": match.group(1)
            })

        return relationships

    @staticmethod
    def parse_file(file_path):
        """
        Parsea un archivo JS/TS/JSX/TSX y retorna una lista de DocumentChunk,
        uno por cada entidad encontrada (componente, función, servicio, hook, api call).
        """

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

        except Exception as e:
            print(f"Error leyendo {file_path}: {e}")
            return []

        entities = []
        file_name = os.path.basename(file_path)

        dependencies = DependencyParser.extract_dependencies(content)
        relationships = JSEntityParser.extract_relationships(content)

        # -------------------------
        # COMPONENTES REACT
        # -------------------------
        for match in re.finditer(JSEntityParser.COMPONENT_PATTERN, content):
            name = match.group(1)
            block = JSEntityParser.extract_block(content, match.start())

            entities.append(DocumentChunk(
                content=block,
                metadata={
                    "entity_type": "component",
                    "name": name,
                    "path": file_path,
                    "file_name": file_name,
                    "dependencies": str(dependencies),
                    "relationships": str(relationships)
                }
            ))

        # -------------------------
        # FUNCIONES (solo minúscula para no duplicar componentes)
        # -------------------------
        seen_functions = set()

        for match in re.finditer(JSEntityParser.FUNCTION_PATTERN, content):
            name = match.group(1)

            if name in seen_functions:
                continue
            seen_functions.add(name)

            block = JSEntityParser.extract_block(content, match.start())

            entities.append(DocumentChunk(
                content=block,
                metadata={
                    "entity_type": "function",
                    "name": name,
                    "path": file_path,
                    "file_name": file_name,
                    "dependencies": str(dependencies),
                    "relationships": str(relationships)
                }
            ))

        # -------------------------
        # SERVICIOS
        # -------------------------
        for match in re.finditer(JSEntityParser.SERVICE_PATTERN, content):
            name = match.group(1)
            block = JSEntityParser.extract_block(content, match.start())

            entities.append(DocumentChunk(
                content=block,
                metadata={
                    "entity_type": "service",
                    "name": name,
                    "path": file_path,
                    "file_name": file_name,
                    "dependencies": str(dependencies),
                    "relationships": str(relationships)
                }
            ))

        # -------------------------
        # API CALLS
        # -------------------------
        for match in re.finditer(JSEntityParser.API_PATTERN, content):
            method = match.group(1)
            endpoint = match.group(2)
            block = JSEntityParser.extract_block(content, match.start())

            entities.append(DocumentChunk(
                content=block,
                metadata={
                    "entity_type": "api_call",
                    "method": method,
                    "endpoint": endpoint,
                    "path": file_path,
                    "file_name": file_name,
                    "dependencies": str(dependencies),
                    "relationships": str(relationships)
                }
            ))

        if not entities:
            # Fallback: si no se detectó ninguna entidad, indexar el archivo completo
            entities.append(DocumentChunk(
                content=content,
                metadata={
                    "entity_type": "file",
                    "name": file_name,
                    "path": file_path,
                    "file_name": file_name,
                    "dependencies": str(dependencies),
                    "relationships": str(relationships)
                }
            ))

        return entities