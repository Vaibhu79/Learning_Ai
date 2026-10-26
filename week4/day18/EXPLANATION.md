# Day 18: AI Agent with Tool-Calling (Web Search + Calculator)

## 📋 Table of Contents
1. [Big Picture Overview](#big-picture-overview)
2. [Real-Life Analogy](#real-life-analogy)
3. [Prerequisites & Dependencies](#prerequisites--dependencies)
4. [Architecture Diagram](#architecture-diagram)
5. [Line-by-Line Code Explanation](#line-by-line-code-explanation)
6. [Execution Flow & Trace](#execution-flow--trace)
7. [Common Confusions & Clarifications](#common-confusions--clarifications)
8. [Common Mistakes & How to Avoid](#common-mistakes--how-to-avoid)
9. [Quick Review Section](#quick-review-section)
10. [Mental Model & Key Takeaways](#mental-model--key-takeaways)

---

## Big Picture Overview

### 🎯 Kya Hai Ye Day 18?

Day 18 mein hum **Tool-Calling AI Agent** banate hain jo **autonomously decide** karta hai ki kab web search karna hai aur kab calculator use karna hai. Ye ek complete **ReAct Agent** hai with real-world tools!

**What Makes This Special:**

```
Traditional LLM:
User: "What's Bitcoin price * 2?"
LLM: "Bitcoin is around $45,000, so 2x would be $90,000"
❌ Problem: Data outdated, math might be wrong

Tool-Calling Agent (Day 18):
User: "What's Bitcoin price * 2?"
Agent: "I need web search first"
         ↓
Agent calls: web_search("current Bitcoin price")
Result: "$67,234"
         ↓
Agent: "Now I need to calculate"
         ↓
Agent calls: calculate("67234 * 2")
Result: "134468"
         ↓
Agent: "Bitcoin is currently $67,234. Double that is $134,468."
✓ Current data + accurate calculation!
```

**Evolution Journey:**
```
Day 7: ReAct Chain (predefined steps)
         ↓
Day 8-9: LLM Chains (structured flow)
         ↓
Day 18: Tool-Calling Agent (autonomous decisions) ← We are here
         ↓
Production: Multi-tool agents with memory
```

### 🎓 Core Concepts

| Concept | Kya Hai | Example |
|---------|---------|---------|
| **Tool Calling** | LLM decides to use external tools | "I need to search the web" |
| **Tool Definition** | JSON schema describing tool | `{"name": "web_search", "parameters": {...}}` |
| **Tool Registry** | Mapping tool names to functions | `{"web_search": web_search_function}` |
| **Agent Loop** | Iterative: Think → Act → Observe | Max 5 iterations |
| **tool_choice** | How LLM selects tools | `"auto"` = LLM decides |

### 📊 What This Code Does

```
USER QUERY: "What's Bitcoin price and double it?"

Iteration 1:
LLM thinks: "I need current price → web search"
LLM calls: web_search("Bitcoin current price")
Result: "$67,234"
         ↓
Iteration 2:
LLM thinks: "Now I have price, need to calculate"
LLM calls: calculate("67234 * 2")
Result: "134468"
         ↓
Iteration 3:
LLM thinks: "I have all info, can answer"
LLM returns: "Bitcoin is currently $67,234. Double would be $134,468."
         ↓
DONE! Final answer returned.
```

---

## Real-Life Analogy

### 👨‍💼 Personal Research Assistant

Imagine tumne ek **smart assistant** hire kiya jo tumhare questions answer kare.

#### Traditional Assistant (No Tools):

```
You: "What's the weather in Delhi and should I carry an umbrella?"

Assistant (Without Tools):
"Based on my training data from 2023, Delhi typically has..."
❌ Problem: Outdated info, might rain today!

You: "What's 15% of 2500?"
Assistant: "Approximately 375"
❌ Problem: Not exact, might be calculation error
```

#### Tool-Calling Agent (This Code):

```
You: "What's the weather in Delhi and should I carry an umbrella?"

Agent (Internal thought): "I need current weather data"
Agent → Uses web_search("Delhi weather today")
Result: "Cloudy, 80% chance of rain, 28°C"
         ↓
Agent: "It's cloudy with 80% rain chance. Yes, carry an umbrella!"
✓ Current, accurate data!

You: "What's 15% of 2500?"
Agent (Internal thought): "This is a math problem"
Agent → Uses calculate("2500 * 0.15")
Result: "375.0"
         ↓
Agent: "15% of 2500 is exactly 375."
✓ Precise calculation!
```

### 🏢 Office Scenario

**You're a Manager, Agent is Your Junior:**

```
WITHOUT TOOLS (Dumb Junior):
You: "Get me competitor pricing for Product X"
Junior: "Umm, I think it was around $50 last year..."
You: "That's useless, go check!"

WITH TOOLS (Smart Junior):
You: "Get me competitor pricing for Product X"
Junior thinks: "I need to search online"
Junior → Opens browser → Searches → Finds info
Junior: "Here's current pricing:
  - Competitor A: $47.99
  - Competitor B: $52.50
  - Average: $50.25
  Source: [links]"
You: "Perfect!"

This is EXACTLY what tool-calling agent does:
- Recognizes need for external data
- Uses appropriate tool (web search)
- Returns structured answer with sources
```

### 🎯 Restaurant Ordering Analogy

```
CUSTOMER: "I want a burger combo, what's the price with 15% tip?"

WAITER WITHOUT TOOLS:
"Hmm, burger combo is maybe $12, and 15% of that is... around $1.80,
so total is about $13.80?"
❌ Vague, might be wrong

WAITER WITH TOOLS:
Waiter thinks: "Need to check exact price"
Waiter → Checks menu (tool 1)
Result: "$14.50"

Waiter thinks: "Now calculate tip"
Waiter → Uses calculator (tool 2)
Result: "$2.18"

Waiter: "Burger combo is $14.50, with 15% tip ($2.18) total is $16.68"
✓ Exact, reliable!

TOOLS:
- web_search = Check menu
- calculate = Calculator
- Agent loop = Waiter's thinking process
```

---

## Prerequisites & Dependencies

### Required Knowledge
```
✓ Day 7: ReAct Chain concept
✓ Day 8-9: LLM chains and structured flow
✓ JSON structure and parsing
✓ Python functions and dictionaries
✓ API calls and error handling
✓ Basic understanding of LLM capabilities
```

### Python Libraries

```toml
[project]
dependencies = [
    "groq>=0.4.1",           # LLM API with tool-calling support
    "tavily-python>=0.3.0",  # Web search API
    "python-dotenv>=1.0.0",  # Environment variables
]
```

**Installation:**
```bash
uv add groq python-dotenv tavily-python
# or
pip install groq tavily-python python-dotenv
```

### API Keys Required

```bash
# .env file
GROQ_API_KEY=gsk_your_groq_api_key_here
TAVILY_API_KEY=tvly_your_tavily_api_key_here
```

**Where to Get:**
- Groq: https://console.groq.com/keys
- Tavily: https://tavily.com/ (web search API)

### What is Tavily?

```
Tavily = Search API optimized for LLMs

Why not Google?
- Google returns HTML, ads, lots of noise
- Tavily returns clean, LLM-friendly summaries
- Designed specifically for AI agents

Example:
Query: "Bitcoin price"
Google: 10 pages of links, ads, news
Tavily: "Title: Bitcoin Price Today
         Content: Bitcoin is trading at $67,234 as of..."
         Clean, structured, ready for LLM!
```

---

## Architecture Diagram

### Complete Agent System

```
┌──────────────────────────────────────────────────────────┐
│                    USER QUERY                             │
│  "What's Bitcoin price and calculate 15% of it?"         │
└──────────────────────────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────┐
│                    AGENT LOOP                             │
│                  (max 5 iterations)                       │
└──────────────────────────────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
    ┌─────────┐     ┌─────────┐     ┌─────────┐
    │  GROQ   │     │  TAVILY │     │CALCULATOR│
    │   LLM   │     │ (Search)│     │  (eval) │
    │         │     │         │     │         │
    └─────────┘     └─────────┘     └─────────┘
          │               │               │
          └───────────────┼───────────────┘
                          ▼
                  
ITERATION 1:
┌────────────────────────────────────────────────┐
│ LLM Thinks: "Need current Bitcoin price"      │
│ LLM Returns: tool_call(web_search, ...)       │
└────────────────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────────┐
│ Agent executes: web_search("Bitcoin price")   │
│ Tavily returns: "$67,234"                     │
└────────────────────────────────────────────────┘
                    │
                    ▼
ITERATION 2:
┌────────────────────────────────────────────────┐
│ LLM Thinks: "Got price, now calculate 15%"    │
│ LLM Returns: tool_call(calculate, ...)        │
└────────────────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────────┐
│ Agent executes: calculate("67234 * 0.15")     │
│ Calculator returns: "10085.1"                  │
└────────────────────────────────────────────────┘
                    │
                    ▼
ITERATION 3:
┌────────────────────────────────────────────────┐
│ LLM Thinks: "I have all info, can answer"     │
│ LLM Returns: NO tool_calls (final answer)     │
│ Content: "Bitcoin is $67,234, 15% is $10,085" │
└────────────────────────────────────────────────┘
                    │
                    ▼
            ┌──────────────┐
            │FINAL ANSWER  │
            │  to User     │
            └──────────────┘
```

### Message Flow in Detail

```
messages = [
  {"role": "system", "content": "You are a research assistant..."},
  {"role": "user", "content": "What's Bitcoin price * 0.15?"}
]
         ↓
┌─────────────────────────────────────────────────────────┐
│              ITERATION 1: LLM CALL #1                    │
├─────────────────────────────────────────────────────────┤
│ Input: messages + tools definition                      │
│ Output: tool_call(web_search, {"query": "Bitcoin"})   │
└─────────────────────────────────────────────────────────┘
         ↓
messages.append(LLM response with tool_call)
         ↓
Execute: web_search("Bitcoin price")
Result: "$67,234"
         ↓
messages.append({"role": "tool", "content": "$67,234"})
         ↓
messages = [
  {"role": "system", "content": "..."},
  {"role": "user", "content": "What's Bitcoin price * 0.15?"},
  {"role": "assistant", "tool_calls": [...]},
  {"role": "tool", "content": "$67,234"}
]
         ↓
┌─────────────────────────────────────────────────────────┐
│              ITERATION 2: LLM CALL #2                    │
├─────────────────────────────────────────────────────────┤
│ Input: messages (now with search result)               │
│ Output: tool_call(calculate, {"expression": "67234*0.15"})│
└─────────────────────────────────────────────────────────┘
         ↓
Execute: calculate("67234 * 0.15")
Result: "10085.1"
         ↓
messages.append({"role": "tool", "content": "10085.1"})
         ↓
messages = [
  ... (previous messages) ...,
  {"role": "assistant", "tool_calls": [...]},
  {"role": "tool", "content": "10085.1"}
]
         ↓
┌─────────────────────────────────────────────────────────┐
│              ITERATION 3: LLM CALL #3                    │
├─────────────────────────────────────────────────────────┤
│ Input: messages (with both results)                    │
│ Output: NO tool_calls, just content                    │
│ Content: "Bitcoin is $67,234. 15% is $10,085.10"      │
└─────────────────────────────────────────────────────────┘
         ↓
    DONE! Return final answer
```

### Tool Definition Structure

```
TOOL DEFINITION (JSON):
┌──────────────────────────────────────┐
│ {                                    │
│   "type": "function",               │
│   "function": {                     │
│     "name": "web_search",           │ ← LLM calls this
│     "description": "Search web...", │ ← When to use
│     "parameters": {                 │
│       "type": "object",             │
│       "properties": {               │
│         "query": {                  │ ← Required args
│           "type": "string",         │
│           "description": "..."      │
│         }                           │
│       },                            │
│       "required": ["query"]         │ ← Must provide
│     }                               │
│   }                                 │
│ }                                   │
└──────────────────────────────────────┘
         │
         ▼
PYTHON FUNCTION:
┌──────────────────────────────────────┐
│ def web_search(query: str) -> str:  │
│     # Actual implementation          │
│     return tavily.search(query)      │
└──────────────────────────────────────┘
         │
         ▼
TOOL REGISTRY:
┌──────────────────────────────────────┐
│ AVAILABLE_TOOLS = {                  │
│   "web_search": web_search,          │ ← Links name to function
│   "calculate": calculate              │
│ }                                    │
└──────────────────────────────────────┘

When LLM says: tool_call("web_search", {"query": "test"})
Agent finds: AVAILABLE_TOOLS["web_search"]
Agent calls: web_search(query="test")
```

---

## Line-by-Line Code Explanation

### Part 1: Imports & Setup

```python
import os
import json

from dotenv import load_dotenv
from groq import Groq
from tavily import TavilyClient
```

**Import Breakdown:**

| Import | Purpose | Used For |
|--------|---------|----------|
| `os` | Environment variables | `os.getenv()` |
| `json` | Parse JSON | Parse tool call arguments |
| `load_dotenv` | Load .env file | Get API keys |
| `Groq` | LLM with tool-calling | Main agent brain |
| `TavilyClient` | Web search API | Get current information |

---

### Part 2: Initialize Clients

```python
load_dotenv()

groq = Groq(api_key=os.getenv("GROQ_API_KEY"))
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
```

**What Happens:**

```
1. load_dotenv()
   ↓
   Reads .env file
   ↓
   Sets environment variables

2. os.getenv("GROQ_API_KEY")
   ↓
   Returns: "gsk_abc123..."
   ↓
   groq = Groq(api_key="gsk_abc123...")

3. os.getenv("TAVILY_API_KEY")
   ↓
   Returns: "tvly_xyz789..."
   ↓
   tavily = TavilyClient(api_key="tvly_xyz789...")

Result: Both clients ready to use!
```

---

### Part 3: Tool 1 - Web Search

```python
def web_search(query: str) -> str:
    """Search the web for current information."""

    try:
        response = tavily.search(
            query=query,
            max_results=3,
            search_depth="basic"
        )

        results = []

        for result in response["results"]:
            results.append(
                f"Title: {result['title']}\n"
                f"URL: {result['url']}\n"
                f"Content: {result['content']}"
            )

        return "\n\n".join(results)

    except Exception as e:
        return f"Search failed: {e}"
```

**Function Breakdown:**

```python
web_search(query: str) -> str
#          │            │
#          │            └─ Returns: formatted search results
#          └─ Input: search query (e.g., "Bitcoin price")
```

**Tavily Search Parameters:**

```python
tavily.search(
    query="Bitcoin price",     # What to search
    max_results=3,              # Get top 3 results
    search_depth="basic"        # "basic" or "advanced"
)
```

**Response Structure:**

```python
response = {
    "results": [
        {
            "title": "Bitcoin Price Today - CoinDesk",
            "url": "https://coindesk.com/price/bitcoin",
            "content": "Bitcoin is currently trading at $67,234, up 2.3% today..."
        },
        {
            "title": "BTC Price Live",
            "url": "https://crypto.com/bitcoin",
            "content": "Bitcoin (BTC) price is $67,230. Market cap $1.3T..."
        },
        {
            "title": "Bitcoin - Wikipedia",
            "url": "https://en.wikipedia.org/wiki/Bitcoin",
            "content": "Bitcoin is a decentralized digital currency..."
        }
    ]
}
```

**Formatted Output:**

```
Title: Bitcoin Price Today - CoinDesk
URL: https://coindesk.com/price/bitcoin
Content: Bitcoin is currently trading at $67,234, up 2.3% today...

Title: BTC Price Live
URL: https://crypto.com/bitcoin
Content: Bitcoin (BTC) price is $67,230. Market cap $1.3T...

Title: Bitcoin - Wikipedia
URL: https://en.wikipedia.org/wiki/Bitcoin
Content: Bitcoin is a decentralized digital currency...
```

**Error Handling:**

```python
try:
    # Search
except Exception as e:
    return f"Search failed: {e}"
# Returns error message instead of crashing
```

---

### Part 4: Tool 2 - Calculator

```python
def calculate(expression: str) -> str:
    """Perform a mathematical calculation."""

    try:
        return str(
            eval(
                expression,
                {"__builtins__": {}},
                {}
            )
        )
    except Exception as e:
        return f"Calculation failed: {e}"
```

**Function Breakdown:**

```python
calculate(expression: str) -> str
#         │                    │
#         │                    └─ Returns: result as string
#         └─ Input: math expression (e.g., "2500 * 0.15")
```

**Safe eval() Usage:**

```python
eval(
    expression,           # "2500 * 0.15"
    {"__builtins__": {}}, # Disable built-in functions (security)
    {}                    # Empty local namespace
)
```

**Why This is (Relatively) Safe:**

```python
# Dangerous (without restrictions):
eval("__import__('os').system('rm -rf /')")  # Could delete files!

# Safe (with restrictions):
eval(
    "__import__('os').system('rm -rf /')",
    {"__builtins__": {}},  # No __import__ available
    {}
)
# Raises: NameError: name '__import__' is not defined

# Works fine for math:
eval("2500 * 0.15", {"__builtins__": {}}, {})
# Returns: 375.0
```

**⚠️ Security Note:**

```
This is safer than raw eval(), but still has risks:
- Don't expose to untrusted user input directly
- LLM generates the expression (trusted source)
- Production: Use ast.literal_eval() or math parser library

Why we use it here:
- Simple demo/learning code
- LLM is the one calling it (not random users)
- Good enough for controlled environments
```

**Examples:**

```python
calculate("2 + 2")           # "4"
calculate("100 * 0.15")      # "15.0"
calculate("(50 + 30) / 2")   # "40.0"
calculate("2 ** 10")         # "1024" (power)
calculate("sqrt(16)")        # Error: name 'sqrt' not defined
```

---

### Part 5: Tool Registry

```python
AVAILABLE_TOOLS = {
    "web_search": web_search,
    "calculate": calculate,
}
```

**What is Tool Registry:**

```
It's a dictionary mapping tool NAMES to actual FUNCTIONS

When LLM says: "Call tool named 'web_search'"
Agent looks up: AVAILABLE_TOOLS["web_search"]
Agent gets: The actual web_search function
Agent calls: web_search(query="...")

Without registry:
Agent: "LLM wants 'web_search'"
Agent: "Uhh, what's that? Where is the function?"
❌ Can't find it!

With registry:
Agent: "LLM wants 'web_search'"
Agent: AVAILABLE_TOOLS["web_search"]  # Found it!
Agent: web_search(...)  # Call it!
✓ Works!
```

**Why Not Just Use Function Names Directly:**

```python
# Bad approach:
tool_name = "web_search"
# How to call function from string?
# Can't do: "web_search"(query)  ❌

# Good approach (registry):
tool_name = "web_search"
func = AVAILABLE_TOOLS[tool_name]
result = func(query="test")  ✓
```

---

### Part 6: Tool Definitions for LLM

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            
            "description": (
                "Search the web for current information, "
                "news, recent events, prices, statistics, "
                "or facts that may have changed."
            ),
            
            "parameters": {
                "type": "object",
                
                "properties": {
                    "query": {
                        "type": "string",
                        "description": (
                            "A specific and concise "
                            "web search query."
                        )
                    }
                },
                
                "required": ["query"]
            }
        }
    },
    # ... (calculate tool similar structure)
]
```

**This is THE MOST IMPORTANT part! Let's break it down:**

**Level 1: Tool Type**

```python
{
    "type": "function",  # This tool is a Python function
    "function": {        # Function details below
        ...
    }
}
```

**Level 2: Function Metadata**

```python
"function": {
    "name": "web_search",  # LLM will call this exact name
    
    "description": (       # When should LLM use this tool?
        "Search the web for current information, "
        "news, recent events, prices, statistics, "
        "or facts that may have changed."
    ),
    
    "parameters": {...}    # What arguments does it need?
}
```

**Why Description Matters:**

```
LLM reads description to decide WHEN to use tool:

User query: "What's Bitcoin price?"
LLM thinks: "This is current information, prices... matches web_search description!"
LLM calls: web_search

User query: "What's 2+2?"
LLM thinks: "This is calculation, matches calculate description"
LLM calls: calculate

User query: "What's capital of France?"
LLM thinks: "This is static fact, I know it's Paris. No tool needed."
LLM returns: "Paris"
```

**Level 3: Parameters Schema**

```python
"parameters": {
    "type": "object",      # Arguments are a JSON object
    
    "properties": {        # List of argument fields
        "query": {         # Argument name
            "type": "string",  # Data type
            "description": (   # What is this argument?
                "A specific and concise web search query."
            )
        }
    },
    
    "required": ["query"]  # Which arguments are mandatory?
}
```

**How LLM Uses This:**

```
LLM sees parameters schema:
{
    "properties": {
        "query": {"type": "string", ...}
    },
    "required": ["query"]
}

LLM generates tool call:
{
    "name": "web_search",
    "arguments": {
        "query": "Bitcoin current price"  ← Must be string
    }
}

Agent receives and validates:
- Has "query" field? ✓
- Is it a string? ✓
- Calls: web_search(query="Bitcoin current price")
```

**Complete Tool Definition (Calculate):**

```python
{
    "type": "function",
    "function": {
        "name": "calculate",
        
        "description": (
            "Perform mathematical calculations "
            "such as percentages, multiplication, "
            "division, or arithmetic."
        ),
        
        "parameters": {
            "type": "object",
            
            "properties": {
                "expression": {
                    "type": "string",
                    "description": (
                        "A mathematical expression "
                        "such as '2500 * 0.15'."
                    )
                }
            },
            
            "required": ["expression"]
        }
    }
}
```

---

### Part 7: System Prompt

```python
SYSTEM_PROMPT = """
You are a research assistant.

Rules:

1. Use web_search for current or changing information.
2. Use calculate for mathematical calculations.
3. You may use tools multiple times.
4. When you have enough information, answer the user.
5. Include useful source URLs from web search results.
"""
```

**Why System Prompt Matters:**

```
Without clear instructions:
User: "What's Bitcoin price * 2?"
LLM: "Hmm, I'll try to answer from memory: around $90,000?"
❌ Not using tools!

With system prompt:
User: "What's Bitcoin price * 2?"
LLM: "I need web_search first, then calculate"
LLM: web_search("Bitcoin price") → calculate("67234 * 2")
LLM: "$134,468"
✓ Using tools correctly!
```

**Rule-by-Rule Breakdown:**

1. **"Use web_search for current or changing information"**
   ```
   Tells LLM: Don't guess prices, dates, news - search!
   ```

2. **"Use calculate for mathematical calculations"**
   ```
   Tells LLM: Don't approximate math - use calculator!
   ```

3. **"You may use tools multiple times"**
   ```
   Tells LLM: It's OK to call web_search twice if needed
   Example: Search for "Bitcoin" then search for "Ethereum"
   ```

4. **"When you have enough information, answer the user"**
   ```
   Tells LLM: Don't keep calling tools forever - know when to stop
   ```

5. **"Include useful source URLs from web search results"**
   ```
   Tells LLM: Cite your sources for credibility
   Output: "According to CoinDesk (coindesk.com), Bitcoin is $67,234"
   ```

---

### Part 8: Agent Loop Function

```python
def run_agent(question: str, max_iterations: int = 5):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": question
        }
    ]

    for iteration in range(max_iterations):

        print(f"\n--- Iteration {iteration + 1} ---")

        response = groq.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        messages.append(message)

        # NO TOOL → FINAL ANSWER
        if not message.tool_calls:
            print("\nFINAL ANSWER:")
            print(message.content)
            return message.content

        # TOOL CALL(S)
        print(f"LLM requested {len(message.tool_calls)} tool(s)")

        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments
            )

            print(f"Tool: {tool_name}")
            print(f"Arguments: {arguments}")

            if tool_name not in AVAILABLE_TOOLS:
                result = f"Unknown tool: {tool_name}"
            else:
                result = AVAILABLE_TOOLS[tool_name](**arguments)

            print("Tool result received.")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

    print("\nMaximum iterations reached.")
    return "I couldn't complete the task within the iteration limit."
```

**This is the HEART of the agent! Let's break it down step by step:**

**Step 1: Initialize Messages**

```python
messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT  # Instructions for LLM
    },
    {
        "role": "user",
        "content": question  # User's actual question
    }
]
```

**Step 2: Iteration Loop**

```python
for iteration in range(max_iterations):
#                       │
#                       └─ Default: 5 attempts max
```

**Why max_iterations:**

```
Prevents infinite loops:

Bad scenario (without limit):
Iteration 1: LLM calls web_search
Iteration 2: LLM calls web_search again (same query)
Iteration 3: LLM calls web_search again
... (forever)

With limit:
After 5 iterations: "Maximum iterations reached" → Stop
```

**Step 3: Call LLM**

```python
response = groq.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=messages,              # Conversation history
    tools=tools,                    # Available tools
    tool_choice="auto"              # LLM decides when to use tools
)
```

**tool_choice Options:**

```python
tool_choice="auto"      # LLM decides (recommended)
tool_choice="none"      # Never use tools
tool_choice="required"  # Must use a tool
tool_choice={"type": "function", "function": {"name": "web_search"}}  # Force specific tool
```

**Step 4: Extract Message**

```python
message = response.choices[0].message
messages.append(message)  # Add to conversation history
```

**What's in message:**

```python
# If LLM wants to use tool:
message = {
    "role": "assistant",
    "content": null,
    "tool_calls": [
        {
            "id": "call_abc123",
            "function": {
                "name": "web_search",
                "arguments": '{"query": "Bitcoin price"}'
            }
        }
    ]
}

# If LLM has final answer:
message = {
    "role": "assistant",
    "content": "Bitcoin is currently $67,234.",
    "tool_calls": null
}
```

**Step 5: Check for Final Answer**

```python
if not message.tool_calls:
    print("\nFINAL ANSWER:")
    print(message.content)
    return message.content  # Done! Exit loop
```

**Step 6: Process Tool Calls**

```python
for tool_call in message.tool_calls:
    
    tool_name = tool_call.function.name  # "web_search"
    
    arguments = json.loads(
        tool_call.function.arguments  # '{"query": "Bitcoin"}'
    )
    # arguments = {"query": "Bitcoin"}
    
    print(f"Tool: {tool_name}")
    print(f"Arguments: {arguments}")
```

**Step 7: Execute Tool**

```python
if tool_name not in AVAILABLE_TOOLS:
    result = f"Unknown tool: {tool_name}"
else:
    result = AVAILABLE_TOOLS[tool_name](**arguments)
    #                                    │
    #                                    └─ ** unpacks dict to kwargs
    #                                       {"query": "Bitcoin"} → query="Bitcoin"
```

**kwargs Unpacking Example:**

```python
arguments = {"query": "Bitcoin price"}

# Without **:
web_search(arguments)  # ❌ Wrong: passes dict as first arg

# With **:
web_search(**arguments)  # ✓ Correct: web_search(query="Bitcoin price")

# Equivalent to:
web_search(query=arguments["query"])
```

**Step 8: Add Tool Result to Messages**

```python
messages.append({
    "role": "tool",
    "tool_call_id": tool_call.id,  # Links to original tool call
    "content": result               # Tool output
})
```

**Message History After Tool Call:**

```python
messages = [
    {"role": "system", "content": "You are a research assistant..."},
    {"role": "user", "content": "What's Bitcoin price?"},
    {"role": "assistant", "tool_calls": [...]},  # LLM requested tool
    {"role": "tool", "tool_call_id": "call_abc123", "content": "$67,234"}  # Tool result
]

# Next iteration: LLM sees this full history and can now answer!
```

---

### Part 9: Main Execution

```python
if __name__ == "__main__":

    print("=" * 60)
    print("AI RESEARCH AGENT")
    print("=" * 60)

    question = input("\nAsk me anything: ")

    run_agent(question)
```

**What This Does:**

```
1. Print banner:
   ============================================================
   AI RESEARCH AGENT
   ============================================================

2. Get user input:
   Ask me anything: What's Bitcoin price * 2?

3. Run agent:
   run_agent("What's Bitcoin price * 2?")
   
   --- Iteration 1 ---
   LLM requested 1 tool(s)
   Tool: web_search
   Arguments: {'query': 'Bitcoin current price'}
   Tool result received.
   
   --- Iteration 2 ---
   LLM requested 1 tool(s)
   Tool: calculate
   Arguments: {'expression': '67234 * 2'}
   Tool result received.
   
   --- Iteration 3 ---
   FINAL ANSWER:
   Bitcoin is currently $67,234. Double that would be $134,468.
```

---

## Execution Flow & Trace

### Complete Execution Example

**User Query:** "What's the current price of Bitcoin and calculate 15% of it?"

```
┌──────────────────────────────────────────────────────────┐
│                    START PROGRAM                          │
└──────────────────────────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────┐
│ INITIALIZATION                                            │
├──────────────────────────────────────────────────────────┤
│ 1. Load .env file                                        │
│ 2. Initialize Groq client (LLM)                          │
│ 3. Initialize Tavily client (Search)                     │
│ 4. Define tools: web_search, calculate                   │
│ 5. Create tool definitions for LLM                       │
└──────────────────────────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────┐
│ USER INPUT                                                │
├──────────────────────────────────────────────────────────┤
│ Ask me anything: What's Bitcoin price and 15% of it?    │
└──────────────────────────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────┐
│ CREATE INITIAL MESSAGES                                   │
├──────────────────────────────────────────────────────────┤
│ messages = [                                             │
│   {role: "system", content: "You are a research..."},   │
│   {role: "user", content: "What's Bitcoin price and     │
│                             15% of it?"}                 │
│ ]                                                        │
└──────────────────────────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────┐
│ ITERATION 1                                               │
├──────────────────────────────────────────────────────────┤
│ Print: "--- Iteration 1 ---"                            │
│                                                          │
│ Call Groq LLM:                                           │
│   Input: messages + tools                                │
│   Model thinks: "I need current Bitcoin price"          │
│   Returns: tool_call(web_search, {"query": "Bitcoin"}) │
│                                                          │
│ Print: "LLM requested 1 tool(s)"                        │
│ Print: "Tool: web_search"                               │
│ Print: "Arguments: {'query': 'Bitcoin current price'}"  │
│                                                          │
│ Execute: web_search("Bitcoin current price")            │
│   → Tavily API call                                     │
│   → Returns: "Title: Bitcoin Price...\nContent: $67,234"│
│                                                          │
│ Print: "Tool result received."                          │
│                                                          │
│ Append to messages:                                      │
│   {role: "assistant", tool_calls: [...]},               │
│   {role: "tool", content: "$67,234 ..."}                │
└──────────────────────────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────┐
│ ITERATION 2                                               │
├──────────────────────────────────────────────────────────┤
│ Print: "--- Iteration 2 ---"                            │
│                                                          │
│ Call Groq LLM:                                           │
│   Input: messages (now with Bitcoin price data)          │
│   Model thinks: "Got price: $67,234. Now calculate 15%"│
│   Returns: tool_call(calculate, {"expression":          │
│                                  "67234 * 0.15"})       │
│                                                          │
│ Print: "LLM requested 1 tool(s)"                        │
│ Print: "Tool: calculate"                                │
│ Print: "Arguments: {'expression': '67234 * 0.15'}"     │
│                                                          │
│ Execute: calculate("67234 * 0.15")                      │
│   → eval("67234 * 0.15", {}, {})                       │
│   → Returns: "10085.1"                                  │
│                                                          │
│ Print: "Tool result received."                          │
│                                                          │
│ Append to messages:                                      │
│   {role: "assistant", tool_calls: [...]},               │
│   {role: "tool", content: "10085.1"}                    │
└──────────────────────────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────┐
│ ITERATION 3                                               │
├──────────────────────────────────────────────────────────┤
│ Print: "--- Iteration 3 ---"                            │
│                                                          │
│ Call Groq LLM:                                           │
│   Input: messages (with price + calculation)             │
│   Model thinks: "I have all info: price and 15%"        │
│   Returns: NO tool_calls                                 │
│           content: "Bitcoin is currently trading at      │
│                     $67,234. 15% of that is $10,085.10" │
│                                                          │
│ Check: message.tool_calls?                               │
│   → No tool_calls! This is final answer.                │
│                                                          │
│ Print: "FINAL ANSWER:"                                   │
│ Print: "Bitcoin is currently trading at $67,234.        │
│         15% of that is $10,085.10."                     │
│                                                          │
│ Return answer → Exit function                            │
└──────────────────────────────────────────────────────────┘
                          │
                          ▼
                  ┌──────────────┐
                  │ PROGRAM END  │
                  └──────────────┘
```

### Sample Console Output

```
============================================================
AI RESEARCH AGENT
============================================================

Ask me anything: What's Bitcoin price and calculate 15% of it?

--- Iteration 1 ---
LLM requested 1 tool(s)
Tool: web_search
Arguments: {'query': 'Bitcoin current price'}
Tool result received.

--- Iteration 2 ---
LLM requested 1 tool(s)
Tool: calculate
Arguments: {'expression': '67234 * 0.15'}
Tool result received.

--- Iteration 3 ---

FINAL ANSWER:
Bitcoin is currently trading at $67,234. 15% of that amount would be $10,085.10.

Source: CoinDesk (https://coindesk.com/price/bitcoin)
```

---

## Common Confusions & Clarifications

### Confusion 1: Tool Definition vs Tool Implementation

**❓ Question:** "Tool definition aur actual function mein kya difference hai?"

**💡 Answer:**

```python
# TOOL DEFINITION (for LLM):
tools = [{
    "type": "function",
    "function": {
        "name": "web_search",           # ← Name LLM uses
        "description": "Search web...", # ← When to use
        "parameters": {...}             # ← What arguments
    }
}]

# Purpose: Tell LLM about tool capabilities
# Language: JSON (LLM-readable)
# Contains: Metadata, no actual code


# TOOL IMPLEMENTATION (actual function):
def web_search(query: str) -> str:  # ← Actual Python code
    response = tavily.search(query)  # ← Real API call
    return format_results(response)  # ← Processing logic

# Purpose: Execute the actual task
# Language: Python
# Contains: Real implementation


# LINKING (registry):
AVAILABLE_TOOLS = {
    "web_search": web_search  # Links name to function
}

Flow:
1. LLM reads tool definition → Knows web_search exists
2. LLM generates: tool_call("web_search", {"query": "..."})
3. Agent looks up: AVAILABLE_TOOLS["web_search"]
4. Agent calls: web_search(query="...")
5. Python function executes → Returns result
```

**Analogy:**

```
Tool Definition = Restaurant Menu
- "Burger: Grilled beef patty with cheese ($10)"
- Describes what it is, what's in it, price
- Customer (LLM) reads this to decide

Tool Implementation = Kitchen Recipe
- "1. Grill patty for 5 min each side
   2. Add cheese, melt 1 min
   3. Assemble with bun"
- Actual cooking instructions
- Chef (Python) follows this

Tool Registry = Kitchen Staff List
- "Burger: Chef John"
- Links menu item to specific chef
```

---

### Confusion 2: Why Use eval() for Calculator?

**❓ Question:** "`eval()` dangerous hai, fir kyun use kar rahe hain?"

**💡 Answer:**

**Why eval() is Normally Dangerous:**

```python
# User input (malicious):
user_input = "__import__('os').system('rm -rf /')"

eval(user_input)  # ❌ DISASTER! Deletes entire system!
```

**Why It's (Relatively) Safe Here:**

```python
# 1. Restricted environment:
eval(
    expression,
    {"__builtins__": {}},  # No dangerous functions
    {}
)

# 2. LLM generates input (not random users):
# LLM: "I need to calculate 2500 * 0.15"
# LLM generates: {"expression": "2500 * 0.15"}
# This is trusted input (from your own LLM)

# 3. Still fails on dangerous code:
eval("__import__('os')", {"__builtins__": {}}, {})
# Error: NameError: name '__import__' is not defined ✓
```

**Production Alternatives:**

```python
# Option 1: ast.literal_eval (safest, but limited):
import ast
ast.literal_eval("2 + 2")  # ✓ Works
ast.literal_eval("2 + 2 * 3")  # ❌ Doesn't work (not a literal)

# Option 2: Math parser library:
from simpleeval import simple_eval
simple_eval("2 + 2 * 3")  # ✓ Safe and powerful

# Option 3: sympy:
from sympy import sympify
sympify("2 + 2 * 3").evalf()  # ✓ Safe, supports complex math
```

**Recommendation:**

```python
# For learning (Day 18): eval() with restrictions is OK
# For production: Use simpleeval or sympy
```

---

### Confusion 3: Kab Tool Use Hoga Aur Kab Nahi?

**❓ Question:** "LLM kaise decide karta hai ki tool use karein ya nahi?"

**💡 Answer:**

**Decision Process:**

```
LLM reads:
1. User question
2. Tool descriptions
3. System prompt

Then decides:
- Do I already know the answer? → No tool
- Do I need current data? → web_search
- Do I need calculation? → calculate
- Do I need both? → Both tools (multiple iterations)
```

**Examples:**

```python
# Example 1: No tool needed
User: "What's capital of France?"
LLM thinks: "I know this: Paris. No tool needed."
LLM returns: "The capital of France is Paris."

# Example 2: Tool needed
User: "What's Bitcoin price?"
LLM thinks: "This is current price, changes constantly. Need web_search."
LLM calls: web_search("Bitcoin current price")

# Example 3: Both tools
User: "What's Bitcoin price * 2?"
Iteration 1:
  LLM: "Need current price first"
  LLM: web_search("Bitcoin price")
Iteration 2:
  LLM: "Got price: $67,234. Now calculate."
  LLM: calculate("67234 * 2")
Iteration 3:
  LLM: "Got both results. Can answer now."
  LLM: "$134,468"
```

**What Influences Decision:**

```python
# 1. Tool description (most important):
"description": "Search the web for CURRENT information, prices..."
# Keywords: "current", "prices" → LLM knows when to use

# 2. System prompt:
"Use web_search for current or changing information"
# Explicit instruction

# 3. Parameter descriptions:
"query": "A specific and concise web search query"
# LLM learns to format queries properly

# 4. LLM's training:
# GPT models are trained to understand when to use tools
```

---

### Confusion 4: Multiple Tool Calls in One Iteration?

**❓ Question:** "Kya LLM ek iteration mein multiple tools call kar sakta hai?"

**💡 Answer: YES!**

```python
# Example: LLM calls both tools at once
User: "Search for Bitcoin price and also Ethereum price"

Iteration 1:
LLM returns:
{
    "tool_calls": [
        {
            "function": {"name": "web_search", "arguments": '{"query": "Bitcoin"}'}
        },
        {
            "function": {"name": "web_search", "arguments": '{"query": "Ethereum"}'}
        }
    ]
}

# Agent processes BOTH tool calls:
for tool_call in message.tool_calls:
    # First iteration: Bitcoin search
    # Second iteration: Ethereum search
    ...

# Then LLM gets BOTH results and can answer
```

**Code Handles This:**

```python
for tool_call in message.tool_calls:  # ← Loop handles multiple
    tool_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)
    
    result = AVAILABLE_TOOLS[tool_name](**arguments)
    
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,  # ← Unique ID for each
        "content": result
    })
