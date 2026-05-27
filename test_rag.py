from app.llm.rag_chain import RAGChain

rag = RAGChain()

result = rag.query("¿Qué componentes React existen en el repositorio?")

print("RESPUESTA:")
print(result["answer"])

print("\nFUENTES:")
for s in result["sources"]:
    print(f"  - {s['file']} | {s['entity_type']} | {s['name']}")