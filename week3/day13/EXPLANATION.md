# Week 3, Day 13 - Complete RAG System with Embeddings 🔗

## 1. What Does This Code Do?

Ye program **production-grade RAG system** hai jo embeddings use karke semantic search implement karta hai.

**Complete workflow:**
1. **Documents** define karo (company knowledge base)
2. **Embeddings** generate karo har document ke liye
3. **User question** ko embedding mein convert karo
4. **Cosine similarity** se most relevant document find karo
5. **LLM** ko relevant context provide karo
6. **Accurate answer** generate karo

**Real-world use:** Enterprise search, Q&A systems, customer support, documentation assistants.

---

## 2. Big Picture Visualization

```
KNOWLEDGE BASE (Documents):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Doc 1: "Employees receive 24 days of paid leave..."
Doc 2: "Work from office on Tuesday, Wednesday, Thursday..."
Doc 3: "Rs 3000 per month for gym reimbursement..."
Doc 4: "Rs 2000 per month for home internet..."
Doc 5: "90 day notice period..."

    ↓ [Convert to embeddings]

VECTOR DATABASE (In-memory):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Embedding 1: [0.23, -0.89, 0.45, ...]
Embedding 2: [0.12, 0.56, -0.34, ...]
Embedding 3: [-0.45, 0.23, 0.67, ...]
Embedding 4: [0.34, -0.12, 0.89, ...]
Embedding 5: [0.56, 0.78, -0.23, ...]


USER QUERY:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"How much vacation do I get?"

    ↓ [Convert to embedding]

Query Embedding: [0.25, -0.87, 0.42, ...]

    ↓ [Calculate similarity with all docs]

Similarities:
├─ Doc 1: 0.91 ← Highest! ✓
├─ Doc 2: 0.23
├─ Doc 3: 0.15
├─ Doc 4: 0.18
└─ Doc 5: 0.12

    ↓ [Retrieve Doc 1]

Context: "Employees receive 24 days of paid leave..."

    ↓ [Pass to LLM]

LLM Answer: "You get 24 days of paid leave per year."
```

---

## 3. Real-Life Analogy

Socho ek **library** hai with a smart librarian.

### Old System (Keyword Search):

```
You: "Book about vacation policy"
Librarian: Searches for books with "vacation" in title
Finds: Nothing (books titled "Leave Policy", "Time Off")
Result: No results ❌
```

---

### New System (Semantic Search with RAG):

```
You: "Book about vacation policy"

Librarian (Embedding System):
    ├─ Understands you want: time off, leave, holidays
    ├─ Knows "vacation" = "leave" = "paid time off"
    ├─ Finds book: "Employee Leave Policy"
    ├─ Reads relevant section
    └─ Summarizes: "You get 24 days paid leave"

Result: Perfect answer! ✓
```

RAG with embeddings = Librarian who understands meaning, not just words!

---

## 4. Prerequisites / Concepts Used

Days 11-12 concepts plus:

1. **Multiple documents** - Knowledge base with several items
2. **Document embeddings** - Vectorizing entire corpus
3. **Query embedding** - Vectorizing user question
4. **Batch similarity** - Comparing query with all docs
5. **Argmax/ranking** - Finding best match
6. **Context injection** - Passing retrieved doc to LLM
7. **Enumerate** - Tracking index and value
8. **List comprehension** - Efficient iteration
9. **Tuple unpacking** - (score, document) pairs

---

## 5. Code Architecture

### Component 1: Knowledge Base (Documents)

```python
documents = [
    "Employees receive 24 days of paid leave per year.",
    
    "Employees work from the office on Tuesday, Wednesday and Thursday. "
    "Monday and Friday are optional work-from-home days.",
    
    "Employees receive Rs 3000 per month for gym reimbursement.",
    
    "Employees can claim Rs 2000 per month for home internet.",
    
    "Employees have a 90 day notice period."
]
```

**Structure:** List of strings, each representing a knowledge item.

