import re

class DependencyParser:

    FUNCTION_PATTERN = r"(?:const|let|var|function)\s+([a-zA-Z0-9_]+)"

    @staticmethod
    def extract_dependencies(content):

        matches = re.findall(
            DependencyParser.IMPORT_PATTERN,
            content
        )

        dependencies = []

        for match in matches:

            imported_item = match[0]
            imported_from = match[1]

            dependencies.append({
                "import": imported_item,
                "from": imported_from
            })

        return dependencies