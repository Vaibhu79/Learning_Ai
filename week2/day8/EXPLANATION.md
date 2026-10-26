# Week 2, Day 8 - Multi-Step LLM Chains ⛓️

## 1. What Does This Code Do?

Ye program **LLM chaining** ka concept sikha raha hai - ek complex task ko multiple simple steps mein todna aur har step ke liye LLM ko separately call karna.

**Simple workflow:**
1. **Step 1:** Resume se skills extract karo (LLM call 1)
2. **Step 2:** Job description se skills extract karo (LLM call 2)  
3. **Step 3:** Dono ko compare karke match score do (LLM call 3)

**Key insight:** Instead of one complex prompt, use multiple focused prompts in sequence.

---

## 2. Big Picture Visualization

```
TRADITIONAL APPROACH (Single LLM Call):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Massive Prompt:
"Compare this resume with this JD. Extract skills from both,
match them, score them, and explain everything..."
    │
    ▼
LLM (overwhelmed, inconsistent)
    │
    ▼
Unpredictable output


CHAINING APPROACH (Multiple LLM Calls):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Resume Text
    │
    ▼
[LLM Call 1] "Extract skills from resume"
    │
    ▼
Candidate Skills: "Python, FastAPI, MySQL..."
    │
    ▼
[LLM Call 2] "Extract skills from JD"
    │
    ▼
Job Skills: "Python, FastAPI, PostgreSQL..."
    │
    ▼
[LLM Call 3] "Compare these two skill lists"
    │
    ▼
Score: 85%, Matching: [...], Missing: [...]
```

---

## 3. Real-Life Analogy

Socho ek **assembly line** factory hai (like car manufacturing).

**Without Chaining (One worker does everything):**
```
Worker 1: 
├─ Design car
├─ Build engine
├─ Paint
├─ Test
└─ Package

Problems:
- Overwhelming
- Slow
- Error-prone
- Inconsistent quality
```

**With Chaining (Specialized workers):**
```
Worker 1: Design (specialist) ✓
    ↓
Worker 2: Build engine (specialist) ✓
    ↓
Worker 3: Paint (specialist) ✓
    ↓
Worker 4: Test (specialist) ✓
    ↓
Worker 5: Package (specialist) ✓

Benefits:
- Focused tasks
- Faster
- Higher quality
- Consistent
```

LLM chains work the same way!

---

## 4. Prerequisites / Concepts Used

Week 1-2 concepts plus:

1. **Function chaining** - Output of function 1 → Input of function 2
2. **Helper functions** - Reusable LLM wrappers
3. **Sequential processing** - Step-by-step execution
4. **Modular prompts** - Each step has focused prompt
5. **Intermediate results** - Storing outputs between steps
6. **Separation of concerns** - Each function does one thing
7. **Rate limiting** - time.sleep() between calls

---

## 5. Code Architecture

### Component 1: Helper Function (LLM Wrapper)

```python
def ask_llm(system_prompt, user_prompt):
    sys_msg = {
        "role": "system",
        "content": system_prompt,
    }
    user_msg = {
        "role": "user",
        "content": user_prompt
    }
    
    messages = [sys_msg, user_msg]
    
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    
    answer = response.choices[0].message.content
    return answer
```

**Purpose:** Reusable function to call LLM.

