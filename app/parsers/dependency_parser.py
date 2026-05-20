import re


class DependencyParser:

    IMPORT_PATTERN = r'import\s+(.*?)\s+from\s+[\'"](.*?)[\'"]'

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