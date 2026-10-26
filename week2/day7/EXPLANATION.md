# Week 2, Day 7 - ReAct Pattern: LLM Agents with Tools 🛠️

## 1. What Does This Code Do?

Ye program **ReAct (Reasoning + Acting) pattern** implement karta hai - ek powerful agent architecture jahan LLM **soch sakta hai** (Reasoning) aur **actions le sakta hai** (Acting).

**Simple explanation:**
1. LLM ko tools diye jate hain (`get_product_price`, `calculator`)
2. User ek complex question puchta hai
3. LLM **step-by-step** sochta hai kya karna hai
4. LLM appropriate tool call karta hai
5. Tool ka result LLM ko wapas milta hai (Observation)
6. LLM next step decide karta hai
7. Jab task complete ho, final answer deta hai

**Real-world analogy:** Ek assistant jo information find kar sakta hai (tools) aur logical reasoning kar sakta hai.

---

## 2. Big Picture Visualization

```
User Question
    │
    │ "I have 5000 rupees. What is the price 
    │  of iPhone 17 and how much will I have left?"
    │
    ▼
Agent (LLM)
    │
    ├─ Step 1: Think
    │   └─ "Need to get iPhone 17 price"
    │
    ├─ Action: get_product_price("iPhone 17")
    │   ↓
    │   Tool executes
    │   ↓
    │   Observation: 1000
    │
    ├─ Step 2: Think
    │   └─ "Need to calculate 5000 - 1000"
    │
    ├─ Action: calculator("5000 - 1000")
    │   ↓
    │   Tool executes
    │   ↓
    │   Observation: 4000
    │
    ├─ Step 3: Think
    │   └─ "Have all info, can answer now"
    │
    └─ Final Answer:
        "iPhone 17 costs 1000 rupees. 
         You'll have 4000 rupees left."
```

---

## 3. Real-Life Analogy

Socho ek **research assistant** hai jiske paas tools hain.

**Without Tools (Traditional LLM):**
```
You: "What's the price of iPhone 17 and how much will I save?"
Assistant: "I don't have real-time pricing information..."
```

**With Tools (ReAct Agent):**
```
You: "What's the price of iPhone 17 and how much will I save if I have 5000?"

Assistant's Internal Process:
    ↓
Thought: "I need to check the price first"
Action: Calls pricing database
Observation: 1000 rupees
    ↓
Thought: "Now I need to calculate savings"
Action: Uses calculator
Observation: 4000 rupees
    ↓
Thought: "I have all information"
Final Answer: "iPhone 17 costs 1000. You'll have 4000 left."
```

---

## 4. Prerequisites / Concepts Used

Week 1-2 concepts plus:

1. **ReAct pattern** - Reasoning + Acting
2. **Tool calling** - LLM executing functions
3. **Regex** - Pattern matching for parsing LLM output
4. **Iterative loops** - Multi-step reasoning
5. **State management** - Conversation memory
6. **Action parsing** - Extracting tool calls from text
7. **Observation injection** - Feeding tool results back
8. **Regular expressions** - `re.search()`, patterns
9. **String matching** - Identifying tool names
10. **Multi-turn dialogue** - Agent maintains context

---

## 5. What is ReAct?

### ReAct = Reasoning + Acting

**Research paper:** "ReAct: Synergizing Reasoning and Acting in Language Models" (2022)

### Traditional LLM (Knowledge-only):
```
User: "What's 2+2?"
LLM: "4" ✓ (from training)

User: "What's the weather today?"
LLM: "I don't have real-time data" ✗ (no access to tools)
```

### ReAct Agent (Knowledge + Tools):
```
User: "What's the weather today?"
LLM: 
    Thought: I need to check weather API
    Action: weather_api("current")
    Observation: 25°C, Sunny
    Final Answer: "It's 25°C and sunny today" ✓
```

---

### ReAct Loop:

```
Thought → Action → Observation → Thought → Action → Observation → ... → Answer
```

