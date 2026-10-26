# Week 3, Day 11 - Introduction to RAG (Retrieval-Augmented Generation) 🔍

## 1. What Does This Code Do?

Ye program **RAG (Retrieval-Augmented Generation)** ka most basic implementation hai - LLM ko apna **private knowledge base** dena.

**Simple workflow:**
1. Knowledge base define karo (dictionary mein)
2. User question analyze karo
3. Relevant information retrieve karo
4. LLM ko retrieved info provide karo (context)
5. LLM accurate answer de

**Real-world use:** Company policies, product documentation, internal knowledge bases - kuch bhi jo LLM ke training mein nahi tha.

---

## 2. Big Picture Visualization

```
WITHOUT RAG (Traditional LLM):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

User: "What is Harry's age?"
    │
    ▼
LLM (only training data)
    │
    ▼
Response: "I don't have information about Harry"
❌ Cannot answer


WITH RAG (This Code):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

User: "What is Harry's age?"
    │
    ▼
Retrieval Function
    │
    ├─ Search knowledge base
    ├─ Find: "Harry ki age 55 hai"
    └─ Return relevant info
    │
    ▼
LLM (training data + retrieved info)
    │
    ▼
Response: "Harry's age is 55"
✅ Accurate answer!
```

---

## 3. Real-Life Analogy

Socho ek **exam** de rahe ho.

### Without RAG (Closed Book Exam):
```
Question: "What's company policy X?"
Student (LLM): "I don't know, I wasn't trained on this"
❌ Fail
```

### With RAG (Open Book Exam):
```
Question: "What's company policy X?"
    ↓
Student (LLM): "Let me check the policy book..."
    ↓
Finds relevant page
    ↓
Reads: "Policy X states..."
    ↓
Answer: "According to the policy, X means..."
✅ Correct!
```

RAG = Giving LLM access to reference materials!

---

## 4. Prerequisites / Concepts Used

Weeks 1-2 concepts plus:

1. **RAG concept** - Retrieval + Generation
2. **Knowledge base** - Private data storage
3. **Retrieval function** - Finding relevant info
4. **Context injection** - Adding info to prompt
5. **Keyword matching** - Simple search logic
6. **Dictionary as knowledge store** - Key-value pairs
7. **String operations** - `.lower()`, `in` operator
8. **Fallback responses** - Handling not-found cases

---

## 5. What is RAG?

### RAG = Retrieval-Augmented Generation

**Three components:**

#### 1. **Retrieval** 📚
Find relevant information from knowledge base.

#### 2. **Augmented** ➕
Add retrieved info to LLM prompt (augment context).

#### 3. **Generation** 🤖
LLM generates response using retrieved context.

---

### Why RAG Exists

**Problem with LLMs:**

```
LLM Training Data:
    ├─ Public internet (2023 cutoff)
    ├─ Books, Wikipedia
    └─ General knowledge

What LLM DOESN'T know:
    ❌ Your company's private data
    ❌ Recent events (after training)
    ❌ Personalized information
    ❌ Real-time data
    ❌ Proprietary knowledge
```

**Solution: RAG**

```
Your Private Data
    │
    ├─ Company documents
    ├─ Product info
    ├─ User data
    └─ Recent updates
    
    ↓ [Retrieval]
    
Retrieved Context
    │
    ↓ [Augmentation]
    
LLM + Context → Accurate Answer!
```

---

## 6. Code Architecture

### Component 1: Knowledge Base

```python
knowledge_base = {
    "age": "harry ki age 55 hai",
    "class": "harry 12th me padhta hai"
}
```

**Purpose:** Store facts/information.

**Structure:**
- **Key:** Topic/category
- **Value:** Actual information

**Real-world equivalent:**
```python
company_knowledge = {
    "leave_policy": "Employees get 24 days paid leave...",
    "wfh_policy": "Work from home on Monday and Friday...",
    "salary_day": "Salary is credited on last working day..."
}
```

---

### Component 2: Retrieval Function

```python
def retrive_info(question):
    question = question.lower()  # Case-insensitive
    
    if "age" in question:
        return knowledge_base["age"]
    elif "class" in question:
        return knowledge_base["class"]
    else:
        return "no information about this bs"
```