```

---

### Confusion 5: tool_choice="auto" Kya Karta Hai?

**❓ Question:** "`tool_choice` ke different options ka matlab?"

**💡 Answer:**

```python
# Option 1: "auto" (default, recommended)
tool_choice="auto"
# LLM decides: Use tool, don't use tool, or multiple tools
# Most flexible

User: "What's 2+2?"
LLM: "I know this: 4" (no tool)

User: "What's Bitcoin price?"
LLM: web_search(...) (uses tool)


# Option 2: "none"
tool_choice="none"
# LLM will NEVER use tools
# Even if it needs current data!

User: "What's Bitcoin price?"
LLM: "Based on my training data, Bitcoin is around $40,000"
❌ Outdated, wrong!


# Option 3: "required"
tool_choice="required"
# LLM MUST use a tool (at least one)
# Even for simple questions

User: "What's 2+2?"
LLM: calculate("2+2")  # Forced to use tool
Result: "4"
# Works but unnecessary overhead


# Option 4: Specific tool
tool_choice={
    "type": "function",
    "function": {"name": "web_search"}
}
# LLM MUST use web_search specifically

User: "What's 2+2?"
LLM: web_search("2+2 calculation")  # Forced!
❌ Wrong tool for the job!
```

**When to Use What:**

```python
# Development/Production (default):
tool_choice="auto"  # LLM decides intelligently