**Example:**
```
User: "Book me a flight to NYC and tell me the weather there"

Thought 1: Need to book flight
Action 1: book_flight("NYC")
Observation 1: "Flight booked, confirmation #ABC123"

Thought 2: Need weather info
Action 2: weather_api("NYC")
Observation 2: "15°C, Rainy"

Final Answer: "Flight booked (confirmation #ABC123). NYC weather: 15°C, Rainy"
```

---

## 6. Code Architecture

### Component 1: Tools (Python Functions)

```python
def get_product_price(product):
    if product == 'iPhone 17':
        return 1000
    elif product == "iPhone 15":
        return 500
    else:
        return 0

def calculator(expression):
    try:
        return eval(expression)
    except:
        return "calc error!"
```

**Purpose:** Real functions LLM can execute.

**Real-world equivalent:**
- API calls
- Database queries
- File operations
- External service calls

---

### Component 2: Tool Registry

```python
tools = {
    "get_product_price": get_product_price,
    "calculator": calculator
}
```

**Purpose:** Map tool names (strings) to actual functions.

**Why dictionary?**
```python
tool_name = "calculator"
tool_function = tools[tool_name]  # Get function by name
result = tool_function("2+2")      # Execute it
```

---

### Component 3: System Prompt (The Brain)

```python
system_prompt = """
You are a shopping assistant.

You have these tools:

get_product_price(product)
calculator(expression)

IMPORTANT:
Call tools exactly like these examples:

Action: get_product_price("iPhone 17")
Action: calculator("5000 - 1000")

Never write:
get_product_price(product="iPhone 17")

Never write:
calculator(expression="5000 - 1000")

Follow these rules:

1. Decide what you need to do next.
2. Call ONLY ONE tool at a time.
3. After writing an Action, STOP immediately.
4. Never guess or invent a tool result.
5. Wait until you receive an Observation.
6. Then decide your next action.
7. When the task is complete, give the Final Answer.

Format:

Thought: what you need to do
Action: tool_name(argument)

When finished:

Final Answer: your answer
"""
```

---

## DEEP DIVE: System Prompt Design

### Why such specific instructions?

#### Instruction 1: Exact format
```
Action: get_product_price("iPhone 17")  ✓ Correct

NOT:
Action: get_product_price(product="iPhone 17")  ✗ Wrong
```

**Reason:** Regex parser expects exact format. Python-style named arguments won't parse correctly.

---

#### Instruction 2: One tool at a time
```
Rule: "Call ONLY ONE tool at a time"
```

**Why?**

**Bad (multiple actions):**
```
Thought: Need price and calculation
Action: get_product_price("iPhone 17")
Action: calculator("5000 - 1000")
```
Problem: Regex can't reliably parse multiple actions. Results might mix.

**Good (one action):**
```
Thought: Need price first
Action: get_product_price("iPhone 17")
(wait for observation)

Thought: Now calculate
Action: calculator("5000 - 1000")
```

---

#### Instruction 3: Stop after action
```
Rule: "After writing an Action, STOP immediately"
```

**Why?**

**Bad:**
```
Action: get_product_price("iPhone 17")
The price is probably 1000 rupees...  ← DON'T DO THIS
```

**Good:**
```
Action: get_product_price("iPhone 17")
(stop, wait for observation)
```

LLM should **not** guess results. It must wait for actual tool output.

---

#### Instruction 4: Never guess
```
Rule: "Never guess or invent a tool result"
```

LLMs can hallucinate. This rule prevents fake data.

---

#### Instruction 5: Final Answer marker
```
When finished:
Final Answer: your answer
```

This tells the agent loop to stop iterating.

---

## 7. Agent Loop Implementation

### Function: `run_agent(question)`

