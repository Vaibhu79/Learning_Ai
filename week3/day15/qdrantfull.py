import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue, MatchAny, PayloadSchemaType
from sentence_transformers import SentenceTransformer
from groq import Groq
import json

# Load .env's variables

load_dotenv()

# subse palihe keys connect kar lenge groq and qdrant client ki
QDRANT_URL=os.getenv("QDRANT_URL"),
QDRANT_API_KEY=os.getenv("QDRANT_API_KEY"),
GROQ_API_KEY=os.getenv("GROQ_API_KEY")

# fir qdrant ka client bana lenge
client = QdrantClient(
    url=QDRANT_URL,
    api_key=GROQ_API_KEY
)

print("connected to qdrant db cloud successfully")


# ab hum banayenge qdrant ka ek collection

COLLECTION_NAME = "knowledge_filter"
EMBEDDING_SIZE= 384

# ab hum aisa function banayenge ki agar ye collection palihe se hai toh fir usko dele karke new collection banao

if client.collection_exists(COLLECTION_NAME):
    print(f" Deleting existing collection {COLLECTION_NAME}")
    client.delete_collection(COLLECTION_NAME)

# create karenge collection ko

client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(
        size=EMBEDDING_SIZE,
        distance=Distance.COSINE,
    )
)

print(f"created collection{COLLECTION_NAME}")
print(f"vector size {EMBEDDING_SIZE}")
print("distance: COSINE")

# index banana padega taki hum kisi bhi chiz pe filtering use kar sake
client.create_payload_index(
    collection_name = COLLECTION_NAME,
    field_name="category",
    field_schema=PayloadSchemaType.KEYWORD
)


# hamari json file import karke knowledge base ka use karenge 

with open("knowledge.json", "r", encoding="utf-8") as f:
    documents = json.load(f)

# embedding banaenyenge ab hum

print("Loading embedding model...")

model= SentenceTransformer("all-MiniLM-L6-v2") #384

print("Embedding model ready!")
texts = [document["text"] for document in documents]


embeddings = model.encode(texts)

print(f"Generated {len(embeddings)} embeddings")
print(f"Embedding size: {len(embeddings[0])}")


# ab hum hamare qdrant me data store karne ke liye points banayenge

for i in range(len(documents)):
    point = PointStruct(
        id= i+1,
        vector=embeddings[i].tolist(),
        payload=documents[i]
    )
    points.append(point)


# aab humne jo bhi point banaya hai usko hum hamare qdrant me upload karenge

client.upsert( 
    #is se hum upload+insert karte hain
    collection_name=COLLECTION_NAME,
    points=points
)
print(f"uploaded {len(points)} Document to Qdrant")


# ab hum karenge search top 3 results batao 

def search(query,top_k=3):

    # convert this question into an embedding
    query_vector = model.encode(query).tolist()

    # Search qdrant for similar vector
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
        with_payload=True
    )

    return results

# ab hum query filter bhi lagayenge taki filter ho sake chizen

def search_with_filter(query,query_filter=None,top_k=3):

    query_vector = model.encode(query).tolist()

    results = client.querry_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
        with_payload=True,
        query_filter=query_filter
    ).points

    return results

reimbursement_filter = Filter(
    must = [
        FieldCondition(
            key="category",
            match=MatchValue(value="reimbursement")
        )
    ]
)

# PART 9 — TEST SEARCH

query = "How many vacation days do I get?"

results = search_with_filter(query, reimbursement_filter,top_k=3)

print("\nSearch results:")

for result in results:
    print(f"Score: {result.score:.3f}")
    print(result.payload["text"])
    print()



# PART 10 — CONNECT TO GROQ


groq_client = Groq(
    api_key=GROQ_API_KEY
)


# PART 11 — ASK THE LLM


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
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content



# PART 12 — COMPLETE RAG PIPELINE


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