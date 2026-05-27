import re
import os

from app.models.document import DocumentChunk


class PythonEntityParser:

    # Clases
    CLASS_PATTERN = r"^class\s+([A-Za-z][a-zA-Z0-9_]*)(?:\(.*?\))?:"

    # Funciones y métodos
    FUNCTION_PATTERN = r"^(    )?def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\("

    # Imports absolutos: import os, from app.x import Y
    IMPORT_PATTERN = r"^(?:from\s+([\w.]+)\s+import\s+([\w,\s*]+)|import\s+([\w,\s.]+))"

    # Decoradores
    DECORATOR_PATTERN = r"^(\s*)@([\w.]+)"

    # Rutas de API (FastAPI / Flask / Django)
    ROUTE_PATTERN = r"@(?:app|router)\.(get|post|put|delete|patch)\(['\"]([^'\"]+)['\"]"

    # -------------------------------------------------------------------------

    @staticmethod
    def extract_block(lines, start_line):
        """
        Extrae un bloque Python completo (clase o función) usando indentación.
        Recibe la lista de líneas y el índice de la línea donde empieza el bloque.
        Retorna el contenido como string.
        """

        if start_line >= len(lines):
            return ""

        header = lines[start_line]
        base_indent = len(header) - len(header.lstrip())

        block_lines = [header]

        for i in range(start_line + 1, len(lines)):
            line = lines[i]
            stripped = line.rstrip()

            # Línea vacía o solo espacios: se incluye pero no detiene el bloque
            if stripped == "":
                block_lines.append(line)
                continue

            current_indent = len(line) - len(line.lstrip())

            # Si la indentación volvió al nivel base o menos, el bloque terminó
            if current_indent <= base_indent and stripped:
                break

            block_lines.append(line)

        # Quitar líneas vacías al final
        while block_lines and block_lines[-1].strip() == "":
            block_lines.pop()

        return "".join(block_lines)

    @staticmethod
    def extract_imports(content):
        """Extrae todos los imports del archivo."""

        imports = []

        for match in re.finditer(
            PythonEntityParser.IMPORT_PATTERN,
            content,
            re.MULTILINE
        ):
            if match.group(1):
                imports.append({
                    "from": match.group(1),
                    "import": match.group(2).strip()
                })
            elif match.group(3):
                imports.append({
                    "import": match.group(3).strip()
                })

        return imports

    @staticmethod
    def extract_routes(content):
        """Extrae rutas de API definidas con decoradores (FastAPI / Flask)."""

        routes = []

        for match in re.finditer(PythonEntityParser.ROUTE_PATTERN, content):
            routes.append({
                "method": match.group(1).upper(),
                "path": match.group(2)
            })

        return routes

    @staticmethod
    def parse_file(file_path):
        """
        Parsea un archivo .py y retorna una lista de DocumentChunk,
        uno por cada entidad encontrada (clase, función, ruta de API).
        """

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

        except Exception as e:
            print(f"Error leyendo {file_path}: {e}")
            return []

        lines = content.splitlines(keepends=True)
        entities = []
        file_name = os.path.basename(file_path)

        imports = PythonEntityParser.extract_imports(content)
        routes = PythonEntityParser.extract_routes(content)

        current_decorators = []

        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            # Acumular decoradores
            dec_match = re.match(PythonEntityParser.DECORATOR_PATTERN, line)
            if dec_match:
                current_decorators.append(stripped)
                i += 1
                continue

            # -------------------------
            # CLASES
            # -------------------------
            class_match = re.match(
                PythonEntityParser.CLASS_PATTERN,
                stripped
            )
            if class_match:
                class_name = class_match.group(1)
                block = PythonEntityParser.extract_block(lines, i)

                entities.append(DocumentChunk(
                    content=block,
                    metadata={
                        "entity_type": "class",
                        "name": class_name,
                        "path": file_path,
                        "file_name": file_name,
                        "line": i + 1,
                        "decorators": str(current_decorators),
                        "imports": str(imports),
                        "routes": str(routes)
                    }
                ))

                current_decorators = []
                i += 1
                continue

            # -------------------------
            # FUNCIONES Y MÉTODOS
            # -------------------------
            func_match = re.match(
                r"^(    )?def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(",
                line
            )
            if func_match:
                func_name = func_match.group(2)
                is_method = func_match.group(1) is not None  # tiene indentación base
                block = PythonEntityParser.extract_block(lines, i)

                entities.append(DocumentChunk(
                    content=block,
                    metadata={
                        "entity_type": "method" if is_method else "function",
                        "name": func_name,
                        "path": file_path,
                        "file_name": file_name,
                        "line": i + 1,
                        "decorators": str(current_decorators),
                        "imports": str(imports),
                        "routes": str(routes)
                    }
                ))

                current_decorators = []
                i += 1
                continue

            # Si la línea no es decorador, clase ni función, resetear decoradores
            if stripped and not stripped.startswith("#"):
                current_decorators = []

            i += 1

        # Fallback: indexar archivo completo si no se detectó ninguna entidad
        if not entities:
            entities.append(DocumentChunk(
                content=content,
                metadata={
                    "entity_type": "file",
                    "name": file_name,
                    "path": file_path,
                    "file_name": file_name,
                    "line": 1,
                    "imports": str(imports),
                    "routes": str(routes)
                }
            ))

        return entities