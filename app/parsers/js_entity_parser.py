import re
import os

from app.models.document import DocumentChunk
from app.parsers.dependency_parser import DependencyParser


class JSEntityParser:

    # React Components
    COMPONENT_PATTERN = r"export\s+default\s+function\s+([A-Z][a-zA-Z0-9_]+)"

    # Functions
    FUNCTION_PATTERN = r"(?:const|let|var|function)\s+([a-zA-Z0-9_]+)"

    # Services
    SERVICE_PATTERN = r"const\s+([a-zA-Z0-9_]+Service)\s*="

    # Hooks
    HOOK_PATTERN = r"(useState|useEffect|useRef|useMemo|useCallback)"

    # API Calls
    API_PATTERN = r"api\.(get|post|put|delete)\(['\"](.*?)['\"]"

    @staticmethod
    def extract_block(content, start_index):

        brace_count = 0
        block_start = start_index
        block_end = start_index

        inside_block = False

        for i in range(start_index, len(content)):

            char = content[i]

            if char == "{":

                brace_count += 1
                inside_block = True

            elif char == "}":

                brace_count -= 1

                if inside_block and brace_count == 0:

                    block_end = i
                    break

        return content[block_start:block_end + 1]

    @staticmethod
    def parse_file(file_path):

        try:

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            entities = []

            # DEPENDENCIAS
            dependencies = DependencyParser.extract_dependencies(
                content
            )

            # =========================
            # COMPONENTES REACT
            # =========================

            component_matches = re.finditer(
                JSEntityParser.COMPONENT_PATTERN,
                content
            )

            for match in component_matches:

                component_name = match.group(1)

                component_content = JSEntityParser.extract_block(
                    content,
                    match.start()
                )

                entities.append(
                    DocumentChunk(
                        content=component_content,
                        metadata={
                            "entity_type": "component",
                            "name": component_name,
                            "path": file_path,
                            "file_name": os.path.basename(file_path),
                            "dependencies": str(dependencies)
                        }
                    )
                )

            # =========================
            # FUNCIONES
            # =========================

            function_matches = re.finditer(
                JSEntityParser.FUNCTION_PATTERN,
                content
            )

            for match in function_matches:

                function_name = match.group(1)

                function_content = JSEntityParser.extract_block(
                    content,
                    match.start()
                )

                entities.append(
                    DocumentChunk(
                        content=function_content,
                        metadata={
                            "entity_type": "function",
                            "name": function_name,
                            "path": file_path,
                            "file_name": os.path.basename(file_path),
                            "dependencies": str(dependencies)
                        }
                    )
                )

            # =========================
            # SERVICES
            # =========================

            service_matches = re.finditer(
                JSEntityParser.SERVICE_PATTERN,
                content
            )

            for match in service_matches:

                service_name = match.group(1)

                service_content = JSEntityParser.extract_block(
                    content,
                    match.start()
                )

                entities.append(
                    DocumentChunk(
                        content=service_content,
                        metadata={
                            "entity_type": "service",
                            "name": service_name,
                            "path": file_path,
                            "file_name": os.path.basename(file_path),
                            "dependencies": str(dependencies)
                        }
                    )
                )

            # =========================
            # HOOKS
            # =========================

            hook_matches = re.finditer(
                JSEntityParser.HOOK_PATTERN,
                content
            )

            for match in hook_matches:

                hook_name = match.group(1)

                hook_content = JSEntityParser.extract_block(
                    content,
                    match.start()
                )

                entities.append(
                    DocumentChunk(
                        content=hook_content,
                        metadata={
                            "entity_type": "hook",
                            "name": hook_name,
                            "path": file_path,
                            "file_name": os.path.basename(file_path)
                        }
                    )
                )

            # =========================
            # API CALLS
            # =========================

            api_matches = re.finditer(
                JSEntityParser.API_PATTERN,
                content
            )

            for match in api_matches:

                method = match.group(1)
                endpoint = match.group(2)

                api_content = JSEntityParser.extract_block(
                    content,
                    match.start()
                )

                entities.append(
                    DocumentChunk(
                        content=api_content,
                        metadata={
                            "entity_type": "api_call",
                            "method": method,
                            "endpoint": endpoint,
                            "path": file_path,
                            "file_name": os.path.basename(file_path)
                        }
                    )
                )

            return entities

        except Exception as e:

            print(f"Error parsing {file_path}: {e}")

            return []