# Testing specific tool:
tool_choice={"type": "function", "function": {"name": "web_search"}}

# Pure chatbot (no tools):
tool_choice="none"

# Force tool use (rare):
tool_choice="required"
```

---

## Common Mistakes & How to Avoid

### Mistake 1: Forgetting Tool Registry

**❌ Wrong:**

```python
# Define tools
def web_search(query):
    ...

# Define tool definitions
tools = [{"function": {"name": "web_search", ...}}]

# Run agent
run_agent(question)

# Inside agent:
tool_name = "web_search"
result = tool_name(query)  # ❌ Can't call string!
```

**✓ Correct:**

```python
# Define tools
def web_search(query):
    ...

# CREATE REGISTRY
AVAILABLE_TOOLS = {
    "web_search": web_search  # Map name to function
}

# Inside agent:
tool_name = "web_search"
func = AVAILABLE_TOOLS[tool_name]  # Get function
result = func(query)  # ✓ Call function
```

---

### Mistake 2: Tool Name Mismatch

**❌ Wrong:**

```python
# Function name:
def web_search(...):
    ...

# Tool definition (different name):
tools = [{
    "function": {
        "name": "search_web",  # ❌ Different!
        ...
    }
}]

# Registry:
AVAILABLE_TOOLS = {
    "web_search": web_search  # ❌ Name doesn't match definition
}