```python
def run_agent(question):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ]
    
    for step in range(5):  # Max 5 iterations
        print("\n------------------")
        print("STEP", step + 1)
        print("------------------")
        
        # Get LLM response
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0
        )
        
        answer = response.choices[0].message.content
        print(answer)
        
        # Check if finished
        if "Final Answer:" in answer:
            break
        
        # Parse action
        match = re.search(r"Action:\s*(\w+)\((.*?)\)", answer)
        
        if match:
            tool_name = match.group(1)
            tool_input = match.group(2).strip().strip('"')
            
            # Execute tool
            if tool_name in tools:
                tool = tools[tool_name]
                observation = tool(tool_input)
            else:
                observation = "Tool not found"
            
            print("Observation:", observation)
            
            # Add to conversation
            messages.append({"role": "assistant", "content": answer})
            messages.append({"role": "user", "content": "Observation: " + str(observation)})
            
            sleep(5)  # Rate limiting
```

---

## DEEP DIVE: Line-by-Line Agent Loop

### Setup: Initialize conversation

```python
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": question}
]
```

**Initial state:**
```
messages = [
    {system instructions},
    {user question}
]
```

---

### Loop: Max 5 steps

```python
for step in range(5):
```

**Why 5?** Safety limit. Prevents infinite loops if LLM gets stuck.

**Typical usage:**
- Simple task: 2-3 steps
- Complex task: 4-5 steps
- If exceeds 5: Something's wrong (bad prompt or LLM confusion)

---

### Step 1: Get LLM response

```python
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=messages,
    temperature=0
)
```

**Why temperature=0?**  
Agent needs **deterministic** behavior, not creativity.

```
temperature=0 → Consistent, predictable actions
temperature>0 → Random, unpredictable (bad for agents)
```

---

### Step 2: Extract answer

```python
answer = response.choices[0].message.content
print(answer)
```

**Example answer:**
```
Thought: I need to find the price of iPhone 17 first
Action: get_product_price("iPhone 17")
```

---

### Step 3: Check termination

```python
if "Final Answer:" in answer:
    break
```

**Termination condition:** LLM says "Final Answer:"

**Example:**
```
Final Answer: iPhone 17 costs 1000 rupees. You will have 4000 rupees left.
```

Loop ends, agent done!

---

### NEW CONCEPT: Regex Parsing

### Step 4: Parse action

```python
match = re.search(r"Action:\s*(\w+)\((.*?)\)", answer)
```

---

## DEEP DIVE: Regular Expressions (Regex)

### What is Regex?

**Regex** = Pattern matching for strings.

### Basic regex syntax:

```python
\w   → Word character (a-z, A-Z, 0-9, _)
\s   → Whitespace (space, tab)
\d   → Digit (0-9)
.    → Any character
*    → 0 or more times
+    → 1 or more times
?    → 0 or 1 time
()   → Capture group
```

---

### Our regex pattern:

```python
r"Action:\s*(\w+)\((.*?)\)"
```

**Let's break it down:**

```
Action:          → Literal text "Action:"
\s*              → Zero or more spaces
(\w+)            → Capture group 1: One or more word chars (tool name)
\(               → Literal opening parenthesis
(.*?)            → Capture group 2: Any characters (lazy match)
\)               → Literal closing parenthesis
```

---

### Example matching:

**Input:**
```
"Action: get_product_price("iPhone 17")"
```

**Pattern match:**
```
Action:                    → Matches "Action:"
\s*                        → Matches " " (one space)
(\w+)                      → Captures "get_product_price"
\(                         → Matches "("
(.*?)                      → Captures "\"iPhone 17\""
\)                         → Matches ")"
```

**Captured groups:**
- Group 1: `"get_product_price"`
- Group 2: `"\"iPhone 17\""`

---

### Step 5: Extract captures

```python
if match:
    tool_name = match.group(1)
    tool_input = match.group(2).strip().strip('"')
```

**Word-by-word:**

- `match.group(1)` → First captured group (tool name)
- `match.group(2)` → Second captured group (argument)
- `.strip()` → Remove leading/trailing whitespace
- `.strip('"')` → Remove quotes