**Real-world equivalent:**
```python
# From company handbook, product docs, FAQs, etc.
documents = [
    "Policy 1...",
    "Policy 2...",
    "Product feature 1...",
    "FAQ answer 1...",
    # ... 1000s of items
]
```

---

### Component 2: Embedding Model

```python
model = SentenceTransformer("all-MiniLM-L6-v2")
```

Same as Day 12 - converts text to 384-dimensional vectors.

---

### Component 3: Document Embeddings

```python
document_embeddings = model.encode(documents)
```

**What happens:**

```
Input (list of 5 strings):
    documents = [doc1, doc2, doc3, doc4, doc5]

    ↓ [Batch encoding]

Output (2D numpy array):
    document_embeddings = [
        [0.23, -0.89, 0.45, ...],  # doc1 embedding (384 dims)
        [0.12, 0.56, -0.34, ...],  # doc2 embedding
        [-0.45, 0.23, 0.67, ...],  # doc3 embedding
        [0.34, -0.12, 0.89, ...],  # doc4 embedding
        [0.56, 0.78, -0.23, ...]   # doc5 embedding
    ]

Shape: (5, 384)
    ├─ 5 documents
    └─ 384 dimensions each
```

---

### Component 4: Cosine Similarity Function

```python
def cosice_sim(a, b):
    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )
```

Same as Day 12 - measures vector similarity.

---

### Component 5: Retrieval Function

```python
def retrive(qembeding):
    scores = []
    
    # Compare query with each document
    for i, document in enumerate(document_embeddings):
        score = cosice_sim(qembeding, document)
        scores.append((score, documents[i]))
    
    # Sort by score (highest first)
    scores.sort(reverse=True)
    
    # Return best match
    return scores[0]
```

---

## DEEP DIVE: Retrieval Function

### Line-by-line Breakdown:

#### Line 1: Initialize scores list

```python
scores = []
```

Will store `(similarity_score, document_text)` tuples.

---

#### Line 2: Loop through document embeddings

```python
for i, document in enumerate(document_embeddings):
```

**What is enumerate?**

Gives both index and value.

**Example:**
```python
items = ['a', 'b', 'c']

for i, item in enumerate(items):
    print(i, item)

Output:
0 a
1 b
2 c
```

**In our code:**
```
i = 0, document = embedding of doc 1
i = 1, document = embedding of doc 2
i = 2, document = embedding of doc 3
i = 3, document = embedding of doc 4
i = 4, document = embedding of doc 5
```

---

#### Line 3: Calculate similarity

```python
score = cosice_sim(qembeding, document)
```

**Comparison:**
```
query_embedding: [0.25, -0.87, 0.42, ..., 0.56]
document_embedding: [0.23, -0.89, 0.45, ..., 0.54]
    ↓
cosine_sim(...) = 0.91
```

---

#### Line 4: Store score with document text

```python
scores.append((score, documents[i]))
```

**Why `documents[i]` not `document`?**

- `document` = embedding (numbers)
- `documents[i]` = original text

**Tuple structure:**
```python
(0.91, "Employees receive 24 days of paid leave per year.")
```

**After loop, scores looks like:**
```python
scores = [
    (0.91, "Employees receive 24 days..."),
    (0.23, "Employees work from office..."),
    (0.15, "Employees receive Rs 3000..."),
    (0.18, "Employees can claim Rs 2000..."),
    (0.12, "Employees have a 90 day...")
]
```

---

#### Line 5: Sort by score

```python
scores.sort(reverse=True)
```

**Before sort:**
```python
[
    (0.91, "doc1"),
    (0.23, "doc2"),
    (0.15, "doc3"),
    (0.18, "doc4"),
    (0.12, "doc5")
]
```

**After sort (reverse=True for descending):**
```python
[
    (0.91, "doc1"),  # Highest
    (0.23, "doc2"),
    (0.18, "doc4"),
    (0.15, "doc3"),
    (0.12, "doc5")   # Lowest
]
```

---

