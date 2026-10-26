# subse palihe we will import all the required things we want to use our qdrant vector database
import os

from pathlib import Path
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from groq import Groq

# .env se hamare variables ko load krenge
load_dotenv()


QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
GROQ_API_KEY=os.getenv("GROQ_API_KEY")



# client banayenge for connection with groq and qdrant

client = QdrantClient(
    url = QDRANT_URL,
    api_key=QDRANT_API_KEY
)
print("connected to qdrant cloud")

COLLECTION_NAME="knowledge"
EMBEDDING_SIZE = 384

# agar koi collection palihe se hai to usko delete kar do
if client.collection_exists(COLLECTION_NAME):
    print(f""" Deleting existing collection: {COLLECTION_NAME}""")
    client.delete_collection(COLLECTION_NAME)

# create collection

client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(
        size=EMBEDDING_SIZE,
        distance=Distance.COSINE
    )
)

print(f"Created collection: {COLLECTION_NAME}")
print(f"Vector size: {EMBEDDING_SIZE}")
print("Distance: COSINE")


# ab humne ek saperate file banayi hai knowledge.txt usko hum yha use karne ke liye load karenge

with open("knowledge.txt","r",encoding="utf-8") as f:
    documents = [
        line.strip()
        for line in f
        if line.strip()
    ]

print(f"Loded {len(documents)}documents")


#  ab hum embedding banayenge

print("loading embedding model")

model=SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model ready hai")

# ye jo uppar hum knowledge.txt ke andar se lines nikal ke documents array me save karwa rhe h wo h
embeddings = model.encode(documents)

print(f"Generated {len(embeddings)} embeddings")
print(f"Embedding size: {len(embeddings[0])}")


# ab hum banayenge qdrant ke points
points = []

for i, embedding in enumerate(embeddings):
    point = PointStruct(
        id=i+1,

        vector=embedding.tolist(),

        payload={
            "text":documents[i]
        }
    )
    points.append(point)


# ab hum in points jo humne banaye hai unko upload karenge qdrant me
# upsert =  upload + insert means agar palihe se point hai to khuch mnat kro lakin nhi hai to insert kar do
client.upsert(
    collection_name=COLLECTION_NAME,
    points=points
)

print(f"Uploaded {len(points)} documents to Qdrant")


# ab hum search krenge cosine similarity nikalenge wo bhi us data se jo humne qdrant me save kar dia h

def search(query, top_k=3):

    #convert the question into a embedding taki cosine similarity nikal sake 
    query_vector = model.encode(query).tolist()

    # search qdrant for similar vector
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
        with_payload = True
    ).points
    return results


#  ab jo bhi results aaye hum uska score print karenge

query = "How many vacation days do I get?"

results = search(query, top_k=3)

print("\nSearch results:")

for result in results:
    print(f"Score: {result.score:.3f}")
    print(result.payload["text"])
    print()

#  groq wala llm client banayenge

groq_client = Groq(
    api_key=GROQ_API_KEY
)

# PART 11 — ASK THE LLM
# ============================================================

def ask_llm(question, context):

    prompt = f"""
Answer the question using only the information provided below.

Context:
{context}

Question:
{question}

If the answer is not present in the context, say:
"I don't know based on the provided information."
"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


# ============================================================
# PART 12 — COMPLETE RAG PIPELINE
# ============================================================

question = "How many vacation days do I get?"

results = search(question, top_k=3)


# Extract text from the search results
context = "\n".join(
    result.payload["text"]
    for result in results
)


answer = ask_llm(question, context)


print("\nFinal Answer:")
print(answer)