**Purpose:** Find relevant info based on question.

**How it works:**

```
Input: "What is Harry's age?"
    ↓
Convert to lowercase: "what is harry's age?"
    ↓
Check if "age" in question: YES
    ↓
Return: "harry ki age 55 hai"
```

---

### Component 3: LLM Function with Context

```python
def ask_llm(question):
    # STEP 1: Retrieve relevant context
    context = retrive_info(question)
    
    # STEP 2: Create system prompt with context
    sys_prompt = f"""Give answer in one line, and answer only based on this context do not hallucinate {context}"""
    
    system_message = {
        "role": "system",
        "content": sys_prompt
    }
    
    # STEP 3: User message
    user_message = {
        "role": "user",
        "content": question
    }
    
    # STEP 4: Call LLM
    messages = [system_message, user_message]
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    
    # STEP 5: Extract answer
    answer = response.choices[0].message.content
    return answer
```

---

## 7. COMPLETE EXECUTION TRACE

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SETUP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Knowledge Base:
{
    "age": "harry ki age 55 hai",
    "class": "harry 12th me padhta hai"
}

Client: Groq initialized
Model: "openai/gpt-oss-120b"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
USER QUESTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

question = "Do you know code with harry's age"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 1: Call ask_llm()
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ask_llm("Do you know code with harry's age")
    │
    ▼
STEP 1a: Retrieve context
    │
    ├─ Call: retrive_info("Do you know code with harry's age")
    │
    ├─ Inside retrive_info():
    │   │
    │   ├─ question = "Do you know code with harry's age"
    │   ├─ question = question.lower()
    │   ├─ question = "do you know code with harry's age"
    │   │
    │   ├─ Check: if "age" in question
    │   ├─ "age" in "do you know code with harry's age"
    │   ├─ Result: TRUE ✓
    │   │
    │   └─ return knowledge_base["age"]
    │       └─ return "harry ki age 55 hai"
    │
    └─ context = "harry ki age 55 hai"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 2: Create System Prompt with Context
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

sys_prompt = f"""Give answer in one line, and answer only 
based on this context do not hallucinate {context}"""

Substitution:
sys_prompt = """Give answer in one line, and answer only 
based on this context do not hallucinate harry ki age 55 hai"""

system_message = {
    "role": "system",
    "content": "Give answer in one line, and answer only based 
               on this context do not hallucinate harry ki age 55 hai"
}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 3: Create User Message
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

user_message = {
    "role": "user",
    "content": "Do you know code with harry's age"
}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 4: Combine Messages
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

messages = [
    {
        "role": "system",
        "content": "Give answer in one line, and answer only 
                   based on this context do not hallucinate 
                   harry ki age 55 hai"
    },
    {
        "role": "user",
        "content": "Do you know code with harry's age"
    }
]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 5: Call LLM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=messages
)

LLM receives:
    System: "Answer based on this context: harry ki age 55 hai"
    User: "Do you know code with harry's age"

LLM thinks:
    "I have context saying Harry's age is 55"
    "User asking about Harry's age"
    "I should answer: 55"

LLM generates:
    "Harry is 55 years old" or
    "According to the provided context, Harry's age is 55"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 6: Extract Answer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

answer = response.choices[0].message.content
answer = "Harry is 55 years old."

return answer

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 7: Print Result
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

print(ask_llm(question))

Output:
Harry is 55 years old.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
END
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 8. Key Concepts Explained

### Concept 1: Context Injection

**What is it?**

Adding relevant information to the LLM prompt.

**Without context:**
```python
System: "You are a helpful assistant"
User: "What is Harry's age?"

LLM: "I don't have information about Harry"
```

**With context (RAG):**
```python
System: "Answer based on this context: harry ki age 55 hai"
User: "What is Harry's age?"

LLM: "Harry is 55 years old"
```

**Key insight:** LLM doesn't "remember" or "learn" - we give it info in real-time!

---

### Concept 2: Retrieval (Simple Version)

Current code uses **keyword matching**:

```python
if "age" in question:
    return knowledge_base["age"]
```

**Flow:**
```
Question contains "age"
    ↓
Return age-related info
```

**Limitations:**

