import re
import os

from app.models.document import DocumentChunk
from app.parsers.dependency_parser import DependencyParser


class JSParser:

    FUNCTION_PATTERN = r"(const|function)\s+([a-zA-Z0-9_]+)"

    @staticmethod
    def parse_file(file_path):

        try:

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # EXTRAER DEPENDENCIAS
            dependencies = DependencyParser.extract_dependencies(
                content
            )

            chunks = []

            matches = list(
                re.finditer(
                    JSParser.FUNCTION_PATTERN,
                    content
                )
            )

            for i, match in enumerate(matches):

                start = match.start()

                end = (
                    matches[i + 1].start()
                    if i + 1 < len(matches)
                    else len(content)
                )

                function_content = content[start:end]

                function_name = match.group(1)

                chunks.append(
                    DocumentChunk(
                        content=function_content,
                        metadata={
                            "type": "function",
                            "function_name": function_name,
                            "path": file_path,
                            "file_name": os.path.basename(file_path),

                            # NUEVO
                            "dependencies": str(dependencies)
                        }
                    )
                )

            return chunks

        except Exception as e:

            print(f"Error parsing {file_path}: {e}")

            return []