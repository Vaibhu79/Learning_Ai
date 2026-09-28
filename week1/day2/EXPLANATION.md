# Week 1, Day 2 - System Prompts & Temperature Parameter 🎭

## 1. What Does This Code Do?

Ye program **system prompts** aur **temperature** ka concept sikha raha hai.

Simple explanation:
1. LLM ko ek **role** diya jata hai (system prompt se)
2. User ek question puchta hai
3. Temperature parameter se output ki **creativity** control karte hain
4. LLM us role ke according answer deta hai

**Example:** Hum LLM ko "brand manager" ban ne ko kaha, aur usne food brand ka naam suggest kiya.

---

## 2. Big Picture Visualization

```
System Message
   │
   │ ("You are a brand manager")
   ▼
LLM gets personality/role
   │
   ▼
User Message
   │
   │ ("suggest a name for my food brand")
   ▼
LLM thinks as a brand manager
   │
   ▼
Temperature = 2 (high creativity)
   │
   ▼
Creative brand name generated
   │
   ▼
Output
```

---

## 3. Real-Life Analogy

Socho ek **actor** hai.

- **System prompt** = Director giving character brief ("Tum ek brand manager ho")
- **User prompt** = Scene ka dialogue ("Food brand ka naam suggest karo")
- **Temperature** = Acting style
  - Low temperature (0.0) = Robotic, predictable acting
  - High temperature (2.0) = Creative, unpredictable, experimental acting
- **Output** = Actor ka final performance

---

## 4. Prerequisites / Concepts Used

Day 1 ke saare concepts plus:

1. **System role** - LLM ko personality dena
2. **Message ordering** - System message pehle, user message baad mein
3. **Temperature parameter** - Creativity control
4. **Multiple dictionaries** - System aur user messages alag-alag

---

## 5. Imports — Explain Every Import

Same as Day 1. Refer to Day 1's EXPLANATION.md for detailed import explanations.

Quick summary:
- `os` → Environment variables
- `Path` → File operations (unused)
- `load_dotenv` → Load .env file
- `Groq` → LLM client

---

## 6. Code Setup / Configuration

Same as Day 1:
```
.env file → load_dotenv() → os.getenv() → Groq client → Ready
```

---

## 7. Data Structures

### New Dictionary 1: `message_system`

```python
message_system = {
    "role": "system",
    "content": "You are a brand manager"
}
```

**Kya hai?**  
Ye dictionary LLM ko ek **role/personality** assign karti hai.

**Role types:**
- `"system"` → LLM ko instructions/personality
- `"user"` → Human ka message
- `"assistant"` → LLM ka previous response

**Why "system"?**  
System messages LLM ko guide karte hain ki wo kaise behave kare throughout the conversation.

---

### Dictionary 2: `message` (user message)

```python
message = {
    "role": role,  # "user"
    "content": prompt  # "suggest a name..."
}
```

Same as Day 1.

---

### List: `messages` (with order)

```python
messages = [message_system, message]
```

**Important:** Order matters!

```
Correct order:
[
    System message (instructions),  ← Pehle
    User message (question)         ← Baad mein
]
```

**Why this order?**  
System message pehle dena chahiye taki LLM samajh jaye ki uski kya role hai, phir user message process kare.

---

## 8. LINE-BY-LINE EXPLANATION

### Lines 1-13: Setup

Same as Day 1 (imports, load_dotenv, API key, client, model).

---

### Line 16-18: Role and prompt

```python
role = "user"
prompt = "suggest a name for my food brand only 1"
```

**Note:** `role` variable sirf user message ke liye hai, not for system.

---

### NEW CONCEPT: System Message

### Lines 20-23:

```python
message_system = {
    "role": "system",
    "content": "You are a brand manager"
}
```

**Word-by-word breakdown:**

- `message_system` → Variable naam (clearly shows ye system message hai)
- `=` → Assignment
- `{` → Dictionary start
- `"role": "system"` → Ye ek system-level instruction hai
- `"content": "You are a brand manager"` → LLM ki personality/role

**Complete meaning:**  
LLM ko bol rahe hain: "Tum ek brand manager ho. Is role ke according sochna aur answer dena."

**Internally kya hota hai:**

```
LLM reads system message
    ↓
Sets internal "personality mode"
    ↓
"I am a brand manager"
    ↓
All future responses will reflect this role
```

**Examples of different system prompts:**

