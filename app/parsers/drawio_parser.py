import os
from lxml import etree
from app.models.document import DocumentChunk


class DrawIOParser:

    @staticmethod
    def parse_file(file_path):
        """
        Parsea un archivo .drawio o .xml de Draw.io y retorna una lista
        de DocumentChunk: uno por diagrama, uno por nodo y uno por conector.
        """

        try:
            tree = etree.parse(file_path)
            root = tree.getroot()
        except Exception as e:
            print(f"Error leyendo {file_path}: {e}")
            return []

        file_name = os.path.basename(file_path)
        entities = []

        # Un archivo Draw.io puede tener múltiples páginas (diagram)
        diagrams = root.findall(".//diagram")

        if not diagrams:
            # Algunos exports tienen el contenido directamente en la raíz
            diagrams = [root]

        for diagram in diagrams:
            diagram_name = diagram.get("name", "sin_nombre")

            # Los nodos están dentro de mxGraphModel > root > mxCell
            cells = diagram.findall(".//mxCell")

            nodes = {}    # id -> label
            edges = []    # lista de relaciones entre nodos

            for cell in cells:
                cell_id    = cell.get("id", "")
                cell_value = cell.get("value", "").strip()
                is_vertex  = cell.get("vertex") == "1"
                is_edge    = cell.get("edge") == "1"
                style      = cell.get("style", "")

                # -------------------------
                # NODOS (vertex)
                # -------------------------
                if is_vertex and cell_value:
                    nodes[cell_id] = cell_value

                    entities.append(DocumentChunk(
                        content=f"Componente de arquitectura: {cell_value}\n"
                                f"Diagrama: {diagram_name}\n"
                                f"Estilo: {style}",
                        metadata={
                            "entity_type": "architecture_node",
                            "name": cell_value,
                            "diagram": diagram_name,
                            "cell_id": cell_id,
                            "path": file_path,
                            "file_name": file_name,
                            "line": 1
                        }
                    ))

                # -------------------------
                # CONECTORES (edge)
                # -------------------------
                if is_edge:
                    source_id = cell.get("source", "")
                    target_id = cell.get("target", "")
                    label     = cell_value or "conecta"

                    edges.append({
                        "source_id": source_id,
                        "target_id": target_id,
                        "label": label
                    })

            # Resolver nombres de source/target usando el mapa de nodos
            for edge in edges:
                source_name = nodes.get(edge["source_id"], edge["source_id"])
                target_name = nodes.get(edge["target_id"], edge["target_id"])
                label       = edge["label"]

                content = (
                    f"Relación de arquitectura:\n"
                    f"  Origen:  {source_name}\n"
                    f"  Destino: {target_name}\n"
                    f"  Tipo:    {label}\n"
                    f"  Diagrama: {diagram_name}"
                )

                entities.append(DocumentChunk(
                    content=content,
                    metadata={
                        "entity_type": "architecture_edge",
                        "name": f"{source_name} -> {target_name}",
                        "source": source_name,
                        "target": target_name,
                        "label": label,
                        "diagram": diagram_name,
                        "path": file_path,
                        "file_name": file_name,
                        "line": 1
                    }
                ))

            # Chunk de resumen del diagrama completo
            if nodes:
                node_list = "\n".join(f"  - {v}" for v in nodes.values() if v)
                edge_list = "\n".join(
                    f"  - {nodes.get(e['source_id'], e['source_id'])} "
                    f"--[{e['label']}]--> "
                    f"{nodes.get(e['target_id'], e['target_id'])}"
                    for e in edges
                ) or "  (sin conectores)"

                summary = (
                    f"Resumen del diagrama '{diagram_name}':\n\n"
                    f"Componentes ({len(nodes)}):\n{node_list}\n\n"
                    f"Relaciones ({len(edges)}):\n{edge_list}"
                )

                entities.append(DocumentChunk(
                    content=summary,
                    metadata={
                        "entity_type": "architecture_diagram",
                        "name": diagram_name,
                        "diagram": diagram_name,
                        "node_count": len(nodes),
                        "edge_count": len(edges),
                        "path": file_path,
                        "file_name": file_name,
                        "line": 1
                    }
                ))

        return entities