**Benefits:**
- ✅ DRY (Don't Repeat Yourself)
- ✅ Consistent structure
- ✅ Easy to modify centrally
- ✅ Cleaner code

**Usage:**
```python
result = ask_llm("You are X", "Do Y")
```

---

### Component 2: Step 1 - Resume Skill Extraction

```python
def step1_res_extract(RESUME):
    # extract skills from resume
    system_prompt = """
    You are a professional HR assistant. Extract the skills from the candidates resume provided.
    Only return the skills no other information. Do not invent any skills by yourself.
    Output Format:
    Skills should be separated by commas. Just return comma separated skills do not return any other filler information
    """
    
    user_prompt = f"""
    Extract the skills from this resume
    {RESUME}
    """
    
    return ask_llm(system_prompt, user_prompt)
```

**Input:** Resume text  
**Output:** Comma-separated skills  
**Example:** `"Python, FastAPI, MySQL, Docker, REST APIs, Git"`

---

### Component 3: Step 2 - JD Skill Extraction

```python
def step2_JD_extract(JD):
    print("step2")
    system_prompt = """
    You are a professional HR assistant. Extract the skills from the Job description provided.
    Only return the skills no other information. Do not invent any skills by yourself.
    Output Format:
    Skills should be separated by commas. Just return comma separated skills do not return any other filler information
    """
    
    user_prompt = f"""
    Extract the skills from this JD
    {JD}
    """
    
    return ask_llm(system_prompt, user_prompt)
```

**Input:** Job description text  
**Output:** Comma-separated skills  
**Example:** `"Python, FastAPI, PostgreSQL, Docker, AWS, REST APIs"`

---

### Component 4: Step 3 - Matching & Scoring

```python
def step3_match(candidate, jd):
    system_prompt = """
    You are a professional HR assistant. compare the skills of candidate and the skills required in the JD and produce a final score between
    1 and 100. also produce a short verdict whether the candidate is a good fit for the role.
    """
    
    user_prompt = f"""
    Compare and match the skills
    JD:
    {jd}
    Candidate:
    {candidate}
    """
    
    return ask_llm(system_prompt, user_prompt)
```

**Input:** Candidate skills (string), JD skills (string)  
**Output:** Score and verdict  
**Example:** 
```
Score: 85/100
Verdict: Good fit. Candidate has most required skills. Missing: PostgreSQL, AWS.
```

---

## 6. Main Execution Flow

```python
JD = """We are hiring a Backend Python Developer.

Requirements:
- Strong Python
- FastAPI or Django
- PostgreSQL
- Docker
- AWS
- REST APIs
- 2+ years of experience
"""

RESUME = """
Name: Rahul Sharma

Experience:
3 years as a Software Developer.

Skills:
Python, FastAPI, MySQL, Docker,
REST APIs, Git

Projects:
Built a food delivery backend using
FastAPI and MySQL.

Deployed applications using Docker.
"""

# Step 1: Extract candidate skills
candidate = step1_res_extract(RESUME)
print(candidate)
sleep(2)

# Step 2: Extract JD skills
jd = step2_JD_extract(JD)
print(jd)
sleep(2)

# Step 3: Match and score
score = step3_match(candidate, jd)
print(score)
```

---

## 7. COMPLETE EXECUTION TRACE

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 1: Extract Candidate Skills
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Input:
    RESUME = "Name: Rahul Sharma\n Experience: 3 years..."

LLM Call 1:
    System: "You are HR assistant, extract skills..."
    User: "Extract skills from this resume {RESUME}"
    
LLM Processing:
    Reads resume
    Identifies: Python, FastAPI, MySQL, Docker, REST APIs, Git
    Ignores: Name, experience years, project details
    
Output:
    candidate = "Python, FastAPI, MySQL, Docker, REST APIs, Git"

Print:
Python, FastAPI, MySQL, Docker, REST APIs, Git

Wait 2 seconds (rate limiting)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 2: Extract JD Skills
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Input:
    JD = "We are hiring Backend Python Developer..."

LLM Call 2:
    System: "You are HR assistant, extract skills..."
    User: "Extract skills from this JD {JD}"
    
LLM Processing:
    Reads JD
    Identifies: Python, FastAPI, Django, PostgreSQL, Docker, AWS, REST APIs
    Ignores: Experience requirement, job description text
    
Output:
    jd = "Python, FastAPI, Django, PostgreSQL, Docker, AWS, REST APIs"

Print:
Python, FastAPI, Django, PostgreSQL, Docker, AWS, REST APIs

Wait 2 seconds

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 3: Match & Score
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Input:
    candidate = "Python, FastAPI, MySQL, Docker, REST APIs, Git"
    jd = "Python, FastAPI, Django, PostgreSQL, Docker, AWS, REST APIs"

LLM Call 3:
    System: "Compare skills and score..."
    User: "Compare: JD: {jd}, Candidate: {candidate}"
    
LLM Processing:
    Matching skills: Python, FastAPI, Docker, REST APIs (4/7)
    Missing skills: Django, PostgreSQL, AWS (3/7)
    Extra skills: MySQL, Git (not in JD, but relevant)
    
    Analysis:
    - Core Python & FastAPI: ✓ Match
    - Docker: ✓ Match
    - REST APIs: ✓ Match
    - MySQL instead of PostgreSQL: Similar but different
    - Missing AWS: Cloud experience gap
    - Has Git: Bonus
    
    Scoring logic:
    - 4 exact matches out of 7 required ≈ 57%
    - MySQL (similar to PostgreSQL) +10%
    - 3 years experience (meets 2+ years) +10%
    - Good fundamentals +8%
    Total: ~85/100

Output:
    score = "Score: 85/100
    
    Verdict: Good fit for the role.
    
    Matching Skills: Python, FastAPI, Docker, REST APIs
    Missing Skills: PostgreSQL (has MySQL), AWS
    
    The candidate has strong fundamentals and 3 years of
    experience, which meets the requirements. MySQL experience
    should translate well to PostgreSQL. AWS could be learned
    on the job."

Print:
Score: 85/100

Verdict: Good fit for the role.
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
END
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total LLM calls: 3
Total time: ~6 seconds (with delays)
```

---

## 8. Why Chaining Works Better

### Reason 1: **Focused Prompts**

**Single LLM approach:**
```
"Extract skills from resume, extract skills from JD,
compare them, score them, explain matching skills,
list missing skills, give verdict..."

Problems:
- Too many instructions
- LLM might skip steps
- Inconsistent output format
- Hard to debug
```

**Chained approach:**
```
Step 1: "Extract skills from resume" (focused)
Step 2: "Extract skills from JD" (focused)
Step 3: "Compare these two lists" (focused)

Benefits:
- Clear, single-purpose prompts
- Reliable outputs
- Easy to debug
- Predictable
```

---

### Reason 2: **Intermediate Validation**

**Without chaining:**
```
Input → LLM (black box) → Output
(Can't inspect intermediate steps)
```

**With chaining:**
```
Input → Step 1 → Check output → Step 2 → Check output → Step 3 → Final
(Can validate each step)
```

**Example:**
```python
candidate = step1_res_extract(RESUME)
print(candidate)  # Verify extraction is correct

if "error" in candidate.lower():
    print("Step 1 failed, stopping")
    exit()

# Continue to step 2...
```

---

### Reason 3: **Reusability**

Functions can be used independently:

```python
# Use step1 for another purpose
skills = step1_res_extract(some_other_resume)

# Use step2 separately
required_skills = step2_JD_extract(another_jd)

# Use step3 for different comparison
score = step3_match(profile_a, profile_b)
```

---

### Reason 4: **Easier Debugging**

**Problem:** Final output is wrong.

**Single LLM approach:**
```
"Which part failed? Extraction? Comparison? Scoring?"
→ Hard to tell, must guess
```

**Chained approach:**
```
Print after each step:
    Step 1 output: "Python, Java"  ← Looks good
    Step 2 output: "Python, C++"   ← Looks good
    Step 3 output: "Score: 0"      ← Problem is here!

Now debug only step 3!
```

---

### Reason 5: **Flexibility**

Easy to modify individual steps:

```python
# Original: Simple extraction
def step1_res_extract(RESUME):
    return ask_llm("Extract skills", RESUME)

# Enhanced: Extract with categories
def step1_res_extract_v2(RESUME):
    return ask_llm(
        "Extract skills and categorize as: Technical, Soft, Tools",
        RESUME
    )
```

Other steps remain unchanged!

---

## 9. Common Beginner Confusions

### Q1: Kyun 3 LLM calls? 1 hi kaafi nahi?

**Answer:**

**1 call approach:**
```
Prompt: "Do everything: extract, compare, score..."
Problems:
- ❌ Complex prompt
- ❌ Unreliable
- ❌ Hard to debug
- ❌ Can't reuse parts
```

**3 call approach:**
```
Call 1: Extract from resume (simple, reliable)
Call 2: Extract from JD (simple, reliable)
Call 3: Compare (simple, reliable)

Benefits:
- ✅ Simple prompts
- ✅ Reliable
- ✅ Easy to debug
- ✅ Reusable
```

**Trade-off:** More API calls = slightly higher cost, but much better quality!

---

### Q2: sleep(2) kyun use kar rahe hain?

**Answer:**

Rate limiting (discussed in Day 5, Day 7).

**Without sleep:**
```
Call 1: 0.0s
Call 2: 0.2s
Call 3: 0.4s
→ 3 calls in 0.4s → Rate limit error possible
```

**With sleep(2):**
```
Call 1: 0.0s
Sleep 2s
Call 2: 2.0s
Sleep 2s
Call 3: 4.0s
→ 3 calls in 4s → Safe
```

---

### Q3: Har step ka output validate karna compulsory hai?

**Answer:**

No, but **highly recommended** for production code.

**Without validation:**
```python
candidate = step1_res_extract(RESUME)
jd = step2_JD_extract(JD)
score = step3_match(candidate, jd)
# If step1 fails, step3 gets garbage input
```

**With validation:**
```python
candidate = step1_res_extract(RESUME)
if not candidate or len(candidate) < 5:
    raise ValueError("Step 1 failed: No skills extracted")

jd = step2_JD_extract(JD)
if not jd or len(jd) < 5:
    raise ValueError("Step 2 failed: No skills extracted")

score = step3_match(candidate, jd)
```

---

### Q4: Kya hum steps ko parallel run kar sakte hain?

**Answer:**

**Depends on dependencies!**

**Sequential (current code):**
```python
candidate = step1(RESUME)  # Must finish first
jd = step2(JD)             # Then this
score = step3(candidate, jd)  # Then this
```

**Parallel (if steps 1 & 2 are independent):**
```python
import concurrent.futures

with concurrent.futures.ThreadPoolExecutor() as executor:
    future1 = executor.submit(step1, RESUME)
    future2 = executor.submit(step2, JD)
    
    candidate = future1.result()
    jd = future2.result()

score = step3(candidate, jd)  # Still sequential (depends on 1 & 2)
```

**Time saved:**
```
Sequential: 2s + 2s + 2s = 6s
Parallel:   max(2s, 2s) + 2s = 4s
```

---

### Q5: Helper function necessary hai kya?

**Answer:**

**Not necessary, but professional.**

**Without helper (repetitive):**
```python
def step1(RESUME):
    sys_msg = {"role": "system", "content": "..."}
    user_msg = {"role": "user", "content": f"{RESUME}"}
    messages = [sys_msg, user_msg]
    response = client.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content

def step2(JD):
    sys_msg = {"role": "system", "content": "..."}
    user_msg = {"role": "user", "content": f"{JD}"}
    messages = [sys_msg, user_msg]
    response = client.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content

# Repeated boilerplate code!
```

**With helper (DRY):**
```python
def ask_llm(system_prompt, user_prompt):
    # Boilerplate code once
    ...
    return answer

def step1(RESUME):
    return ask_llm("system prompt", f"user prompt {RESUME}")

def step2(JD):
    return ask_llm("system prompt", f"user prompt {JD}")

# Clean, maintainable!
```

---

### Q6: Output format standardize karna important hai?

**Answer:**

**Extremely important!**

**Bad (unpredictable format):**
```
Step 1: "Skills: Python, Java, C++"
Step 2: "Required skills are: Python, Java"
Step 3 gets confused by different formats!
```

**Good (consistent format):**
```
Step 1: "Python, Java, C++"
Step 2: "Python, Java, AWS"
Step 3: Easy to compare!
```

**Best practice:** Specify output format in every prompt:
```
"Output Format: Comma-separated skills, no other text"
```

---

## 10. Common Mistakes / Bugs

### Mistake 1: Not handling empty outputs

**Problem:**
```python
candidate = step1_res_extract(RESUME)
# What if LLM returns empty string?
jd = step2_JD_extract(JD)
score = step3_match(candidate, jd)  # Garbage input!
```

**Solution:**
```python
candidate = step1_res_extract(RESUME)
if not candidate:
    print("Error: No skills extracted from resume")
    return

jd = step2_JD_extract(JD)
if not jd:
    print("Error: No skills extracted from JD")
    return

score = step3_match(candidate, jd)
```

---

### Mistake 2: Ignoring LLM errors

**Problem:**
```python
def ask_llm(system_prompt, user_prompt):
    response = client.chat.completions.create(...)
    # What if API fails?
    return response.choices[0].message.content
```

**Solution:**
```python
def ask_llm(system_prompt, user_prompt):
    try:
        response = client.chat.completions.create(...)
        return response.choices[0].message.content
    except Exception as e:
        print(f"LLM error: {e}")
        return None
```

---

### Mistake 3: Inconsistent output formats

**Problem:**
```python
Step 1: "Skills:\n- Python\n- Java"
Step 2: "Python, Java, AWS"
# Different formats!
```

**Solution:** Enforce format in every prompt:
```python
"Output Format: Comma-separated list, no bullet points, no headers"
```

---

### Mistake 4: Not logging intermediate results

**Problem:**
```python
candidate = step1_res_extract(RESUME)
jd = step2_JD_extract(JD)
score = step3_match(candidate, jd)
print(score)
# Can't see intermediate steps during debugging
```

**Solution:**
```python
print("Step 1: Extracting candidate skills...")
candidate = step1_res_extract(RESUME)
print(f"Result: {candidate}\n")

print("Step 2: Extracting JD skills...")
jd = step2_JD_extract(JD)
print(f"Result: {jd}\n")

print("Step 3: Matching...")
score = step3_match(candidate, jd)
print(f"Result: {score}")
```

---

### Mistake 5: Typo in function name

**Current code has a typo:**
```python
def step2_JD_extract(JD):  # Correct function name
    ...

# But later in main:
jd = step1_res_extract(JD)  # ← BUG! Should be step2_JD_extract
```

Wait, let me re-check the actual code...

Actually, looking at the code again:
```python
candidate=step1_res_extract(RESUME)
print(candidate)
sleep(2)
jd=step1_res_extract(JD)  # ← This should be step2_JD_extract!
```

**This is a BUG!** It's calling `step1` twice instead of `step1` then `step2`.

**Correct:**
```python
candidate = step1_res_extract(RESUME)
jd = step2_JD_extract(JD)  # Fix!
```

---

## 11. Professional Code Review

### ✅ Good Things:

1. **Modular design** - Each step is a separate function
2. **Helper function** - Reusable LLM wrapper
3. **Clear prompts** - Each step has focused instructions
4. **Rate limiting** - sleep() between calls
5. **Output format specified** - Consistent comma-separated format
6. **Separation of concerns** - Extract, extract, compare

---

### 🔧 Improvements:

#### 1. **FIX THE BUG!**

```python
# Current (WRONG):
jd = step1_res_extract(JD)

# Fixed:
jd = step2_JD_extract(JD)
```

---

#### 2. **Add error handling**

```python
def ask_llm(system_prompt, user_prompt):
    try:
        # ... API call
        return answer
    except Exception as e:
        logging.error(f"LLM call failed: {e}")
        return None
```

---

#### 3. **Validate outputs**

```python
candidate = step1_res_extract(RESUME)
if not candidate or len(candidate) < 5:
    raise ValueError("Failed to extract candidate skills")
```

---

#### 4. **Add logging**

```python
import logging

logging.info("Starting skill extraction pipeline")
logging.debug(f"Resume: {RESUME[:100]}...")
logging.info("Step 1: Extracting candidate skills")
```

---

#### 5. **Make configurable**

```python
CONFIG = {
    "model": "llama-3.3-70b-versatile",
    "rate_limit_delay": 2,
    "retry_attempts": 3
}

def ask_llm(system_prompt, user_prompt, config=CONFIG):
    # Use config values
    ...
```

---

#### 6. **Return structured data**

Instead of comma-separated strings, return structured data:

```python
def step1_res_extract_v2(RESUME):
    prompt = "Extract skills as JSON array"
    response = ask_llm(prompt, RESUME)
    return json.loads(response)  # Returns list

# Usage:
candidate_skills = ["Python", "FastAPI", "Docker"]  # List, not string
```

---

## 12. Real-World Chaining Patterns

### Pattern 1: Linear Chain

```
Step A → Step B → Step C → Result
```

Current code follows this pattern.

---

### Pattern 2: Tree Chain

```
       Step 1
       /    \
   Step 2  Step 3
       \    /
       Step 4
```

**Example:**
```python
summary = summarize(document)
keywords = extract_keywords(document)
final = combine(summary, keywords)
```

---

### Pattern 3: Loop Chain

```
Step A → Step B → Evaluate
           ↑          ↓
           └── If not satisfied, retry
```

**Example:**
```python
while score < 80:
    summary = improve_summary(summary, feedback)
    score = evaluate(summary)
```

---

### Pattern 4: Conditional Chain

```
Step A → Condition?
           ├─ Yes: Step B
           └─ No: Step C
```

**Example:**
```python
category = classify(text)
if category == "technical":
    result = technical_analysis(text)
else:
    result = general_analysis(text)
```

---

## 13. What This Code Teaches You

Concepts from Day 8:

1. ✅ **LLM chaining** - Sequential LLM calls
2. ✅ **Modular functions** - One purpose per function
3. ✅ **Helper functions** - Reusable wrappers
4. ✅ **Focused prompts** - Single-purpose instructions
5. ✅ **Intermediate validation** - Checking each step
6. ✅ **Output standardization** - Consistent formats
7. ✅ **Rate limiting** - Managing API calls
8. ✅ **Debugging strategies** - Inspecting intermediate results
9. ✅ **Code organization** - Clean, maintainable structure

---

## 14. What To Learn Next

Day 8 ke baad:

### Immediate (Day 9):
1. **Streaming** - Real-time token-by-token output
2. **Progressive responses** - User sees results as they generate

### Future:
3. **Parallel chains** - Running steps concurrently
4. **Error recovery** - Retry logic, fallbacks
5. **Chain optimization** - Reducing API calls
6. **Advanced patterns** - MapReduce, Tree of Thoughts

---

## 15. Final Mental Model

```
Complex Task
    │
    ├─ Break into simple steps
    │
    ├─ Step 1: Focused LLM call
    │   └─ Validate output
    │
    ├─ Step 2: Focused LLM call
    │   └─ Validate output
    │
    ├─ Step 3: Focused LLM call
    │   └─ Validate output
    │
    └─ Combine results → Final answer
    
Benefits:
- Simple prompts
- Reliable outputs
- Easy debugging
- Reusable components
```

### In one sentence:

**"Ye program LLM chaining pattern use karta hai jahan ek complex task (resume-JD matching) ko teen focused steps mein toda jata hai - har step ek simple, reliable LLM call hai jiska output next step ka input banta hai."**

---

**Excellent work! 🎉**  
LLM chaining is fundamental to building robust AI applications!

This pattern is used in:
- LangChain
- Production AI pipelines
- Multi-agent systems
- Complex workflows

Next: Day 9 mein **streaming responses** for better UX! 🚀
