# Week 1, Day 3 - Tokens and Token Management 🎫

## 1. What Does This Code Do?

Ye program **tokens** ka concept sikha raha hai - LLM processing ka fundamental unit.

Simple explanation:
1. Teen alag-alag prompts hain (different lengths)
2. Har prompt ko LLM ko bhejte hain
3. **max_tokens** parameter se output length limit karte hain
4. Token usage track karte hain (input tokens, output tokens, total)
5. **finish_reason** check karte hain (kyun response ruka)

**Real-world use:** Token counting se cost control hota hai aur API limits manage karte hain.

---

## 2. Big Picture Visualization

```
Multiple Prompts
    │
    ├─ Prompt 1: "Hii" (short)
    ├─ Prompt 2: "Explain big bang" (medium)
    └─ Prompt 3: "1000 words essay" (demanding)
    
Each prompt:
    │
    ▼
Convert to tokens
    │
    ▼
Send to LLM (max_tokens=50)
    │
    ▼
LLM generates response (limited to 50 tokens)
    │
    ▼
Track usage:
    ├─ Prompt tokens (input)
    ├─ Completion tokens (output)
    └─ Total tokens
    
    ▼
Print statistics for each prompt
```

---

## 3. Real-Life Analogy

Socho ek **SMS service** hai purane phone pe.

- **Tokens** = Characters in SMS (160 characters = 1 SMS)
- **Prompt** = Your outgoing message
- **Completion** = Response you receive
- **max_tokens=50** = Response limited to 50 characters
- **Usage tracking** = Bill pe kitne SMS use hue
- **finish_reason** = 
  - `"stop"` = Message complete naturally
  - `"length"` = Message cut due to character limit

API calls mein bhi same concept - tokens count hote hain, cost lagta hai, limits hoti hain.

---

## 4. Prerequisites / Concepts Used

Day 1 & 2 ke concepts plus:

1. **Tokens** - Text ka basic unit jo LLM process karta hai
2. **max_tokens** - Output length control parameter
3. **Token counting** - Input aur output tokens track karna
4. **finish_reason** - Response kyun complete hua
5. **For loops** - Multiple items process karna
6. **Usage object** - API response mein token statistics
7. **f-strings** - Python string formatting

---

## 5. What are Tokens?

### Simple Definition:

**Token** = Text ka ek piece jo LLM process karta hai.

Tokens can be:
- Words
- Parts of words
- Punctuation
- Spaces

### Examples:

```
Text: "Hello world"
Tokens: ["Hello", " world"] → 2 tokens

Text: "Hello, world!"
Tokens: ["Hello", ",", " world", "!"] → 4 tokens

Text: "ChatGPT is amazing"
Tokens: ["Chat", "GPT", " is", " amazing"] → 4 tokens

Text: "I'm learning"
Tokens: ["I", "'m", " learning"] → 3 tokens
```

### Why not just count words?

Kyunki LLM words nahi, **tokens** process karta hai.

```
Word count ≠ Token count

"Hello" → 1 word, 1 token
"Unbelievable" → 1 word, 2 tokens ["Un", "believable"]
"COVID-19" → 1 word, 3 tokens ["COVID", "-", "19"]
```

### Token visualization:

```
Sentence: "The quick brown fox jumps"

Tokenization:
["The", " quick", " brown", " fox", " jumps"]
  ↓       ↓        ↓         ↓       ↓
  1       2        3         4       5   → 5 tokens
```

### Important Rule of Thumb:

**English text:**
- 1 token ≈ 4 characters
- 1 token ≈ 0.75 words
- 100 tokens ≈ 75 words

**Hindi/Devanagari text:**
- Tokens count higher (complex Unicode characters)

---

## 6. Imports — Explain Every Import

Same as Day 1 & 2. Refer to previous explanations.

---

## 7. Data Structures

### List: `prompts`

```python
prompts = [prompt, prompt2, prompt3]
```

**Kya hai?**  
Teen different prompts ka collection.

**Why use list?**  
Loop mein ek-ek karke process kar sakte hain instead of copy-paste code.

**Runtime value:**
```python
[
    "Hii",
    "Explain the big bang theory under 100 words",
    "write 1000 words essay on Ai"
]
```