**Example:**
```python
tool_name = "get_product_price"
tool_input = "iPhone 17"  # Quotes removed
```

---

### Step 6: Execute tool

```python
if tool_name in tools:
    tool = tools[tool_name]
    observation = tool(tool_input)
else:
    observation = "Tool not found"
```

**Flow:**
```
tool_name = "get_product_price"
    ↓
tools["get_product_price"] → function reference
    ↓
function("iPhone 17") → executes
    ↓
observation = 1000
```

---

### Step 7: Feed observation back

```python
messages.append({"role": "assistant", "content": answer})
messages.append({"role": "user", "content": "Observation: " + str(observation)})
```

**What's happening:**

**Before:**
```python
messages = [
    {system},
    {user: original question}
]
```

**After step 1:**
```python
messages = [
    {system},
    {user: original question},
    {assistant: "Thought: ... Action: get_product_price(...)"},
    {user: "Observation: 1000"}
]
```

**Key insight:** We're building a conversation history. LLM sees previous thoughts and observations!

---

### Step 8: Rate limiting

```python
sleep(5)
```

API rate limit protection (discussed in Day 5).

---

## 8. COMPLETE EXECUTION TRACE

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SETUP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

User Question:
"I have 5000 rupees. What is the price of an iPhone 17?
and how much money will I have left?"

messages = [
    {role: "system", content: system_prompt},
    {role: "user", content: question}
]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ITERATION 1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LLM Response:
---
Thought: I need to find the price of iPhone 17 first
Action: get_product_price("iPhone 17")
---

Check "Final Answer:" → Not found, continue

Parse action:
    Regex matches: "get_product_price("iPhone 17")"
    tool_name = "get_product_price"
    tool_input = "iPhone 17"

Execute tool:
    tools["get_product_price"]("iPhone 17")
    → Returns: 1000

Observation: 1000

Update messages:
messages = [
    {system},
    {user: question},
    {assistant: "Thought: ... Action: get_product_price(...)"},
    {user: "Observation: 1000"}
]

Wait 5 seconds...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ITERATION 2
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LLM Response:
---
Thought: Now I know iPhone 17 costs 1000. I need to calculate 5000 - 1000
Action: calculator("5000 - 1000")
---

Check "Final Answer:" → Not found, continue

Parse action:
    Regex matches: "calculator("5000 - 1000")"
    tool_name = "calculator"
    tool_input = "5000 - 1000"

Execute tool:
    tools["calculator"]("5000 - 1000")
    → eval("5000 - 1000")
    → Returns: 4000

Observation: 4000

Update messages:
messages = [
    {system},
    {user: question},
    {assistant: "Thought: ... Action: get_product_price(...)"},
    {user: "Observation: 1000"},
    {assistant: "Thought: ... Action: calculator(...)"},
    {user: "Observation: 4000"}
]

Wait 5 seconds...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ITERATION 3
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LLM Response:
---
Thought: I have all the information needed to answer
Final Answer: The iPhone 17 costs 1000 rupees. You will have 4000 rupees left.
---

Check "Final Answer:" → FOUND!

Break loop → Agent done

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Final Answer: The iPhone 17 costs 1000 rupees. You will have 4000 rupees left.

Total iterations: 3
Total tools called: 2
Time elapsed: ~10 seconds (with delays)
```

---

## 9. Expected Output

```
------------------
STEP 1
------------------
Thought: I need to find the price of iPhone 17 first
Action: get_product_price("iPhone 17")
Observation: 1000

------------------
STEP 2
------------------
Thought: Now I know the price is 1000 rupees. I need to calculate how much money will be left
Action: calculator("5000 - 1000")
Observation: 4000

