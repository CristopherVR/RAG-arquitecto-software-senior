import xml.etree.ElementTree as ET
from app.models.document import DocumentChunk


class DrawioLoader:

    @staticmethod
    def load_drawio(file_path):

        chunks = []

        try:
            tree = ET.parse(file_path)
            root = tree.getroot()

            for cell in root.iter("mxCell"):
                value = cell.attrib.get("value", "")

                if value.strip():
                    chunks.append(DocumentChunk(
                        content=f"Elemento de diagrama Draw.io: {value}",
                        metadata={
                            "source": file_path,
                            "file": file_path,
                            "type": "drawio_xml"
                        }
                    ))

        except Exception as e:
            print(f"❌ Error leyendo Draw.io/XML: {file_path}")
            print(e)

        return chunks