---

## 8. LINE-BY-LINE EXPLANATION

### Lines 1-16: Setup

Same as Day 1 (imports, load_dotenv, API key validation, client creation, model selection).

---

### Lines 19-21: Variables

```python
role = "user"
```

Standard user role.

---

### Lines 23-25: Three Different Prompts

```python
prompt = "Hii"
prompt2 = "Explain the big bang theory under 100 words"
prompt3 = "write 1000 words essay on Ai"
```

**Word-by-word breakdown:**

- `prompt` → Variable 1 (very short)
- `prompt2` → Variable 2 (medium with constraint)
- `prompt3` → Variable 3 (very demanding)

**Complete meaning:**  
Teen alag-alag length aur complexity ke prompts define kar rahe hain.

**Why three different prompts?**  
Token behavior samajhne ke liye:

```
prompt:  "Hii" 
         → Short input, short expected output
         → Few tokens

prompt2: "Explain the big bang theory under 100 words"
         → Medium input, controlled output
         → Moderate tokens
         → Explicit length constraint

prompt3: "write 1000 words essay on Ai"
         → Short input, LONG expected output
         → Demanding (1000 words ≈ 1300+ tokens)
         → Will exceed max_tokens limit
```

---

### Line 28:

```python
prompts = [prompt, prompt2, prompt3]
```

**Complete meaning:**  
Teeno prompts ko ek list mein dalo taki loop mein process kar sakein.

---

### NEW CONCEPT: For Loop

### Lines 30-37:

```python
for prompt in prompts:
    message = {
        "role": role,
        "content": prompt
    }
    messages = [message]
    response = client.chat.completions.create(model=model, messages=messages, max_tokens=50)
    usage = response.usage
    print(f"Prompt: {prompt} --> your tokens:{usage.prompt_tokens} completion tokens:{usage.completion_tokens} total tokens:{usage.total_tokens} finish reason:{response.choices[0].finish_reason}") 
```

Let me break this down step-by-step:

---

### Line 30:

```python
for prompt in prompts:
```

**Word-by-word breakdown:**

- `for` → Loop keyword (repeat karna hai)
- `prompt` → Temporary variable (har iteration mein change hoga)
- `in` → Membership operator
- `prompts` → List jismein se items lene hain
- `:` → Loop body start hone wala hai

**Complete meaning:**  
`prompts` list ke har item ko ek-ek karke process karo. Current item ko `prompt` variable mein store karo.

**How loop works:**

```
Iteration 1:
    prompt = "Hii"
    (execute loop body)

Iteration 2:
    prompt = "Explain the big bang theory under 100 words"
    (execute loop body)

Iteration 3:
    prompt = "write 1000 words essay on Ai"
    (execute loop body)

Loop ends
```

---

### Lines 31-34: (Inside loop - Message creation)

```python
message = {
    "role": role,
    "content": prompt
}
```

**Complete meaning:**  
Current prompt ke liye message dictionary banao.

**Runtime values:**

```
Iteration 1:
message = {
    "role": "user",
    "content": "Hii"
}

Iteration 2:
message = {
    "role": "user",
    "content": "Explain the big bang theory under 100 words"
}

Iteration 3:
message = {
    "role": "user",
    "content": "write 1000 words essay on Ai"
}
```

---

### Line 35:

```python
messages = [message]
```

Message ko list mein dalo (API requirement).

---

### NEW CONCEPT: max_tokens Parameter

### Line 36:

```python
response = client.chat.completions.create(model=model, messages=messages, max_tokens=50)
```

**Word-by-word breakdown:**

Same as before EXCEPT:
- `max_tokens=50` → **New parameter**

**Complete meaning:**  
API call karo, but output ko maximum 50 tokens tak limit kar do.

---

## DEEP DIVE: max_tokens Parameter

### What is max_tokens?

`max_tokens` ek limit hai jo control karti hai ki LLM **kitne tokens** generate kar sakta hai output mein.

### Syntax:

```python
max_tokens=50  # Maximum 50 tokens output
```

### Examples:

#### Example 1: Short prompt, sufficient max_tokens