------------------
STEP 3
------------------
Thought: I have all the information needed
Final Answer: The iPhone 17 costs 1000 rupees. You will have 4000 rupees left.
```

---

## 10. Key Advantages of ReAct Pattern

### Advantage 1: Explainability

**Traditional LLM:**
```
User: "Complex question"
LLM: "Answer"
```
How did it arrive? Unknown (black box).

**ReAct Agent:**
```
User: "Complex question"
Agent:
    Thought: Step 1 reasoning
    Action: Tool 1
    Observation: Result 1
    Thought: Step 2 reasoning
    Action: Tool 2
    Observation: Result 2
    Final Answer: Answer
```
Full reasoning chain visible!

---

### Advantage 2: Error Recovery

**Traditional:**
```
LLM: "The answer is X"
(Wrong, no way to correct)
```

**ReAct:**
```
Thought: Try approach A
Action: tool_a()
Observation: Error

Thought: Approach A failed, try B
Action: tool_b()
Observation: Success!
```

Agent can adapt!

---

### Advantage 3: Access to Real Data

**Traditional LLM:**
```
User: "What's the weather?"
LLM: "I don't have real-time data" ✗
```

**ReAct Agent:**
```
User: "What's the weather?"
Agent:
    Thought: Need to check weather API
    Action: weather_api()
    Observation: 25°C, Sunny
    Final Answer: "It's 25°C and sunny" ✓
```

---

### Advantage 4: Complex Multi-Step Tasks

**Example task:** "Book a hotel, check weather, book cab"

**Traditional:** Can't execute actions

**ReAct:**
```
Step 1: book_hotel("NYC")
Step 2: weather_api("NYC")
Step 3: book_cab("airport", "hotel")
Final Answer: All done!
```

---

## 11. Common Beginner Confusions

### Q1: Why temperature=0?

**Answer:**

**Creative writing (temperature=1):**
```
"Tell me a story"
→ Creative, varied stories ✓
```

**Agent actions (temperature=0):**
```
"Book flight"
→ Deterministic, reliable action ✓

If temperature=1:
→ Might call wrong tool
→ Might hallucinate results
→ Inconsistent behavior ✗
```

---

### Q2: Why max 5 iterations?

**Answer:**

**Protection against infinite loops.**

**Bad scenario:**
```
Iteration 1: Action: tool_a()
Iteration 2: Action: tool_a()
Iteration 3: Action: tool_a()
...
(Stuck in loop, never finishes)
```

With max iterations, loop stops after 5 steps.

---

### Q3: Can LLM call tools directly?

**Answer:**

**No! LLM can only generate text.**

**What LLM does:**
```
Generates text: "Action: get_product_price("iPhone 17")"
```

**What Python does:**
```
1. Parses text (regex)
2. Extracts tool name & argument
3. Calls actual Python function
4. Gets result
5. Feeds result back to LLM
```

LLM doesn't "execute" code - it suggests what to execute!

---

### Q4: Why regex parsing? Can't use JSON?

**Answer:**

**Regex approach (current):**
```
LLM outputs: "Action: calculator("2+2")"
Parse with regex → Extract function call
```

**JSON approach (advanced):**
```
LLM outputs: {"action": "calculator", "input": "2+2"}
Parse JSON → Extract function call
```

Regex is simpler for text-based outputs. JSON requires `response_format` which some models might not support for function calling.

---

### Q5: Kya hum zyada tools add kar sakte hain?

**Answer:**

**Haan! Just add to tools dict.**

```python
def weather_api(city):
    # Simulate API
    return f"{city}: 25°C, Sunny"

def send_email(to, message):
    # Simulate email
    return f"Email sent to {to}"

tools = {
    "get_product_price": get_product_price,
    "calculator": calculator,
    "weather_api": weather_api,      # New!
    "send_email": send_email          # New!
}
```

Update system prompt with new tool descriptions!

---

### Q6: Why `sleep(5)` after every action?

**Answer:**

API rate limiting (discussed in Day 5).

```
Without sleep:
    → 10 API calls in 10 seconds
    → Rate limit error

