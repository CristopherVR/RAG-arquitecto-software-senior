import os

from app.parsers.pdf_parser import PDFParser
from app.parsers.drawio_parser import DrawIOParser
from app.parsers.excel_parser import ExcelParser
from app.parsers.js_entity_parser import JSEntityParser
from app.parsers.python_entity_parser import PythonEntityParser
from app.parsers.code_parser import CodeParser


SUPPORTED_EXTENSIONS = {
    # JavaScript / TypeScript
    ".js", ".jsx", ".ts", ".tsx",

    # Python
    ".py",

    ".cs",

    # Draw.io y XML
    ".drawio", ".xml",

    # Excel y CSV
    ".xlsx", ".csv",

    ".pdf",

    # Genéricos
    ".md", ".yaml", ".yml", ".json",
}


IGNORED_DIRS = {
    ".git", "node_modules", "bin", "obj",
    "__pycache__", ".venv", "venv", "dist", "build"
}


class FileScanner:

    @staticmethod
    def scan_repository(repo_path):
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
        ext = os.path.splitext(file_path)[1].lower()

        if ext in {".js", ".jsx", ".ts", ".tsx"}:
            return JSEntityParser.parse_file(file_path)

        if ext == ".py":
            return PythonEntityParser.parse_file(file_path)

        if ext == ".drawio":
            return DrawIOParser.parse_file(file_path)

        if ext == ".xml":
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    snippet = f.read(500)

                if "mxCell" in snippet or "mxGraphModel" in snippet:
                    return DrawIOParser.parse_file(file_path)

            except Exception:
                pass

            chunk = CodeParser.parse_file(file_path)
            return [chunk] if chunk else []

        if ext == ".xlsx":
            return ExcelParser.parse_file(file_path)
        
        if ext == ".pdf":
            return PDFParser.parse_file(file_path)

        if ext == ".csv":
            chunk = CodeParser.parse_file(file_path)
            return [chunk] if chunk else []

        if ext in {".md", ".yaml", ".yml", ".json"}:
            chunk = CodeParser.parse_file(file_path)
            return [chunk] if chunk else []

        return []