```
Question: "How old is Harry?"
    ↓
Check: "age" in "How old is Harry?"
    ↓
Result: FALSE (no "age" keyword)
    ↓
Return: "no information" ❌

But we DO have age info! Just phrased differently.
```

**This will be improved in Day 12 with semantic search (embeddings)!**

---

### Concept 3: Hallucination Prevention

```python
sys_prompt = "answer only based on this context do not hallucinate"
```

**What is hallucination?**

LLM making up information that's not in the context.

**Example without instruction:**
```
Context: "Harry ki age 55 hai"
Question: "What is Harry's favorite color?"

Bad LLM: "Harry likes blue"  ← Made up!
```

**With instruction:**
```
Context: "Harry ki age 55 hai"
Question: "What is Harry's favorite color?"

Good LLM: "I don't have information about Harry's favorite color"
```

---

### Concept 4: Fallback Response

```python
else:
    return "no information about this bs"
```

**Purpose:** Handle questions we can't answer.

**Example:**
```
Question: "What is the weather?"
    ↓
Not about "age" or "class"
    ↓
Return: "no information about this bs"
    ↓
LLM: "I don't have information about the weather"
```

---

## 9. Expected Output

### Test Case 1: Age Question

```python
question = "Do you know code with harry's age"
print(ask_llm(question))

Output:
Harry is 55 years old.
```

---

### Test Case 2: Class Question

```python
question = "Which class is Harry in?"
print(ask_llm(question))

Output:
Harry is in 12th class.
```

---

### Test Case 3: Unknown Question

```python
question = "What is Harry's favorite food?"
print(ask_llm(question))

Output:
I don't have information about Harry's favorite food.
```

---

## 10. Limitations of This Approach

### Limitation 1: Keyword-Based Retrieval

**Problem:**

Different phrasings won't work:

```python
✓ "What is Harry's age?"      → "age" found
✓ "Tell me Harry's age"       → "age" found
✗ "How old is Harry?"         → "age" not found ❌
✗ "Harry ki umar kya hai?"    → "age" not found ❌
```

**Solution (Day 12):** Semantic search with embeddings.

---

### Limitation 2: Small Knowledge Base

**Current:**
```python
knowledge_base = {
    "age": "...",
    "class": "..."
}
```

Only 2 facts!

**Real-world needs:**
- 1000s of documents
- Multi-page PDFs
- Dynamic updates

**Solution (Day 14-15):** Vector databases.

---

### Limitation 3: No Context Ranking

**Problem:**

What if multiple topics match?

```python
question = "Tell me about Harry's age and class"

# Both "age" and "class" match!
# Which one to return?
```

**Current code:** Returns first match only.

**Solution (Day 13):** Return multiple contexts, ranked by relevance.

---

### Limitation 4: Hardcoded Logic

```python
if "age" in question:
    return knowledge_base["age"]
elif "class" in question:
    return knowledge_base["class"]
```

**Problem:** Adding new facts requires code changes.

**Solution (Day 12-13):** Dynamic retrieval based on similarity.

---

## 11. Common Beginner Confusions

### Q1: LLM ko training karna hai kya RAG ke liye?

**Answer:**

**NAHI!** LLM ko train nahi karte.

**Misconception:**
```
"I need to retrain LLM on my data"
```

**Reality:**
```
RAG = Give LLM your data at QUERY TIME, not training time

User asks question
    ↓
Retrieve relevant data
    ↓
Pass data to LLM in prompt
    ↓
LLM uses that data
```

No training, no fine-tuning needed!

---

### Q2: Knowledge base mein kitna data daal sakte hain?

**Answer:**

**Limited by context window.**

```
LLM Context Window: ~8000 tokens (example)

Total tokens = System prompt + Retrieved context + User question

If context = 7000 tokens → Very little room for question/answer
```

**Solution:** Don't pass entire knowledge base. Only pass relevant parts (that's the "Retrieval" in RAG).

---

### Q3: RAG vs Fine-tuning mein difference?

**Answer:**

**RAG:**
```
✓ No training needed
✓ Can update knowledge instantly
✓ Cheaper
✓ Works with any LLM
✗ Limited by context window
✗ Slower (retrieval overhead)

Use case: Dynamic data, frequently changing info
```