```python
prompt = "Say hello"
max_tokens = 50

# Output: "Hello! How can I assist you today?"
# Tokens used: ~8 tokens (well within limit)
# finish_reason: "stop" (naturally complete)
```

---

#### Example 2: Long demand, insufficient max_tokens

```python
prompt = "Write 1000 words essay on AI"
max_tokens = 50

# Output: "Artificial Intelligence (AI) is transforming our world at 
# an unprecedented pace. From healthcare to..."
# Tokens used: 50 tokens (hit limit)
# finish_reason: "length" (forcefully cut)
```

---

### Why use max_tokens?

#### Reason 1: **Cost Control**

APIs charge per token. Limit output = save money.

```
Without max_tokens:
    Prompt: "Explain AI"
    Response: 500 tokens (detailed essay)
    Cost: High

With max_tokens=50:
    Prompt: "Explain AI"
    Response: 50 tokens (brief answer)
    Cost: Low
```

---

#### Reason 2: **Prevent Runaway Generation**

LLMs can generate very long outputs.

```
Prompt: "Tell me about history"

Without max_tokens:
    → 2000+ token essay (entire history of humanity!)

With max_tokens=100:
    → 100 token summary (concise)
```

---

#### Reason 3: **API Limits**

Most APIs have per-request token limits.

```
Groq API limits:
- Total tokens (input + output) limit: varies by model
- Rate limits: requests per minute

max_tokens helps stay within limits
```

---

#### Reason 4: **Application Design**

App mein fixed-size outputs chahiye.

```
Use case: Tweet generator
max_tokens = 50  (ensure output fits in UI card)
```

---

### Default value:

Agar `max_tokens` specify nahi karte, default limit hoti hai (model-dependent).

```python
# No max_tokens
response = client.chat.completions.create(model=model, messages=messages)
# Uses API default (often 1024-4096 tokens depending on model)
```

---

### Important Note:

`max_tokens` sirf **output** tokens ko limit karta hai, input tokens ko nahi.

```
Input tokens: Unlimited (within model context limit)
Output tokens: Limited by max_tokens

Total tokens = Input tokens + Output tokens
```

---

### Line 37:

```python
usage = response.usage
```

**Word-by-word breakdown:**

- `usage` → Variable jismein token statistics store hongi
- `=` → Assignment
- `response` → API response object
- `.` → Dot operator
- `usage` → Usage object (part of response)

**Complete meaning:**  
Response object ke andar se usage statistics nikalo aur `usage` variable mein store karo.

**What is usage object?**

`usage` ek object hai jo token statistics contain karta hai:

```python
usage = {
    "prompt_tokens": 5,      # Input mein kitne tokens
    "completion_tokens": 12,  # Output mein kitne tokens
    "total_tokens": 17        # Total (input + output)
}
```

**Structure:**

```
response
    │
    ├── choices (list of responses)
    ├── model (model name)
    ├── created (timestamp)
    └── usage (token statistics)
            │
            ├── prompt_tokens
            ├── completion_tokens
            └── total_tokens
```

---

### NEW CONCEPT: finish_reason

### Line 38:

```python
print(f"Prompt: {prompt} --> your tokens:{usage.prompt_tokens} completion tokens:{usage.completion_tokens} total tokens:{usage.total_tokens} finish reason:{response.choices[0].finish_reason}") 
```

This is a long f-string. Let me break it down:

**Word-by-word breakdown:**

- `print` → Built-in function
- `f"..."` → **F-string** (formatted string literal)
- `{prompt}` → Variable embedding
- `{usage.prompt_tokens}` → Input token count
- `{usage.completion_tokens}` → Output token count
- `{usage.total_tokens}` → Total token count
- `{response.choices[0].finish_reason}` → Why did generation stop

**Complete meaning:**  
Ek detailed line print karo jo bataye:
- Konsa prompt
- Kitne input tokens
- Kitne output tokens
- Total tokens
- Generation kyun ruka

---

## DEEP DIVE: finish_reason

### What is finish_reason?

`finish_reason` batata hai ki LLM ka response **kyun complete hua**.

### Possible values:

#### 1. `"stop"` (Natural completion)