With sleep(5):
    → 10 API calls in 50 seconds
    → Safe
```

---

## 12. Common Mistakes / Bugs

### Mistake 1: LLM doesn't follow format

**Problem:**
```
LLM outputs: "I will use get_product_price for iPhone 17"
Regex doesn't match (no "Action:" keyword)
```

**Solution:** Improve system prompt with stricter format rules and examples.

---

### Mistake 2: Tool name typo

**Problem:**
```
LLM: "Action: get_price("iPhone 17")"  # Wrong name
tools dict has: "get_product_price"
→ Tool not found
```

**Solution:** List exact tool names in system prompt.

---

### Mistake 3: Missing quotes in argument

**Problem:**
```
LLM: "Action: get_product_price(iPhone 17)"  # No quotes
Regex captures: "iPhone 17" (works by luck)

But for strings with spaces:
LLM: "Action: calculator(5000 - 1000)"  # No quotes, but works
LLM: "Action: send_email(user@example.com, Hello World)"  # Breaks! Comma splits
```

**Solution:** Enforce quotes in system prompt.

---

### Mistake 4: Calculator eval() security

**Current code:**
```python
def calculator(expression):
    return eval(expression)
```

**Security risk:** `eval()` can execute arbitrary code!

```python
# Malicious input
calculator("__import__('os').system('rm -rf /')")
# Could delete files!
```

**Solution:** Use safe evaluation or whitelist operations.

```python
import ast
import operator

def safe_calculator(expression):
    try:
        # Parse expression
        node = ast.parse(expression, mode='eval')
        
        # Define allowed operations
        ops = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv
        }
        
        # Evaluate safely
        return eval(compile(node, '<string>', 'eval'), {"__builtins__": {}}, {})
    except:
        return "Error"
```

---

### Mistake 5: Not handling max iterations

**Current code:**
```python
for step in range(5):
    # ... loop body
```

**Problem:** If loop finishes without "Final Answer", no output.

**Better:**
```python
for step in range(5):
    # ... loop body
    
else:  # Executed if loop completes without break
    print("Agent exceeded max iterations")
    print("Last response:", answer)
```

---

## 13. Professional Code Review

### ✅ Good Things:

1. **ReAct implementation** - Industry-standard agent pattern
2. **Regex parsing** - Efficient action extraction
3. **Conversation memory** - Context preservation
4. **Rate limiting** - API safety
5. **Tool registry** - Extensible architecture
6. **Temperature=0** - Deterministic behavior
7. **Max iterations** - Safety mechanism

---

### 🔧 Improvements:

#### 1. **Add error handling**

```python
try:
    observation = tool(tool_input)
except Exception as e:
    observation = f"Tool error: {e}"
```

---

#### 2. **Better regex pattern**

```python
# Current (basic)
r"Action:\s*(\w+)\((.*?)\)"

# Better (handles edge cases)
r"Action:\s*([a-zA-Z_][a-zA-Z0-9_]*)\((.*?)\)"
# Enforces valid Python identifier
```

---

#### 3. **Add logging**

```python
import logging

logging.info(f"Tool called: {tool_name}({tool_input})")
logging.info(f"Tool result: {observation}")
```

---

#### 4. **Validate tool input**

```python
def get_product_price(product):
    if not isinstance(product, str):
        return "Invalid input type"
    
    product = product.strip().lower()
    
    if product == 'iphone 17':
        return 1000
    # ...
```

---

#### 5. **Add tool descriptions to system prompt**

```python
system_prompt = f"""
You have these tools:

1. get_product_price(product_name: str) -> int
   Description: Returns the price of a product in rupees
   Example: get_product_price("iPhone 17") → 1000

2. calculator(expression: str) -> float
   Description: Evaluates mathematical expressions
   Example: calculator("2 + 2") → 4
"""
```

---

## 14. Real-World Applications

### Application 1: Customer Support Bot

```python
tools = {
    "search_orders": search_orders,
    "cancel_order": cancel_order,
    "issue_refund": issue_refund,
    "check_inventory": check_inventory
}

