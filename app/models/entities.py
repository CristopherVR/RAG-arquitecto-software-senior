from dataclasses import dataclass

@dataclass
class CodeEntity:

    entity_type: str
    name: str
    content: str
    metadata: dict