**Meaning:** LLM ne naturally complete response diya.

**Example:**
```python
Prompt: "Say hello"
max_tokens: 50

Response: "Hello! How can I help you?"
finish_reason: "stop"

# LLM felt the response was complete (only 6 tokens used out of 50)
```

---

#### 2. `"length"` (Hit limit)

**Meaning:** Response `max_tokens` limit tak pahunch gaya, but LLM chahta tha aur likhna.

**Example:**
```python
Prompt: "Write 1000 words essay on AI"
max_tokens: 50

Response: "Artificial Intelligence is transforming our world. 
From healthcare to transportation, AI applications are..."
finish_reason: "length"

# LLM wanted to write more, but hit 50 token limit
```

**Visual representation:**

```
LLM wants to generate:
[Token1][Token2][Token3]...[Token48][Token49][Token50][Token51][Token52]...
                                                    ↑
                                            max_tokens limit
                                                    
Output actually generated:
[Token1][Token2][Token3]...[Token48][Token49][Token50]
                                                    ↑
                                            Cut here (finish_reason="length")
```

---

#### 3. `"content_filter"` (Blocked by safety)

**Meaning:** Response inappropriate content contain kar raha tha, API ne block kar diya.

**Example:**
```python
Prompt: "How to hack..."
Response: (blocked)
finish_reason: "content_filter"
```

---

#### 4. `"tool_calls"` (Function calling)

**Meaning:** LLM ne function call kiya (advanced feature, Day 18 mein sikhega).

---

### Why finish_reason matters?

```python
if finish_reason == "length":
    print("Warning: Response was cut short. Increase max_tokens.")
elif finish_reason == "stop":
    print("Response complete.")
```

---

### Lines 40-52: Commented Alternative Loop

```python
# #for i in prompts:
#     message={
#     "role": role,
#     "content": prompt  # BUG HERE
# }
#     messages=[message]
#     response=client.chat.completions.create(model=model,messages=messages,max_tokens=50)
#     usage=response.usage
#     print(f"Prompt: {i} --> your tokens:{usage.prompt_tokens} completion tokens:{usage.completion_tokens} total tokens:{usage.total_tokens} finish reason:{response.choices[0].finish_reason}") 
```

**This is commented code (not executed).**

---

## CRITICAL BUG ANALYSIS:

### Bug in commented code:

**Line 45:**
```python
"content": prompt  # Wrong variable
```