User: "Cancel my order and refund me"
Agent:
    → search_orders(user_id)
    → cancel_order(order_id)
    → issue_refund(order_id)
    → Answer: Done!
```

---

### Application 2: Research Assistant

```python
tools = {
    "web_search": web_search,
    "read_pdf": read_pdf,
    "summarize": summarize,
    "calculate_stats": calculate_stats
}

User: "Research AI papers and give me statistics"
Agent:
    → web_search("AI papers 2024")
    → read_pdf(paper_url)
    → calculate_stats(data)
    → Answer: Here are the stats...
```

---

### Application 3: DevOps Agent

```python
tools = {
    "check_server_status": check_server,
    "restart_service": restart_service,
    "check_logs": check_logs,
    "send_alert": send_alert
}

User: "Server is slow, investigate"
Agent:
    → check_server_status()
    → check_logs()
    → restart_service()
    → send_alert("Issue resolved")
```

---

## 15. What This Code Teaches You

Advanced concepts from Day 7:

1. ✅ **ReAct pattern** - Reasoning + Acting paradigm
2. ✅ **Agent loops** - Iterative problem solving
3. ✅ **Tool calling** - LLM executing functions
4. ✅ **Regex parsing** - Pattern extraction
5. ✅ **State management** - Conversation history
6. ✅ **Multi-step reasoning** - Complex task decomposition
7. ✅ **Observation feedback** - Closed-loop system
8. ✅ **Deterministic behavior** - temperature=0 for agents
9. ✅ **Safe iteration** - Max step limits
10. ✅ **Extensible architecture** - Easy to add tools

---

## 16. What To Learn Next

Day 7 ke baad:

### Immediate (Day 8):
1. **Multi-step chains** - Breaking complex tasks into steps
2. **Chain-of-thought** - Structured reasoning
3. **LLM chaining** - Multiple LLM calls in sequence

### Future (Week 3-4):
4. **RAG with agents** - Combining retrieval with actions
5. **Advanced tool calling** - Native function calling APIs
6. **Multi-agent systems** - Multiple agents collaborating
7. **Agent memory** - Long-term context

---

## 17. Final Mental Model

```
User Question
    │
    ▼
Agent Loop (max 5 iterations)
    │
    ├─ LLM Thinks (Reasoning)
    │   └─ Decides what to do
    │
    ├─ LLM Acts (Action)
    │   └─ Calls a tool
    │
    ├─ Tool Executes
    │   └─ Returns observation
    │
    ├─ Observation → Back to LLM
    │   └─ Context updated
    │
    └─ Repeat until "Final Answer"
    
Result: Complex task solved step-by-step!
```

### In one sentence:

**"Ye program ReAct pattern implement karta hai jahan LLM iteratively sochta hai (Thought), tools execute karta hai (Action), results observe karta hai (Observation), aur multi-step reasoning se complex questions solve karta hai."**

---

## 18. Comparison: Traditional vs ReAct

| Aspect | Traditional LLM | ReAct Agent |
|--------|----------------|-------------|
| **Knowledge** | Static (training data) | Dynamic (tools) |
| **Actions** | None | Can execute functions |
| **Real-time data** | ❌ | ✅ |
| **Complex tasks** | Single-step | Multi-step |
| **Explainability** | Black box | Transparent reasoning |
| **Error recovery** | ❌ | ✅ Can retry |
| **Cost** | Low | Higher (multiple calls) |
| **Latency** | Fast | Slower (iterations) |

---

**Phenomenal progress! 🎉**  
You've mastered one of the most powerful AI patterns - ReAct agents!

This is the foundation of:
- ChatGPT Plugins
- AutoGPT
- LangChain Agents
- Production AI assistants

Next: Day 8 mein **multi-step LLM chains** for complex workflows! 🚀
