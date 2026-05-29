from pypdf import PdfReader


class PDFParser:

    @staticmethod
    def parse_file(file_path):

        from app.models.document import DocumentChunk

        documents = []

        try:
            reader = PdfReader(file_path)

            for page_num, page in enumerate(reader.pages):

                text = page.extract_text()

                if text and text.strip():

                    documents.append(
                        DocumentChunk(
                            content=text,
                            metadata={
                                "source": file_path,
                                "file": file_path,
                                "page": page_num + 1,
                                "type": "pdf"
                            }
                        )
                    )

        except Exception as e:
            print("Error leyendo PDF:")
            print(e)

        return documents