**Problem:**  
Loop variable hai `i`, but message mein `prompt` use kar rahe ho (which is the first prompt's value, not changing).

**Result:**  
Har iteration mein same prompt bhejega ("Hii"), not different ones.

---

### Correct vs Wrong:

**Wrong approach (commented code):**
```python
for i in prompts:
    message = {
        "role": role,
        "content": prompt  # ← Always "Hii"
    }
```

**Iteration trace:**
```
Iteration 1:
    i = "Hii"
    message["content"] = prompt  # "Hii" (correct by accident)

Iteration 2:
    i = "Explain..."
    message["content"] = prompt  # Still "Hii" (WRONG!)

Iteration 3:
    i = "write 1000 words..."
    message["content"] = prompt  # Still "Hii" (WRONG!)
```

---

**Correct approach (active code):**
```python
for prompt in prompts:
    message = {
        "role": role,
        "content": prompt  # ← Changes every iteration
    }
```

**Iteration trace:**
```
Iteration 1:
    prompt = "Hii"
    message["content"] = "Hii" (correct)

Iteration 2:
    prompt = "Explain..."
    message["content"] = "Explain..." (correct)

Iteration 3:
    prompt = "write 1000 words..."
    message["content"] = "write 1000 words..." (correct)
```

---

**Good catch by the developer!** Commented code mein mistake thi, active code mein sahi hai.

---

## 9. COMPLETE EXECUTION TRACE

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SETUP (Lines 1-28)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Imports ✓
load_dotenv() ✓
API key loaded ✓
Client created ✓
Model = "llama-3.3-70b-versatile"

prompts = [
    "Hii",
    "Explain the big bang theory under 100 words",
    "write 1000 words essay on Ai"
]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ITERATION 1: prompt = "Hii"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

message = {
    "role": "user",
    "content": "Hii"
}

messages = [message]

API Call:
    model = "llama-3.3-70b-versatile"
    messages = [{"role": "user", "content": "Hii"}]
    max_tokens = 50

LLM Processing:
    Input: "Hii"
    Input tokens: 1-2 tokens
    
    Generate response: "Hello! How can I assist you today?"
    Output tokens: ~8 tokens
    
    finish_reason: "stop" (response complete, didn't hit limit)

usage:
    prompt_tokens: 2
    completion_tokens: 8
    total_tokens: 10

Print:
Prompt: Hii --> your tokens:2 completion tokens:8 total tokens:10 finish reason:stop

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ITERATION 2: prompt = "Explain the big bang theory under 100 words"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

message = {
    "role": "user",
    "content": "Explain the big bang theory under 100 words"
}

messages = [message]

API Call:
    model = "llama-3.3-70b-versatile"
    messages = [{"role": "user", "content": "Explain..."}]
    max_tokens = 50

LLM Processing:
    Input: "Explain the big bang theory under 100 words"
    Input tokens: ~10 tokens
    
    Generate response: "The Big Bang Theory proposes that 
    the universe began as an infinitely hot, dense point 
    13.8 billion years ago..."
    Output tokens: 50 tokens (hit limit!)
    
    finish_reason: "length" (wanted to write more, but limited)

usage:
    prompt_tokens: 10
    completion_tokens: 50
    total_tokens: 60

Print:
Prompt: Explain the big bang theory under 100 words --> your tokens:10 completion tokens:50 total tokens:60 finish reason:length

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ITERATION 3: prompt = "write 1000 words essay on Ai"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

message = {
    "role": "user",
    "content": "write 1000 words essay on Ai"
}

messages = [message]

API Call:
    model = "llama-3.3-70b-versatile"
    messages = [{"role": "user", "content": "write 1000..."}]
    max_tokens = 50

LLM Processing:
    Input: "write 1000 words essay on Ai"
    Input tokens: ~7 tokens
    
    Generate response: "Artificial Intelligence: Transforming 
    Our World\n\nArtificial Intelligence (AI) has emerged as 
    one of the most..."
    Output tokens: 50 tokens (hit limit!)
    
    finish_reason: "length" (wanted to write 1300+ tokens for 1000 words!)

usage:
    prompt_tokens: 7
    completion_tokens: 50
    total_tokens: 57

Print:
Prompt: write 1000 words essay on Ai --> your tokens:7 completion tokens:50 total tokens:57 finish reason:length

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LOOP ENDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 10. EXPECTED OUTPUT

```
Prompt: Hii --> your tokens:2 completion tokens:8 total tokens:10 finish reason:stop

Prompt: Explain the big bang theory under 100 words --> your tokens:10 completion tokens:50 total tokens:60 finish reason:length

Prompt: write 1000 words essay on Ai --> your tokens:7 completion tokens:50 total tokens:57 finish reason:length
```

---

## 11. Key Observations from Output

### Observation 1: Short prompt, short response

```
Prompt: "Hii"
Tokens: 2 → 8 → 10
finish_reason: "stop"
```

**Analysis:**  
- Input small (2 tokens)
- Output bhi small (8 tokens)
- max_tokens=50 sufficient tha
- Natural completion

---

### Observation 2: Medium prompt, hit limit

```
Prompt: "Explain the big bang theory under 100 words"
Tokens: 10 → 50 → 60
finish_reason: "length"
```

**Analysis:**  
- Input medium (10 tokens)
- Output max limit tak (50 tokens)
- Prompt mein "under 100 words" tha (≈130 tokens)
- But max_tokens=50 ki wajah se response incomplete
- finish_reason="length" indicates truncation

---

### Observation 3: Demanding prompt, hit limit

```
Prompt: "write 1000 words essay on Ai"
Tokens: 7 → 50 → 57
finish_reason: "length"
```

**Analysis:**  
- Input small (7 tokens)
- Output max limit tak (50 tokens)
- Prompt demanded 1000 words (≈1300 tokens)
- But max_tokens=50 only allowed ~37 words
- Massive truncation
- finish_reason="length"

---

### Learning:

**max_tokens should match expected output length:**

```
Short answer expected → max_tokens=50-100
Medium answer → max_tokens=200-500
Long answer → max_tokens=1000-2000
Essay/article → max_tokens=2000-4000
```

---

## 12. Common Beginner Confusions

### Q1: Token kaise count kare manually?

**Answer:**  
Approximate formula:
```
English text: 1 token ≈ 4 characters
"Hello world" (11 chars) ≈ 3 tokens
```

**Exact count:**  
Online tokenizer tools use karo:
- OpenAI Tokenizer: https://platform.openai.com/tokenizer
- Tiktoken library (Python)

---

### Q2: max_tokens input ko bhi limit karta hai kya?

**Answer:**  
**Nahi!** max_tokens sirf **output** ko limit karta hai.

```python
Input: 1000 tokens (allowed)
max_tokens: 50
Output: Maximum 50 tokens
```

**Input limit alag hai:**  
Model ka context window (e.g., 8192 tokens total context).

---

### Q3: finish_reason="length" matlab error hai kya?

**Answer:**  
**Nahi**, error nahi hai. Ye sirf indicate karta hai ki response incomplete ho sakta hai.

**When it's okay:**
```python
# Deliberately limiting output
max_tokens=10  # Want short answer
finish_reason="length"  # Expected
```

**When it's a problem:**
```python
# Expecting complete answer
Prompt: "Write essay"
max_tokens=50  # Too low!
finish_reason="length"  # Problem - increase max_tokens
```

---

### Q4: Total tokens ka cost kaise calculate kare?

**Answer:**  
Cost = (Input tokens × Input price) + (Output tokens × Output price)

**Example (Groq pricing - hypothetical):**
```
Input: $0.0001 per 1K tokens
Output: $0.0002 per 1K tokens

Usage:
prompt_tokens: 100
completion_tokens: 500
total_tokens: 600

Cost:
= (100 × 0.0001/1000) + (500 × 0.0002/1000)
= $0.00001 + $0.0001
= $0.00011 (very cheap!)
```

---

### Q5: Agar max_tokens bahut high set karu to kya hoga?

**Answer:**  
Koi problem nahi, but:

```python
max_tokens=10000  # Very high

Short prompt: "Say hi"
Response: "Hi" (2 tokens)
finish_reason: "stop"

# LLM naturally stops, doesn't force full 10000 tokens
```

**Best practice:**  
Set max_tokens reasonably - expected output size + buffer.

---

### Q6: Kya max_tokens = 0 ho sakta hai?

**Answer:**  
Technically nahi. Minimum usually 1.

```python
max_tokens=0  # Invalid
# Error: max_tokens must be at least 1
```

---

### Q7: Loop mein `i` vs `prompt` variable confusion

**Answer:**  

**Good naming (current code):**
```python
for prompt in prompts:  # Clear: item naam same hai list ke items ka type
    print(prompt)
```

**Confusing naming (commented code):**
```python
for i in prompts:  # Confusing: 'i' suggests index, but it's actually the item
    print(i)
```

**Best practice:**
```python
# Use meaningful names
for prompt in prompts:  # Good
for p in prompts:       # Okay
for i in prompts:       # Confusing (i suggests index)
```

---

### Q8: Kya hum token usage ke basis pe decisions le sakte hain?

**Answer:**  
**Haan!** Absolutely.

**Example:**
```python
response = client.chat.completions.create(...)
usage = response.usage

if usage.total_tokens > 1000:
    print("Warning: High token usage, check your prompt")

if response.choices[0].finish_reason == "length":
    print("Response was cut off. Consider increasing max_tokens.")
```

---

## 13. Common Mistakes / Bugs

### Mistake 1: Variable name mismatch in loop (Commented code bug)

**Already discussed above.** Always use loop variable inside loop body.

---

### Mistake 2: max_tokens too low for task

**Problem:**
```python
prompt = "Write a detailed 500-word essay on AI"
max_tokens = 50  # Way too low!

# Response will be incomplete
finish_reason = "length"
```

**Solution:**
```python
max_tokens = 700  # 500 words ≈ 650 tokens + buffer
```

---

### Mistake 3: Not checking finish_reason

**Problem:**
```python
response = client.chat.completions.create(max_tokens=50, ...)
print(response.choices[0].message.content)
# Prints incomplete answer, user thinks it's complete
```

**Better:**
```python
response = client.chat.completions.create(max_tokens=50, ...)
answer = response.choices[0].message.content

if response.choices[0].finish_reason == "length":
    print("WARNING: Response may be incomplete")
    print(answer)
else:
    print(answer)
```

---

### Mistake 4: Confusing prompt_tokens with total_tokens

**Wrong:**
```python
print(f"Total cost based on {usage.prompt_tokens} tokens")
# Ignoring completion_tokens!
```

**Correct:**
```python
print(f"Total tokens: {usage.total_tokens}")
print(f"Breakdown: {usage.prompt_tokens} input + {usage.completion_tokens} output")
```

---

### Mistake 5: F-string syntax errors

**Common errors:**
```python
# Error 1: Missing 'f'
print("Tokens: {usage.total_tokens}")  # Prints literal string
# Output: "Tokens: {usage.total_tokens}"

# Correct:
print(f"Tokens: {usage.total_tokens}")  # Variable interpolated
# Output: "Tokens: 57"

# Error 2: Wrong quotes
print(f'Tokens: {usage.total_tokens}')  # Works, but mixing quotes can cause issues

# Error 3: Nested quotes conflict
print(f"He said "{hello}"")  # Syntax error
print(f"He said '{hello}'")  # Correct
```

---

## 14. Professional Code Review

### ✅ Good Things:

1. **Practical demonstration** - Multiple prompts show token behavior
2. **Token tracking** - Proper usage monitoring
3. **Loop usage** - DRY principle (Don't Repeat Yourself)
4. **finish_reason tracking** - Aware of response completion status
5. **Clear variable names** - `prompt`, `usage`, etc. are descriptive
6. **Self-correction** - Commented buggy code shows learning process

---

### 🔧 Improvements:

#### 1. **Hardcoded max_tokens insufficient for some prompts**

**Current:**
```python
max_tokens=50  # Too low for prompt3
```

**Better:**
```python
# Adjust per prompt
prompt_configs = [
    {"prompt": "Hii", "max_tokens": 50},
    {"prompt": "Explain...", "max_tokens": 150},
    {"prompt": "write 1000...", "max_tokens": 1400}
]

for config in prompt_configs:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": config["prompt"]}],
        max_tokens=config["max_tokens"]
    )
```

---

#### 2. **Output formatting could be better**

**Current:**
```python
print(f"Prompt: {prompt} --> your tokens:{usage.prompt_tokens}...")
# Long, hard to read
```

**Better:**
```python
print(f"\n{'='*60}")
print(f"Prompt: {prompt[:50]}...")  # Truncate long prompts
print(f"Token Usage:")
print(f"  Input:  {usage.prompt_tokens:>4} tokens")
print(f"  Output: {usage.completion_tokens:>4} tokens")
print(f"  Total:  {usage.total_tokens:>4} tokens")
print(f"Status: {response.choices[0].finish_reason}")
print(f"{'='*60}")
```

**Output example:**
```
============================================================
Prompt: Hii
Token Usage:
  Input:     2 tokens
  Output:    8 tokens
  Total:    10 tokens
Status: stop
============================================================
```

---

#### 3. **No response content printed**

**Current code doesn't print actual answers!**

**Add:**
```python
answer = response.choices[0].message.content
print(f"Response: {answer}\n")
```

---

#### 4. **Add warning for truncated responses**

```python
if response.choices[0].finish_reason == "length":
    print("⚠️  WARNING: Response was truncated. Increase max_tokens.")
```

---

#### 5. **Calculate cost (educational)**

```python
# Hypothetical pricing
INPUT_COST_PER_1K = 0.0001  # $0.0001 per 1K tokens
OUTPUT_COST_PER_1K = 0.0002

cost = (usage.prompt_tokens * INPUT_COST_PER_1K / 1000) + \
       (usage.completion_tokens * OUTPUT_COST_PER_1K / 1000)
       
print(f"Estimated cost: ${cost:.6f}")
```

---

#### 6. **Error handling missing**

```python
try:
    response = client.chat.completions.create(...)
except Exception as e:
    print(f"Error processing prompt '{prompt}': {e}")
    continue  # Skip to next prompt
```

---

## 15. What This Code Teaches You

New concepts from Day 3:

1. ✅ **Tokens** - LLM processing unit
2. ✅ **max_tokens** - Output length control
3. ✅ **Token counting** - Input, output, total tracking
4. ✅ **finish_reason** - Response completion status
5. ✅ **For loops** - Iterating through lists
6. ✅ **Usage object** - API statistics
7. ✅ **F-strings** - String formatting
8. ✅ **Cost awareness** - Token-based pricing understanding

---

## 16. What To Learn Next

Day 3 ke baad:

### Immediate:
1. **JSON mode** - Structured outputs (Day 4)
2. **Pydantic models** - Schema validation
3. **response_format parameter** - Forcing JSON

### Future:
4. **Token optimization** - Reducing token usage
5. **Streaming** - Token-by-token generation
6. **Context window** - Maximum total tokens
7. **Tokenization libraries** - tiktoken, sentencepiece

---

## 17. Advanced Token Concepts (FYI)

### Context Window:

```
Model: llama-3.3-70b-versatile
Context window: ~8000 tokens (example)

Total tokens = Input tokens + Output tokens ≤ Context window

If input = 7000 tokens
Max possible output = 1000 tokens
```

---

### Token Optimization Strategies:

**Strategy 1: Concise prompts**
```python
# Verbose (more tokens)
"Can you please explain to me what artificial intelligence is?"

# Concise (fewer tokens)
"Explain artificial intelligence"
```

**Strategy 2: Abbreviations (when appropriate)**
```python
# More tokens
"Machine Learning, Artificial Intelligence, Natural Language Processing"

# Fewer tokens (if model understands)
"ML, AI, NLP"
```

**Strategy 3: Remove filler words**
```python
# More tokens
"I would like to know about Python programming language"

# Fewer tokens
"Explain Python programming"
```

---

## 18. Final Mental Model

```
Multiple Prompts
    │
    ├─ Loop through each
    │
    └─ For each prompt:
            │
            ├─ Create message
            ├─ Send to LLM (max_tokens=50)
            ├─ Track token usage
            │   ├─ prompt_tokens
            │   ├─ completion_tokens
            │   └─ total_tokens
            ├─ Check finish_reason
            │   ├─ "stop" → Complete
            │   └─ "length" → Truncated
            └─ Print statistics
```

### In one sentence:

**"Ye program multiple prompts ko loop mein process karta hai, har prompt ke liye token usage track karta hai, aur max_tokens=50 limit apply karta hai jisse kuch responses truncate ho jate hain (finish_reason='length')."**

---

## 19. Quick Reference Card

### Token Formulas:
```
English: 1 token ≈ 4 characters ≈ 0.75 words
100 tokens ≈ 75 words

Hindi: 1 token ≈ 2-3 characters (higher token count)
```

### max_tokens Guidelines:
```
Quick answer:     50-100
Paragraph:        100-200
Detailed answer:  200-500
Essay:            500-1500
Article:          1500-3000
```

### finish_reason Values:
```
"stop"           → Natural completion ✓
"length"         → Hit max_tokens limit ⚠️
"content_filter" → Blocked by safety 🚫
"tool_calls"     → Function calling 🔧
```

---

## 20. Debugging Checklist

Token-related issues:

- [ ] Are prompts significantly different lengths?
- [ ] Is max_tokens appropriate for each prompt?
- [ ] Is finish_reason being checked?
- [ ] Are token counts being logged?
- [ ] Is loop variable used correctly in message?
- [ ] Are f-strings formatted correctly?
- [ ] Is cost being monitored (for production)?

---

**Excellent progress! 🎉**  
Tumne tokens, max_tokens, aur token tracking successfully seekh liya!

Next: Day 4 mein **JSON mode aur Pydantic** ka powerful combination sikhega! 🚀