```python
# Example 1: Technical expert
"You are a senior Python developer with 10 years of experience."

# Example 2: Friendly teacher
"You are a friendly teacher who explains concepts simply."

# Example 3: Strict reviewer
"You are a code reviewer who focuses on finding bugs and security issues."
```

---

### Lines 26-29: User message

```python
message = {
    "role": role,
    "content": prompt
}
```

Same as Day 1.

**Runtime value:**
```python
{
    "role": "user",
    "content": "suggest a name for my food brand only 1"
}
```

---

### Line 32:

```python
messages = [message_system, message]
```

**Word-by-word breakdown:**

- `messages` → List variable
- `=` → Assignment
- `[` → List start
- `message_system` → Pehla element (system instructions)
- `,` → Separator
- `message` → Dusra element (user question)
- `]` → List end

**Complete meaning:**  
Dono messages ko ek list mein dalo, pehle system message, phir user message.

**Why order matters:**

```
CORRECT:
[system, user]
    ↓
LLM pehle role samajhta hai,
phir question process karta hai

WRONG:
[user, system]
    ↓
LLM confused ho sakta hai
```

**Runtime value:**
```python
[
    {
        "role": "system",
        "content": "You are a brand manager"
    },
    {
        "role": "user",
        "content": "suggest a name for my food brand only 1"
    }
]
```

---

### NEW CONCEPT: Temperature Parameter

### Line 35:

```python
response = client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=2
)
```

**Word-by-word breakdown:**

- Same as Day 1 EXCEPT:
- `temperature=2` → **New parameter**

**Complete meaning:**  
API call karte waqt temperature parameter pass kar rahe hain.

---

## DEEP DIVE: Temperature Parameter

### What is Temperature?

Temperature ek setting hai jo control karti hai ki LLM ka output kitna **creative** ya **predictable** hoga.

### Temperature Range:

```
0.0 ──────────────────── 1.0 ──────────────────── 2.0
│                        │                        │
Deterministic         Balanced              Very Creative
Predictable           Creative              Random/Experimental
Safe                  Default               Risky
```

### Examples:

#### Temperature = 0.0 (Low)

**Prompt:** "Suggest a name for my food brand"

**Possible outputs:** (consistently similar)
- FreshBite
- FreshBite
- FreshBite

**Behavior:**
- Sabse probable/common answer deta hai
- Har baar almost same answer
- Safe, predictable

---

#### Temperature = 1.0 (Medium - Default)

**Prompt:** "Suggest a name for my food brand"

**Possible outputs:** (varied but reasonable)
- TastyBites
- FlavorHub
- CrunchCo

**Behavior:**
- Balanced creativity
- Different answers har baar
- Reasonable variations

---

#### Temperature = 2.0 (High) ← Code mein use hua hai

**Prompt:** "Suggest a name for my food brand"

**Possible outputs:** (very creative/random)
- ZestyNova
- FlavorQuake
- CrunchWave Fusion
- NomNom Galaxy

**Behavior:**
- Bahut creative
- Unique answers
- Sometimes weird/unusual
- Experimental

---

### Internal Working:

```
LLM generates probability distribution:
    ↓
Word 1: 40% chance
Word 2: 30% chance
Word 3: 20% chance
Word 4: 10% chance
    ↓
Temperature = 0 → Always pick Word 1
Temperature = 1 → Randomly pick based on probabilities
Temperature = 2 → Flatten probabilities, more randomness
```

### When to use what?

```
Temperature 0.0 - 0.3:
✓ Code generation
✓ Math problems
✓ Factual Q&A
✓ Data extraction

Temperature 0.7 - 1.0:
✓ General conversation
✓ Content writing
✓ Emails
✓ Explanations

Temperature 1.5 - 2.0:
✓ Creative writing
✓ Brainstorming
✓ Brand names
✓ Story generation
```

---

### Line 38-39: Print

```python
# print(response)  ← Commented out
```

Is baar full response print nahi kar rahe (already Day 1 mein dekh liya).

---

### Line 42-43:

```python
print(response.choices[0].message.content)
```

Same as Day 1 - clean answer extract karke print karna.

---

## 9. COMPLETE EXECUTION TRACE

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 1-5: Same as Day 1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

(Imports, load_dotenv, API key, client, model)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 6: System message banao
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

message_system = {
    "role": "system",
    "content": "You are a brand manager"
}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 7: User message banao
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