**Fine-tuning:**
```
✓ Knowledge "baked in" to model
✓ No retrieval needed (faster)
✗ Expensive ($100s-$1000s)
✗ Time-consuming
✗ Hard to update (need retrain)

Use case: Specialized language, domain-specific style
```

---

### Q4: Kya LLM context ko "yaad" rakh leta hai?

**Answer:**

**NAHI!** LLM stateless hai.

```
Call 1:
Context: "Harry's age is 55"
Question: "How old is Harry?"
Answer: "55"

Call 2:
Question: "What did I just ask?"
Answer: "I don't know" ← No memory of call 1!
```

Each API call is independent. For memory, you need conversation history (Week 2 concepts).

---

### Q5: `retrive_info()` function mein typo hai?

**Answer:**

**Haan!** Correct spelling: `retrieve` (with two 'e's).

**Typo:** `retrive_info` → Should be `retrieve_info`

**Impact:** No error, just bad practice. Code still works.

---

## 12. Common Mistakes / Bugs

### Mistake 1: Not converting to lowercase

**Problem:**
```python
question = "What is Harry's AGE?"
if "age" in question:  # ← "age" not in "AGE"
    return ...

Result: Doesn't match! ❌
```

**Solution:** Convert to lowercase first.
```python
question = question.lower()
```

---

### Mistake 2: Forgetting to inject context

**Bad:**
```python
def ask_llm(question):
    # No retrieval!
    messages = [{"role": "user", "content": question}]
    response = client.chat.completions.create(...)
    return response.choices[0].message.content

# LLM has no context → Can't answer
```

**Good:**
```python
def ask_llm(question):
    context = retrive_info(question)  # ← Retrieve first!
    sys_prompt = f"Answer based on: {context}"
    # Then call LLM with context
```

---

### Mistake 3: Vague system prompt

**Bad:**
```python
sys_prompt = "Answer the question"
# LLM might hallucinate
```

**Good:**
```python
sys_prompt = f"Answer ONLY based on this context: {context}. Do not use any other knowledge."
# Clear instruction to use only provided context
```

---

### Mistake 4: No fallback handling

**Problem:**
```python
def retrive_info(question):
    if "age" in question:
        return knowledge_base["age"]
    # What if no match?

Result: Function returns None → Error in f-string
```

**Solution:** Always have fallback.
```python
else:
    return "no information available"
```

---

## 13. Professional Code Review

### ✅ Good Things:

1. **RAG fundamentals** - Retrieval + Context injection
2. **Simple demonstration** - Easy to understand
3. **Fallback handling** - Returns message if no match
4. **Hallucination prevention** - Explicit instruction
5. **Modular design** - Separate retrieval and LLM functions

---

### 🔧 Improvements:

#### 1. **Fix typo**

```python
# Current:
def retrive_info(question):

# Correct:
def retrieve_info(question):
```

---

#### 2. **Better keyword matching**

```python
# Current: Only checks main keywords
if "age" in question:
    return knowledge_base["age"]

# Better: Check synonyms
age_keywords = ["age", "old", "years", "umar"]
if any(keyword in question for keyword in age_keywords):
    return knowledge_base["age"]
```

---

#### 3. **Structured knowledge base**

```python
# Current: Simple dict
knowledge_base = {
    "age": "harry ki age 55 hai",
    "class": "harry 12th me padhta hai"
}

# Better: With metadata
knowledge_base = [
    {
        "topic": "age",
        "keywords": ["age", "old", "years", "umar"],
        "content": "Harry is 55 years old"
    },
    {
        "topic": "class",
        "keywords": ["class", "grade", "standard"],
        "content": "Harry is in 12th grade"
    }
]
```

---

#### 4. **Error handling**

```python
def ask_llm(question):
    try:
        context = retrieve_info(question)
        
        if not context:
            return "I don't have information about that"
        
        # Rest of code...
    except Exception as e:
        return f"Error occurred: {e}"
```

---

#### 5. **Logging**

```python
import logging

def retrieve_info(question):
    logging.info(f"Retrieving info for: {question}")
    
    question = question.lower()
    
    if "age" in question:
        logging.info("Found age information")
        return knowledge_base["age"]
    
    logging.warning("No information found")
    return "no information available"
```