# Result: LLM calls "search_web", but registry has "web_search"
# Error: Unknown tool!
```

**✓ Correct:**

```python
# Keep names consistent everywhere:

def web_search(...):  # ← Name 1

tools = [{
    "function": {
        "name": "web_search",  # ← Same name
        ...
    }
}]

AVAILABLE_TOOLS = {
    "web_search": web_search  # ← Same name
}
```

---

### Mistake 3: Not Handling Tool Errors

**❌ Wrong:**

```python
def web_search(query: str) -> str:
    response = tavily.search(query)  # What if API fails?
    return format_results(response)  # Crash!

# If Tavily API is down:
# Exception: ConnectionError
# Agent crashes ❌
```

**✓ Correct:**

```python
def web_search(query: str) -> str:
    try:
        response = tavily.search(query)
        return format_results(response)
    except Exception as e:
        return f"Search failed: {e}"  # Return error as string
        
# Now LLM sees: "Search failed: Connection timeout"
# LLM can respond: "Sorry, web search is currently unavailable"
# Agent continues ✓
```

---

### Mistake 4: Infinite Tool Calling

**❌ Wrong:**

```python
# No max_iterations limit:
while True:
    response = groq.chat.completions.create(...)
    
    if not response.message.tool_calls:
        break
    
    # Execute tools...
    