message = {
    "role": "user",
    "content": "suggest a name for my food brand only 1"
}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 8: Messages list (ORDER MATTERS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

messages = [
    message_system,  ← Pehle
    message          ← Baad mein
]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 9: API call with temperature=2
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Python → Groq API
         │
         ├─ Model: llama-3.3-70b-versatile
         ├─ Messages: [system, user]
         └─ Temperature: 2 (high creativity)

LLM processing:
    │
    ├─ Step 1: Read system message
    │   └─ "I am a brand manager"
    │
    ├─ Step 2: Read user message
    │   └─ "Suggest food brand name"
    │
    ├─ Step 3: Generate response
    │   └─ Temperature=2 → Be very creative
    │
    └─ Step 4: Return answer

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 10: Print answer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

print(response.choices[0].message.content)

Output (example):
"FlavorFusion"
```

---

## 10. EXPECTED OUTPUT

### Example Run 1:
```
FlavorFusion
```

### Example Run 2:
```
TasteBurst
```

### Example Run 3:
```
Yummify
```

**Note:** Temperature=2 ki wajah se har baar different naam milega.

---

## 11. Common Beginner Confusions

### Q1: System message zaroori hai kya?

**Answer:**  
Nahi, optional hai. But ye LLM ki output quality improve karta hai.

**Without system message:**
```python
messages = [{"role": "user", "content": "Suggest a food brand name"}]
# Generic answer milega
```

**With system message:**
```python
messages = [
    {"role": "system", "content": "You are a brand manager"},
    {"role": "user", "content": "Suggest a food brand name"}
]
# Professional, creative answer milega
```

---

### Q2: System message kahan likhun - pehle ya baad mein?

**Answer:**  
**Hamesha pehle!**

```python
# CORRECT
messages = [system_message, user_message]

# WRONG
messages = [user_message, system_message]
```

---

### Q3: Temperature ki default value kya hai?

**Answer:**  
Usually `1.0` (agar parameter specify nahi karte).

```python
# These are equivalent:
response = client.chat.completions.create(model=model, messages=messages)
response = client.chat.completions.create(model=model, messages=messages, temperature=1.0)
```

---

### Q4: Temperature > 2.0 ya < 0.0 ho sakta hai?

**Answer:**  
Technically haan, but not recommended.

**Valid range:** 0.0 - 2.0

**If you try temperature=3.0:**
- Some APIs allow it
- Output bahut unstable hoga
- Gibberish ho sakta hai

---

### Q5: Kya hum multiple system messages bhej sakte hain?

**Answer:**  
Haan, but combine kar lo ek mein.

**Instead of:**
```python
[
    {"role": "system", "content": "You are a brand manager"},
    {"role": "system", "content": "Be creative"},
    {"role": "user", "content": "..."}
]
```

**Better:**
```python
[
    {"role": "system", "content": "You are a creative brand manager."},
    {"role": "user", "content": "..."}
]
```

---

### Q6: System prompt kaise likhe - short ya detailed?

**Answer:**  
Depends on use case.

**Short (fast, simple tasks):**
```python
"You are a helpful assistant."
```

**Detailed (complex tasks):**
```python
"""
You are a senior Python developer with expertise in Django.
Answer questions about Django best practices.
Provide code examples when relevant.
Be concise but thorough.
"""
```

---

## 12. Common Mistakes / Bugs

### Mistake 1: Wrong message order

**Wrong:**
```python
messages = [message, message_system]  # User first, system second
```

**Impact:**  
LLM might ignore system message or produce unexpected results.

---

### Mistake 2: Typo in "role"

**Wrong:**
```python
message_system = {
    "rol": "system",  # Typo
    "content": "..."
}
```

**Error:**  
API will reject the request.

---

### Mistake 3: Temperature as string

**Wrong:**
```python
temperature="2"  # String
```

**Correct:**
```python
temperature=2  # Integer or float
```

---

### Mistake 4: Too high temperature for factual tasks

**Bad example:**
```python
prompt = "What is 2+2?"
temperature = 2  # Too high!

# Possible bad output: "2+2 = 5" (hallucination)
```

**Better:**
```python
temperature = 0  # Deterministic for math
```

---

## 13. Professional Code Review

### ✅ Good Things:

1. **System prompt used** - Proper role assignment
2. **Clear variable names** - `message_system` vs `message`
3. **Temperature experimentation** - Learning parameter usage
4. **Comments** - Helpful for understanding

---

### 🔧 Improvements:

#### 1. **Temperature value too high for this task**

**Current:**
```python
temperature=2
```

**Issue:**  
Brand name generation doesn't need extreme creativity. Temperature=2 might give weird names.

**Better:**
```python
temperature=1.2  # Creative but not too random
```

---

#### 2. **Prompt could be more specific**

**Current:**
```python
prompt = "suggest a name for my food brand only 1"
```

**Better:**
```python
prompt = """
Suggest one unique name for my food brand.

Requirements:
- Easy to pronounce
- Memorable
- Related to food/taste
- Modern sounding
"""
```

---

#### 3. **System prompt could be more detailed**

**Current:**
```python
"You are a brand manager"
```

**Better:**
```python
"""
You are an experienced brand manager specializing in food industry.
You create memorable, catchy brand names that resonate with customers.
Focus on names that are:
- Easy to remember
- Simple to pronounce
- Unique in the market
"""
```

---

#### 4. **No error handling**

Same as Day 1 - API call should be in try-except block.

---

#### 5. **Hard to compare temperature effects**

**Better approach:**
```python
# Test different temperatures
for temp in [0, 1, 2]:
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temp
    )
    print(f"Temperature={temp}: {response.choices[0].message.content}")