---

## 14. Evolution Path: This Code → Production RAG

### Current (Day 11): Basic RAG

```
Knowledge Base (2 facts, dictionary)
    ↓
Keyword matching
    ↓
Pass context to LLM
```

**Limitations:** Small scale, keyword-based, hardcoded.

---

### Day 12: Embeddings

```
Knowledge Base (still small)
    ↓
Convert to embeddings (vectors)
    ↓
Semantic similarity search
    ↓
Pass context to LLM
```

**Improvement:** Understands meaning, not just keywords!

---

### Day 13: Full RAG

```
Multiple documents
    ↓
Embeddings
    ↓
Similarity search (retrieve top-k)
    ↓
Pass multiple contexts to LLM
```

**Improvement:** Handle more data, better retrieval.

---

### Day 14-15: Vector Database

```
1000s of documents
    ↓
Store in vector DB (Qdrant)
    ↓
Fast similarity search
    ↓
Retrieve top-k relevant docs
    ↓
Pass to LLM
```

**Improvement:** Production-scale, fast, persistent storage.

---

## 15. Real-World RAG Applications

### Application 1: Customer Support Bot

```python
knowledge_base = {
    "shipping": "Orders ship within 2-3 business days",
    "returns": "30-day return policy, no questions asked",
    "warranty": "1-year warranty on all electronics"
}

User: "How long does shipping take?"
    ↓
Retrieve: "Orders ship within 2-3 business days"
    ↓
LLM: "Your order will ship within 2-3 business days"
```

---

### Application 2: Company Policy Assistant

```python
knowledge_base = {
    "leave": "24 days paid leave per year",
    "wfh": "Work from home Monday and Friday",
    "hours": "Flexible hours, core time 10 AM - 4 PM"
}

Employee: "Can I work from home?"
    ↓
Retrieve: "Work from home Monday and Friday"
    ↓
LLM: "Yes, you can work from home on Mondays and Fridays"
```

---

### Application 3: Product Documentation

```python
knowledge_base = {
    "installation": "Run: pip install package",
    "usage": "Import: from package import main",
    "config": "Configure in config.yaml file"
}

Developer: "How do I install?"
    ↓
Retrieve: "Run: pip install package"
    ↓
LLM: "Install using: pip install package"
```

---

## 16. What This Code Teaches You

Concepts from Day 11:

1. ✅ **RAG fundamentals** - Retrieval-Augmented Generation
2. ✅ **Knowledge base** - Storing private data
3. ✅ **Retrieval function** - Finding relevant info
4. ✅ **Context injection** - Augmenting prompts
5. ✅ **Hallucination prevention** - Using only provided context
6. ✅ **Fallback handling** - Graceful degradation
7. ✅ **Keyword matching** - Simple retrieval logic
8. ✅ **System prompts** - Guiding LLM behavior

---

## 17. What To Learn Next

Day 11 ke baad:

### Immediate (Day 12):
1. **Embeddings** - Vector representations of text
2. **Semantic similarity** - Meaning-based matching
3. **Cosine similarity** - Measuring text similarity

### Future (Day 13-15):
4. **Full RAG pipeline** - End-to-end system
5. **Vector databases** - Scalable storage
6. **Advanced retrieval** - Top-k, filtering, reranking

---

## 18. Final Mental Model

```
Traditional LLM:
    Question → LLM → Answer (limited to training data)

RAG System:
    Question 
        ↓
    Retrieve relevant info from knowledge base
        ↓
    Context + Question → LLM → Accurate answer!
    
Key insight: Give LLM access to your data at query time,
not training time. No retraining needed!
```

### In one sentence:

**"Ye program RAG ka basic implementation hai jahan user question ke basis pe relevant information knowledge base se retrieve ki jati hai, phir us context ko LLM ko provide kiya jata hai taki wo accurate answer de sake - even if that info wasn't in LLM's training data."**

---

**Foundation laid! 🎉**  

This simple RAG pattern is the core of:
- ChatGPT with file uploads
- Notion AI
- Customer support bots
- Enterprise AI assistants

Next: Day 12 will upgrade this to **semantic search** using embeddings - game changer! 🚀
