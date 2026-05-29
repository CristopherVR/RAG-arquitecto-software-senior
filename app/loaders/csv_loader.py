import csv
from app.models.document import DocumentChunk


class CSVLoader:

    @staticmethod
    def load_csv(file_path):

        chunks = []

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)

                for row_number, row in enumerate(reader, start=2):

                    content = f"Diccionario de datos CSV, fila {row_number}:\n"

                    for key, value in row.items():
                        content += f"{key}: {value}\n"

                    chunks.append(DocumentChunk(
                        content=content,
                        metadata={
                            "source": file_path,
                            "file": file_path,
                            "row": row_number,
                            "type": "csv_dictionary"
                        }
                    ))

        except Exception as e:
            print(f"❌ Error leyendo CSV: {file_path}")
            print(e)

        return chunks