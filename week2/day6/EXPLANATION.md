# Week 2, Day 6 - Prompt Engineering Fundamentals 📝

## 1. What Does This Code Do?

Ye program **prompt engineering** ka practical example hai - kaise ek **structured, well-designed prompt** behtar results deta hai compared to vague prompts.

**Concept:** Same task, different prompt quality = vastly different LLM performance.

**Use case:** Customer support ticket classification system.

---

## 2. Big Picture Visualization

```
Customer Complaint
    │
    ↓
LLM Classification System
    │
    ├─ Option 1: Bad Prompt (vague)
    │   └─ Unreliable results
    │
    └─ Option 2: Good Prompt (structured)
        └─ Reliable, consistent results
        
Categories:
    ├─ Billing
    ├─ Technical
    ├─ Return
    └─ Other (fallback)
```

---

## 3. Real-Life Analogy

Socho tum ek employee ko task de rahe ho.

### Bad Instructions:
```
Boss: "Handle this issue."
Employee: "Which issue? What should I do? Confused..."
Result: Inconsistent work
```

### Good Instructions:
```
Boss:
- Role: You're a support assistant
- Task: Classify the issue
- Categories: Billing, Technical, Return
- Output: One word only
- Example: Refund request → Return
- Fallback: If unclear → Other
Result: Clear, consistent work
```

LLMs bhi same hain - clear instructions = better output!

---

## 4. Prerequisites / Concepts Used

1. **Prompt structure** - Role, Task, Constraints, Format, Examples, Fallback
2. **Helper functions** - Reusable LLM wrapper
3. **Prompt templates** - Structured prompt design

---

## 5. Code Breakdown

### Helper Function: `llm_func(prompt)`

```python
def llm_func(prompt):
    message = {
        "role": "user",
        "content": prompt
    }
    messages = [message]
    
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    
    ans = response.choices[0].message.content
    return ans
```

**Purpose:** Reusable wrapper for LLM calls.

**Benefit:** Don't repeat boilerplate code.

---

### BAD PROMPT Example

```python
bad_prompt = """
Role: You are a support assistant in an mobile or laptop company so work accordingly
task: you have to classify the issue in a category
constraint: you have c=to calssify the issue in 3 category which are billing , technical, return
output_format: your answer should be in 1 word only and should be in the 1 category given in constraints
#Example: For instance if a user compalin says he wants a refund then the category is Return
fallback: if issue is not related to any category in the constraints then the answer should be OTHER
this is a user complaint : MY girlfrind broke up with me"""
```

**Problems:**
1. ❌ Typos ("compalin", "c=to")
2. ❌ Inconsistent formatting
3. ❌ All crammed together
4. ❌ Hard to read
5. ❌ Random test case (girlfriend breakup)

---

## 6. Anatomy of a Good Prompt

### Framework: RTCOFX

**R - Role:** Who is the AI?  
**T - Task:** What should it do?  
**C - Constraints:** What are the rules?  
**O - Output Format:** How should the response look?  
**F - Fallback:** What if edge case?  
**X - eXample:** Show, don't just tell  

---

### IMPROVED PROMPT (Professional Version)

```python
good_prompt = """
ROLE:
You are a customer support classification assistant for a mobile and laptop company.

TASK:
Classify customer complaints into the appropriate category.

CATEGORIES (choose exactly one):
1. Billing - Payment issues, charges, invoices, refunds
2. Technical - Device not working, software bugs, hardware problems
3. Return - Product return requests, replacement requests

CONSTRAINTS:
- Return ONLY the category name (one word)
- Choose from: Billing, Technical, Return, Other
- Do not provide explanations

OUTPUT FORMAT:
<Category Name>

EXAMPLES:
- "I want a refund" → Return
- "My phone won't turn on" → Technical
- "Wrong amount charged" → Billing
- "The weather is nice" → Other

FALLBACK:
If the complaint is not related to Billing, Technical, or Return, respond with: Other

COMPLAINT:
{user_complaint}
"""
```

**Why better:**
✓ Clear sections  
✓ Explicit categories with descriptions  
✓ Multiple examples  
✓ Unambiguous output format  
✓ Professional structure

---

## 7. Expected Output

```python
print(llm_func(bad_prompt))
# Output (unpredictable): "Other" or "I'm sorry to hear that" or long paragraph

print(llm_func(good_prompt.format(user_complaint="MY girlfriend broke up with me")))
# Output (consistent): "Other"

print(llm_func(good_prompt.format(user_complaint="My iPhone screen is cracked")))
# Output: "Technical"

print(llm_func(good_prompt.format(user_complaint="I was charged twice")))
# Output: "Billing"
```

---

## 8. Prompt Engineering Best Practices

### 1. **Be Specific**

❌ Bad: "Classify this"  
✅ Good: "Classify this customer complaint into one of three categories: Billing, Technical, or Return"

---

### 2. **Provide Context (Role)**

❌ Bad: "Answer this question"  
✅ Good: "You are a senior Python developer. Answer this coding question."

---

### 3. **Use Examples (Few-Shot Learning)**

❌ Bad: "Extract the name"  
✅ Good: 
```
Extract the name.
Examples:
- "Hi I'm John" → John
- "My name is Sarah" → Sarah
```

---

### 4. **Define Output Format**

❌ Bad: "Tell me about AI"  
✅ Good: "Explain AI in exactly 3 bullet points, each under 10 words."

---

### 5. **Add Constraints**

❌ Bad: "Summarize this"  
✅ Good: "Summarize in under 50 words. Do not include personal opinions."

---

### 6. **Handle Edge Cases (Fallback)**

❌ Bad: "Classify: Dog, Cat, Bird"  
✅ Good: "Classify as Dog, Cat, Bird. If none match, return 'Other'."

---

## 9. Common Beginner Confusions

### Q1: Kya long prompt costly hai?

**Answer:** Haan, but worth it.

```
Short vague prompt:
- Less tokens (cheap)
- Bad results → retry → more calls → expensive overall

Long clear prompt:
- More tokens (slightly expensive)
- Good results → no retry → cheaper overall
```

---

### Q2: Examples compulsory hain?

**Answer:** No, but highly recommended (few-shot learning).

```python
# Zero-shot (no examples)
"Classify sentiment: positive, negative, neutral"

# Few-shot (with examples) - BETTER
"Classify sentiment.
Examples:
- 'I love this!' → positive
- 'This is terrible' → negative
- 'It's okay' → neutral"
```

---

### Q3: Prompt ka order matter karta hai?

**Answer:** Haan!

**Good order:**
1. Role
2. Task
3. Context
4. Examples
5. Actual input

**Bad order:**
1. Actual input (at start)
2. Task (at end)
→ LLM might miss instructions

---

## 10. What This Code Teaches You

1. ✅ **Prompt structure** - RTCOFX framework
2. ✅ **Helper functions** - DRY principle
3. ✅ **Few-shot learning** - Learning by examples
4. ✅ **Edge case handling** - Fallback strategies
5. ✅ **Professional formatting** - Clear, readable prompts

---

## 11. Final Mental Model

```
Vague Prompt → Confused LLM → Bad Output → Retry → Waste time/money

Structured Prompt → Clear Instructions → Good Output → No retry → Save time/money
```

### In one sentence:

**"Ye program prompt engineering fundamentals sikha raha hai - kaise ek well-structured prompt (Role, Task, Constraints, Output format, Examples, Fallback) LLM ko reliable results dene ke liye guide karta hai."**

---

**Great work! 🎉**  
Prompt engineering is the #1 skill for working with LLMs!

Next: Day 7 mein **ReAct pattern** sikhega - LLMs with tools! 🚀
