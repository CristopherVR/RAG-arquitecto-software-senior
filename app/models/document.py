from dataclasses import dataclass

@dataclass
class DocumentChunk:

    content: str
    metadata: dict