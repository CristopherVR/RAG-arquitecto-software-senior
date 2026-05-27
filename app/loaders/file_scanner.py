import os

from app.parsers.js_entity_parser import JSEntityParser
from app.parsers.python_entity_parser import PythonEntityParser
from app.parsers.code_parser import CodeParser


SUPPORTED_EXTENSIONS = {
    # JavaScript / TypeScript
    ".js", ".jsx", ".ts", ".tsx",
    # Python
    ".py",
    # Genéricos (se indexan como texto completo)
    ".md", ".yaml", ".yml", ".json",
}

IGNORED_DIRS = {
    ".git", "node_modules", "bin", "obj",
    "__pycache__", ".venv", "venv", "dist", "build"
}


class FileScanner:

    @staticmethod
    def scan_repository(repo_path):
        """
        Recorre el repositorio y retorna una lista de rutas de archivos
        con extensiones soportadas.
        """

        files = []

        for root, dirs, filenames in os.walk(repo_path):

            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

            for file in filenames:
                ext = os.path.splitext(file)[1].lower()
                if ext in SUPPORTED_EXTENSIONS:
                    files.append(os.path.join(root, file))

        return files

    @staticmethod
    def parse_file(file_path):
        """
        Recibe la ruta de un archivo y delega al parser correcto
        según su extensión. Retorna una lista de DocumentChunk.
        """

        ext = os.path.splitext(file_path)[1].lower()

        if ext in {".js", ".jsx", ".ts", ".tsx"}:
            return JSEntityParser.parse_file(file_path)

        if ext == ".py":
            return PythonEntityParser.parse_file(file_path)

        # Markdown, YAML, JSON — indexar como texto completo
        if ext in {".md", ".yaml", ".yml", ".json"}:
            chunk = CodeParser.parse_file(file_path)
            return [chunk] if chunk else []

        return []