```

---

## 14. What This Code Teaches You

New concepts from Day 2:

1. ✅ **System prompts** - LLM ko role dena
2. ✅ **Message ordering** - System pehle, user baad mein
3. ✅ **Temperature parameter** - Creativity control
4. ✅ **Multiple dictionaries** - Different message types
5. ✅ **API parameters** - Optional parameters ka use

---

## 15. What To Learn Next

Day 2 ke baad:

### Immediate:
1. **max_tokens** - Output length control (Day 3 mein aayega)
2. **Multiple prompts** - Loop mein process karna
3. **Temperature comparison** - Different values ka effect

### Future:
4. **Conversation history** - Multi-turn dialogue
5. **Streaming** - Real-time response
6. **JSON mode** - Structured output

---

## 16. Comparison: Day 1 vs Day 2

| Feature | Day 1 | Day 2 |
|---------|-------|-------|
| **System message** | ❌ Nahi | ✅ Haan ("brand manager") |
| **Temperature** | ❌ Default (1.0) | ✅ Specified (2.0) |
| **Messages count** | 1 (user only) | 2 (system + user) |
| **Output style** | Generic | Role-based |
| **Creativity** | Standard | High |

---

## 17. Experimentation Ideas

Try these variations:

### Experiment 1: Different temperatures

```python
for temp in [0, 0.5, 1, 1.5, 2]:
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temp
    )
    print(f"Temp {temp}: {response.choices[0].message.content}\n")
```

---

### Experiment 2: Different system prompts

```python
system_prompts = [
    "You are a brand manager",
    "You are a creative writer",
    "You are a marketing expert",
    "You are a minimalist designer"
]

for sys_prompt in system_prompts:
    # ... API call
```

---

### Experiment 3: Same prompt, multiple runs

```python
print("Running same prompt 5 times with temperature=2:\n")
for i in range(5):
    # ... API call
    # See how different the outputs are
```

---

## 18. Final Mental Model

```
System Prompt (LLM's personality)
    │
    ▼
User Prompt (actual question)
    │
    ▼
Temperature (creativity level)
    │
    ▼
LLM Processing
    │
    ▼
Creative Answer
```

### In one sentence:

**"Ye program LLM ko ek role (brand manager) deta hai, high creativity setting (temperature=2) use karta hai, aur unique food brand naam generate karta hai."**

---

## 19. Quick Reference

### Temperature Guide:

```python
# Factual/Precise
temperature=0.0  # Math, code, facts

# Balanced
temperature=1.0  # General conversation

# Creative
temperature=1.5  # Brainstorming, ideas

# Very Creative
temperature=2.0  # Experimental, wild ideas
```

### System Prompt Templates:

```python
# Expert
"You are a {expert_type} with {years} years of experience."

# Personality
"You are a {personality} assistant who {behavior}."

# Specific instructions
"You are an assistant. Always {rule1}. Never {rule2}."
```

---

**Great work! 🎉**  
Tumne system prompts aur temperature parameter successfully seekh liya!

Next: Day 3 mein **tokens** aur **max_tokens** parameter ka concept aayega! 🚀