# If LLM keeps calling tools forever:
# Loop never ends! ❌
```

**✓ Correct:**

```python
max_iterations = 5  # Safety limit

for iteration in range(max_iterations):
    response = groq.chat.completions.create(...)
    
    if not response.message.tool_calls:
        break
    
    # Execute tools...

# After 5 iterations:
print("Maximum iterations reached")
return "Task couldn't be completed"
```

---

### Mistake 5: Not Appending Tool Results Correctly

**❌ Wrong:**

```python
# Execute tool
result = web_search(query)

# Wrong format:
messages.append({
    "role": "assistant",  # ❌ Wrong role!
    "content": result
})

# Or:
messages.append({
    "role": "tool",
    "content": result  # ❌ Missing tool_call_id!
})
```

**✓ Correct:**

```python
# Execute tool
result = web_search(query)

# Correct format:
messages.append({
    "role": "tool",        # ✓ Correct role
    "tool_call_id": tool_call.id,  # ✓ Links to original call
    "content": result      # ✓ Tool output
})

# Why tool_call_id matters:
# LLM can match result to specific tool call
# Important when multiple tools called
```

---

## Quick Review Section

### Key Components

| Component | Purpose | Example |
|-----------|---------|---------|
| **Tool Function** | Actual implementation | `def web_search(query): ...` |
| **Tool Definition** | JSON schema for LLM | `{"name": "web_search", "parameters": ...}` |
| **Tool Registry** | Maps names to functions | `{"web_search": web_search}` |
| **System Prompt** | Instructions for LLM | "Use web_search for current info" |
| **Agent Loop** | Iterative think-act cycle | Max 5 iterations |
| **tool_choice** | How LLM uses tools | `"auto"` = LLM decides |

### Tool-Calling Flow

```
1. User asks question
2. LLM decides if tools needed
3. If yes: LLM generates tool_call
4. Agent executes tool
5. Agent sends result back to LLM
6. LLM processes result
7. Repeat or return final answer
```

### Message Roles

```python
"system"     # Instructions for LLM
"user"       # User's question
"assistant"  # LLM's response (may include tool_calls)
"tool"       # Tool execution result
```

### Core Code Pattern

```python
# 1. Define tools
def my_tool(arg):
    return result

