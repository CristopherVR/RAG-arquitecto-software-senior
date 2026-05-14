from app.retrieval.semantic_search import SemanticSearch

search_engine = SemanticSearch()

query = input("Pregunta: ")

results = search_engine.search(query)

documents = results["documents"][0]
metadatas = results["metadatas"][0]

for i, doc in enumerate(documents):

    print("\n====================")
    print(f"Resultado {i+1}")
    print("====================")

    print("\nArchivo:")
    print(metadatas[i]["path"])

    print("\nContenido:")
    print(doc[:1000])