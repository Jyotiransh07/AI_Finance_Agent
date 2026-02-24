from sentence_transformers import SentenceTransformer
import faiss
import os
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

documents = []
for file in os.listdir("data"):
    with open("data/" + file, "r", encoding="utf-8") as f:
        documents.append(f.read())

embeddings = model.encode(documents)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

def retrieve(query):
    query_vector = model.encode([query])
    D, I = index.search(np.array(query_vector), k=2)
    return [documents[i] for i in I[0]]