# 2. Create registry
AVAILABLE_TOOLS = {"my_tool": my_tool}

# 3. Define for LLM
tools = [{"function": {"name": "my_tool", ...}}]

# 4. Agent loop
while not done:
    response = llm.chat(..., tools=tools)
    if response.tool_calls:
        for tool_call in response.tool_calls:
            result = AVAILABLE_TOOLS[tool_call.name](...)
            messages.append({"role": "tool", "content": result})
    else:
        return response.content
```

---

## Mental Model & Key Takeaways

### 🧠 Mental Model: Personal Assistant with Phone Access

```
┌──────────────────────────────────────────────────────────┐
│                   YOU (User)                              │
│         "What's Bitcoin price * 2?"                       │
└──────────────────────────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────┐
│              ASSISTANT (LLM Brain)                        │
│                                                           │
│  Thinks: "I need:                                        │
│   1. Current Bitcoin price (changes) → Google it         │
│   2. Multiplication → Calculator                         │
│                                                           │
│  Has access to:                                          │
│   - Phone (web_search tool)                              │
│   - Calculator (calculate tool)                          │
└──────────────────────────────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
    ┌─────────┐     ┌─────────┐    ┌──────────┐
    │  Phone  │     │Calculator│    │  Brain   │
    │ (Google)│     │   App    │    │ (Memory) │
    └─────────┘     └─────────┘    └──────────┘
          │               │               │
          │ Result:       │ Result:       │ Already
          │ "$67,234"     │ "134468"      │ knows
          │               │               │
          └───────────────┴───────────────┘
                          │
                          ▼
                "Bitcoin is $67,234.
                 Double is $134,468."
