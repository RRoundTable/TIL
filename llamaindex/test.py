from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)

query_engine = index.as_query_engine()
response = query_engine.query("Verylabs 홈페이지에 나와있는 내용에 따르면 베리챗 광고 수익의 10%를 8,000개의 노드 소유자들이 나눠가지는 것으로 나와있는데 그렇다면 나머지 광고 수익의 90% 어떤 식으로 활용이 될까요?")
print(response)