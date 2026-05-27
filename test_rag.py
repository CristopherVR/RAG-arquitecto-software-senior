from app.llm.rag_chain import RAGChain

rag = RAGChain()

result = rag.query("Lista los componentes React encontrados, solo sus nombres y en qué archivo están.")

print("RESPUESTA:")
print(result["answer"])

print("\nFUENTES:")
for s in result["sources"]:
    print(f"  - {s['file']} | {s['entity_type']} | {s['name']}")