```

### Production Best Practices

**1. Add More Tools:**

```python
def get_weather(location: str) -> str:
    """Get current weather"""
    return weather_api.get(location)

def send_email(to: str, subject: str, body: str) -> str:
    """Send an email"""
    return email_service.send(to, subject, body)

def database_query(sql: str) -> str:
    """Query database"""
    return db.execute(sql)

AVAILABLE_TOOLS = {
    "web_search": web_search,
    "calculate": calculate,
    "get_weather": get_weather,
    "send_email": send_email,
    "database_query": database_query
}

# Agent can now do much more!
```

**2. Add Conversation History:**

```python
conversation_history = []

def run_agent_with_history(question: str):
    # Include previous conversation
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *conversation_history,  # Previous messages
        {"role": "user", "content": question}
    ]
    
    # ... rest of agent loop ...
    
    # Save for next time
    conversation_history.append({"role": "user", "content": question})
    conversation_history.append({"role": "assistant", "content": answer})
    
    return answer
```

**3. Add Tool Result Validation:**

```python
def validate_tool_result(tool_name: str, result: str) -> bool:
    """Check if tool returned valid result"""
    if "failed" in result.lower():
        return False
    if tool_name == "web_search" and len(result) < 10:
        return False  # Too short, probably error
    return True

# In agent loop:
result = AVAILABLE_TOOLS[tool_name](**arguments)