#### Line 6: Return best match

```python
return scores[0]
```

Returns tuple: `(0.91, "Employees receive 24 days of paid leave per year.")`

---

### Component 6: LLM Query Function

```python
def ask_llm(question, context):
    sys_prompt = f"""answer in one line only. Answer only based on this context. do not hallucinate. Context: {context}"""
    
    system_message = {
        "role": "system",
        "content": sys_prompt
    }
    
    message = {
        "role": "user",
        "content": question
    }
    
    messages = [system_message, message]
    
    response = client.chat.completions.create(
        model=groqmodel,
        messages=messages
    )
    
    answer = response.choices[0].message.content
    return answer
```

Standard LLM call with context injection (Day 11 concept).

---

## 6. COMPLETE EXECUTION TRACE

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SETUP: Load Model & Documents
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

model = SentenceTransformer("all-MiniLM-L6-v2")
Model loaded: ✓

documents = [
    "Employees receive 24 days of paid leave per year.",
    "Employees work from the office on Tuesday, Wednesday...",
    "Employees receive Rs 3000 per month for gym...",
    "Employees can claim Rs 2000 per month for internet...",
    "Employees have a 90 day notice period."
]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 1: Generate Document Embeddings
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

document_embeddings = model.encode(documents)

Processing each document:

Doc 1: "Employees receive 24 days..."
    → Embedding: [0.0234, -0.0891, 0.0456, ..., 0.0789]

Doc 2: "Employees work from office..."
    → Embedding: [0.0123, 0.0567, -0.0234, ..., 0.0456]

Doc 3: "Employees receive Rs 3000..."
    → Embedding: [-0.0456, 0.0234, 0.0678, ..., 0.0123]

Doc 4: "Employees can claim Rs 2000..."
    → Embedding: [0.0345, -0.0123, 0.0890, ..., 0.0234]

Doc 5: "Employees have a 90 day..."
    → Embedding: [0.0567, 0.0789, -0.0234, ..., 0.0567]

Result:
    document_embeddings.shape = (5, 384)
    5 documents × 384 dimensions each

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 2: User Query
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

query = "how much vacation do i get?"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 3: Generate Query Embedding
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

qembeding = model.encode(query)

Process:
    "how much vacation do i get?"
        ↓
    Tokenize: ["how", "much", "vacation", "do", "i", "get"]
        ↓
    Neural network processing
        ↓
    qembeding = [0.0245, -0.0876, 0.0423, ..., 0.0756]
    
Shape: (384,)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 4: Retrieve Relevant Document
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

score, context = retrive(qembeding)

Inside retrive():

    scores = []
    
    ─────────────────────────────────────────────
    Iteration 1: Doc 0
    ─────────────────────────────────────────────
    i = 0
    document = document_embeddings[0]
    
    score = cosice_sim(qembeding, document)
    Calculation:
        qembeding: [0.0245, -0.0876, ..., 0.0756]
        document:  [0.0234, -0.0891, ..., 0.0789]
        ↓
        cosine_sim = 0.91 ← High! (vacation/leave match)
    
    scores.append((0.91, documents[0]))
    
    ─────────────────────────────────────────────
    Iteration 2: Doc 1
    ─────────────────────────────────────────────
    i = 1
    document = document_embeddings[1]
    
    score = cosice_sim(qembeding, document)
        = 0.23 ← Low (work schedule, not vacation)
    
    scores.append((0.23, documents[1]))
    
    ─────────────────────────────────────────────
    Iteration 3: Doc 2
    ─────────────────────────────────────────────
    i = 2
    score = cosice_sim(qembeding, document_embeddings[2])
        = 0.15 ← Low (gym reimbursement, not vacation)
    
    scores.append((0.15, documents[2]))
    
    ─────────────────────────────────────────────
    Iteration 4: Doc 3
    ─────────────────────────────────────────────
    i = 3
    score = 0.18 ← Low (internet, not vacation)
    
    scores.append((0.18, documents[3]))
    
    ─────────────────────────────────────────────
    Iteration 5: Doc 4
    ─────────────────────────────────────────────
    i = 4
    score = 0.12 ← Low (notice period, not vacation)
    
    scores.append((0.12, documents[4]))
    
    ─────────────────────────────────────────────
    After Loop: scores list
    ─────────────────────────────────────────────
    scores = [
        (0.91, "Employees receive 24 days..."),
        (0.23, "Employees work from office..."),
        (0.15, "Employees receive Rs 3000..."),
        (0.18, "Employees can claim Rs 2000..."),
        (0.12, "Employees have a 90 day...")
    ]
    
    ─────────────────────────────────────────────
    Sort by score (descending)
    ─────────────────────────────────────────────
    scores.sort(reverse=True)
    
    scores = [
        (0.91, "Employees receive 24 days..."),  ← Best!
        (0.23, "Employees work from office..."),
        (0.18, "Employees can claim Rs 2000..."),
        (0.15, "Employees receive Rs 3000..."),
        (0.12, "Employees have a 90 day...")
    ]
    
    ─────────────────────────────────────────────
    Return best match
    ─────────────────────────────────────────────
    return scores[0]
    
    Returns:
        (0.91, "Employees receive 24 days of paid leave per year.")

