from app.models.document import DocumentChunk
import os

class CodeParser:

    @staticmethod
    def parse_file(file_path):

        try:

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            return DocumentChunk(
                content=content,
                metadata={
                    "file_name": os.path.basename(file_path),
                    "path": file_path,
                    "extension": os.path.splitext(file_path)[1],
                    "entity_type": "document",           
                    "name": os.path.basename(file_path), 
                    "line": 1 
                }
            )

        except Exception as e:
            print(f"Error leyendo {file_path}: {e}")
            return None