if not validate_tool_result(tool_name, result):
    result = f"{tool_name} returned invalid result. Please try again."
```

**4. Add Retry Logic:**

```python
MAX_RETRIES = 3

for retry in range(MAX_RETRIES):
    try:
        result = AVAILABLE_TOOLS[tool_name](**arguments)
        break  # Success!
    except Exception as e:
        if retry == MAX_RETRIES - 1:
            result = f"Tool failed after {MAX_RETRIES} attempts: {e}"
        else:
            time.sleep(1)  # Wait before retry
```

### Key Takeaways

1. **Tool Calling = LLM decides when to use external tools**
2. **Three Components: Function + Definition + Registry**
3. **Agent Loop: Think → Act → Observe → Repeat**
4. **tool_choice="auto" lets LLM decide intelligently**
5. **Always handle tool errors gracefully**
6. **Max iterations prevents infinite loops**
7. **Tool definitions guide LLM's decisions**

### Evolution Path

```
Day 7: ReAct Chain (predefined steps)
  ↓
Day 18: Tool-Calling Agent (autonomous decisions)  ← We are here
  ↓
Next: Production agents with:
  - Multiple specialized tools
  - Conversation memory
  - Error handling & retries
  - Tool result validation
  - Streaming responses
  - Multi-agent collaboration
```

---

## 🎯 Summary

**What We Built:**

A fully autonomous AI agent that:
- Searches the web for current information (Tavily)
- Performs mathematical calculations (eval)
- Decides when to use which tool (LLM)
- Chains multiple tools together (iterative loop)
- Returns final answer to user

**Core Pattern:**

```python
# 1. Define tools (Python functions)
def web_search(query: str) -> str: ...
def calculate(expression: str) -> str: ...

# 2. Create registry
AVAILABLE_TOOLS = {"web_search": web_search, "calculate": calculate}

# 3. Define for LLM (JSON)
tools = [{"function": {"name": "web_search", ...}}, ...]

# 4. Agent loop
for iteration in range(max_iterations):
    response = llm.chat(..., tools=tools, tool_choice="auto")
    
    if response.tool_calls:
        for tool_call in response.tool_calls:
            result = AVAILABLE_TOOLS[tool_call.name](**args)
            messages.append({"role": "tool", "content": result})
    else:
        return response.content  # Final answer
```

**Why This is Powerful:**

```
Traditional LLM: Static knowledge cutoff
Tool-Calling Agent: Access to real-time data

Traditional: Can only think
Agent: Can think AND act

Traditional: Single response
Agent: Multi-step reasoning

This is the foundation of modern AI agents like ChatGPT plugins, AutoGPT, and more!
```

Day 18 teaches you to build production-ready AI agents that can interact with the real world! 🚀

---

**Total Lines:** ~1000+
**Hinglish Style:** Easy technical depth with real analogies
**Coverage:** Complete tool-calling system with web search + calculator
**Target:** Senior dev quality for beginners