Back in main code:

score = 0.91
context = "Employees receive 24 days of paid leave per year."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 5: Generate Answer with LLM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

answer = ask_llm(query, context)

Inside ask_llm():

    question = "how much vacation do i get?"
    context = "Employees receive 24 days of paid leave per year."
    
    sys_prompt = """answer in one line only. Answer only 
    based on this context. do not hallucinate. 
    Context: Employees receive 24 days of paid leave per year."""
    
    messages = [
        {
            "role": "system",
            "content": sys_prompt
        },
        {
            "role": "user",
            "content": "how much vacation do i get?"
        }
    ]
    
    LLM Call:
        Input: System + User messages
        Model: openai/gpt-oss-120b
        
    LLM Processing:
        "User asking about vacation"
        "Context says: 24 days paid leave"
        "Answer: 24 days"
    
    Response:
        "You get 24 days of paid leave per year."

answer = "You get 24 days of paid leave per year."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 6: Print Result
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

print(answer)

Output:
You get 24 days of paid leave per year.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
END
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Expected Output

```
You get 24 days of paid leave per year.
```

---

## 8. Why This Works So Well

### Query Analysis:

```
User: "how much vacation do i get?"

Key terms:
- "vacation" → Similar to "paid leave"
- "how much" → Asking for quantity
- "get" → Receiving/entitled to

Semantic understanding:
    User wants to know: Paid time off entitlement
```

---

### Document 1 (Best Match):

```
"Employees receive 24 days of paid leave per year."

Key terms:
- "paid leave" → Semantically equivalent to "vacation"
- "24 days" → Quantity answer
- "receive" → Similar to "get"

Match Score: 0.91 (91% similar!)
```

---

### Why Other Documents Scored Low:

```
Doc 2: "Work from office on Tuesday..."
    - About work schedule, not time off
    - Score: 0.23

Doc 3: "Rs 3000 for gym..."
    - About reimbursement, not vacation
    - Score: 0.15

Doc 4: "Rs 2000 for internet..."
    - About expense claims, not vacation
    - Score: 0.18

Doc 5: "90 day notice period"
    - About resignation, not vacation
    - Score: 0.12
```

---

## 9. Advantages Over Day 11

### Day 11 (Keyword Matching):

```python
if "vacation" in question:
    return vacation_info
elif "leave" in question:
    return vacation_info
# Need to hardcode every synonym!
```

**Problems:**
- ❌ Manual synonym handling
- ❌ Doesn't understand context
- ❌ Brittle (breaks with paraphrasing)

---

### Day 13 (Semantic Search):

```python
# Automatically handles:
✓ "vacation" = "leave" = "time off" = "holidays"
✓ "how much" = "how many" = "what's the amount"
✓ "get" = "receive" = "entitled to"

# No manual rules needed!
```

**Benefits:**
- ✅ Understands meaning
- ✅ Handles synonyms automatically
- ✅ Robust to paraphrasing

---

## 10. Common Beginner Confusions

### Q1: Har document ke liye embedding store karna padta hai?

**Answer:**

**Haan!** But only once (offline).

**Workflow:**
```
One-time setup (offline):
    documents → embeddings → store

Runtime (for each query):
    query → embedding → compare with stored embeddings
```

In production, document embeddings stored in vector database.

---

### Q2: Query embedding bhi store hota hai?

**Answer:**

**Nahi!** Query embedding har baar fresh generate hota hai.

```
User query 1: "vacation days?"
    → Generate embedding → Search → Discard

User query 2: "how many leaves?"
    → Generate new embedding → Search → Discard
```

---

### Q3: Top-1 hi return karte hain, top-5 kyun nahi?

**Answer:**

**Current code:** Top-1 only

**Better approach (top-k):**
```python
def retrieve_top_k(qembeding, k=3):
    scores = []
    for i, document in enumerate(document_embeddings):
        score = cosice_sim(qembeding, document)
        scores.append((score, documents[i]))
    
    scores.sort(reverse=True)
    return scores[:k]  # Return top-k, not just [0]

# Usage:
top_3 = retrieve_top_k(qembeding, k=3)
context = "\n".join([doc for score, doc in top_3])
```

This gives LLM more context!

---

### Q4: Embeddings update kaise kare?

**Answer:**

**New documents add karne par:**

```python
# Option 1: Regenerate all (simple, slow)
documents.append("New policy: ...")
document_embeddings = model.encode(documents)

# Option 2: Append only new (efficient)
new_doc = "New policy: ..."
new_embedding = model.encode([new_doc])
document_embeddings = np.vstack([document_embeddings, new_embedding])
documents.append(new_doc)
```

---

### Q5: Kya LLM embeddings generate kar sakta hai?

**Answer:**

**Nahi!** LLM (GPT, Llama) aur embedding models different hain.

```
LLM (Groq/OpenAI):
    Purpose: Text generation
    Input: Prompt
    Output: Text

Embedding Model (SentenceTransformer):
    Purpose: Convert text to vectors
    Input: Text
    Output: Vector (numbers)
```

Both are neural networks, but different architectures and purposes.

---

### Q6: Similarity threshold set karna chahiye?

**Answer:**

**Haan! Good practice.**

```python
def retrieve(qembeding, threshold=0.5):
    scores = []
    for i, document in enumerate(document_embeddings):
        score = cosice_sim(qembeding, document)
        if score > threshold:  # Only if above threshold
            scores.append((score, documents[i]))
    
    if not scores:
        return (0, "No relevant information found")
    
    scores.sort(reverse=True)
    return scores[0]
```

Prevents returning irrelevant documents with low scores.

---

## 11. Common Mistakes / Bugs

### Mistake 1: Typo in variable name

**Current code:**
```python
def retrive(qembeding):  # Typos in both!
```

**Correct:**
```python
def retrieve(query_embedding):
```

---

### Mistake 2: Not handling empty documents

**Problem:**
```python
documents = []
document_embeddings = model.encode(documents)
# Returns empty array

# Later:
for i, document in enumerate(document_embeddings):
    # Never executes!
```

**Solution:** Validate documents list not empty.

---

### Mistake 3: Recomputing document embeddings on every query

**Inefficient:**
```python
def search(query):
    document_embeddings = model.encode(documents)  # ❌ Recomputing!
    qembeding = model.encode(query)
    # ... search
```

**Efficient:**
```python
# One-time (at startup)
document_embeddings = model.encode(documents)

def search(query):
    qembeding = model.encode(query)
    # ... search using pre-computed document_embeddings
```

---

### Mistake 4: Wrong return format

**Problem:**
```python
return scores[0]  # Returns tuple: (score, document)

# Usage:
context = retrieve(qembeding)
# context is tuple, not string!
```

**Solution:** Unpack properly.
```python
score, context = retrieve(qembeding)
```

---

## 12. Professional Code Review

### ✅ Good Things:

1. **Semantic search** - Embeddings-based retrieval
2. **Batch encoding** - Efficient document processing
3. **Cosine similarity** - Proper similarity metric
4. **Sorted results** - Best match first
5. **Context injection** - RAG implementation

---

### 🔧 Improvements:

#### 1. **Fix typos**

```python
def retrieve(query_embedding):  # Not "retrive(qembeding)"
```

---

#### 2. **Top-k retrieval**

```python
def retrieve(query_embedding, k=3):
    # Return top-k documents, not just best
    scores.sort(reverse=True)
    return scores[:k]
```

---

#### 3. **Threshold filtering**

```python
MIN_SIMILARITY = 0.5

def retrieve(query_embedding):
    # ... similarity calculation
    if score > MIN_SIMILARITY:
        scores.append((score, documents[i]))
```

---

#### 4. **Better return type**

```python
from dataclasses import dataclass

@dataclass
class RetrievalResult:
    score: float
    document: str
    index: int

def retrieve(query_embedding):
    # ... calculation
    return RetrievalResult(score=0.91, document="...", index=0)
```

---

#### 5. **Add logging**

```python
import logging

def retrieve(query_embedding):
    logging.info("Searching through %d documents", len(documents))
    
    # ... search
    
    logging.info("Best match: score=%.3f, doc=%s", score, context[:50])
```

---

#### 6. **Caching query embeddings (optional)**

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_query_embedding(query):
    return model.encode(query)

# Usage:
qembeding = get_query_embedding(query)
```

---

## 13. What This Code Teaches You

Concepts from Day 13:

1. ✅ **Complete RAG pipeline** - End-to-end system
2. ✅ **Document corpus** - Multiple knowledge items
3. ✅ **Batch encoding** - Efficient embedding generation
4. ✅ **Semantic retrieval** - Meaning-based search
5. ✅ **Similarity ranking** - Scoring and sorting
6. ✅ **Tuple unpacking** - (score, document) pairs
7. ✅ **Enumerate usage** - Index + value iteration
8. ✅ **Production patterns** - Reusable components

---

## 14. What To Learn Next

Day 13 ke baad:

### Immediate (Day 14):
1. **Vector database** - Scalable storage (Qdrant)
2. **Persistent storage** - Disk-based embeddings
3. **Fast search** - Optimized similarity search

### Future (Day 15):
4. **Advanced filtering** - Metadata-based queries
5. **Hybrid search** - Combining filters with similarity
6. **Production deployment** - Cloud-based vector DBs

---

## 15. Final Mental Model

```
Documents (Knowledge Base)
    │
    ↓ [Encode once, offline]
    
Document Embeddings (Stored)
    │
User Query
    │
    ↓ [Encode at runtime]
    
Query Embedding
    │
    ↓ [Compare with all docs]
    
Similarity Scores
    │
    ↓ [Rank and select best]
    
Most Relevant Document (Context)
    │
    ↓ [Pass to LLM]
    
LLM with Context
    │
    ↓ [Generate]
    
Accurate Answer!

Key: Semantic understanding > Keyword matching
```

### In one sentence:

**"Ye program complete RAG system implement karta hai jahan sab documents ko pehle embeddings mein convert kiya jata hai, phir user query ke embedding se cosine similarity calculate karke sabse relevant document retrieve kiya jata hai, aur finally LLM ko us context ke saath answer generate karne ke liye diya jata hai."**

---

**Major milestone! 🎉**  

You now have a production-ready RAG system!

This exact pattern powers:
- ChatGPT file uploads
- GitHub Copilot
- Notion AI
- Every enterprise AI assistant

Next: Day 14 will add **Qdrant vector database** for scalability! 🚀
