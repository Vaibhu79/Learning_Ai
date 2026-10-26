# Week 1, Day 4 - JSON Mode & Pydantic Models 🗂️

## 1. What Does This Code Do?

Ye program **structured outputs** ka concept sikha raha hai - LLM se clean, parseable data kaise extract kare.

Simple explanation:
1. User ka unstructured data hai (customer ticket mein mixed information)
2. Pydantic se ek **schema/blueprint** banate hain (kya data chahiye)
3. LLM ko schema de do aur **JSON format** mein response maango
4. Response automatically validate ho jata hai
5. Clean, typed data mil jata hai (directly access kar sakte ho)

**Real-world use:** Customer support tickets, forms, resumes, invoices - koi bhi unstructured text se structured data extract karna.

---

## 2. Big Picture Visualization

```
Unstructured Text
    │
    │ "Hello My name is Vaibhav. Yesterday I broke up 
    │  with my girlfriend sheetal I have an iPhone which 
    │  is not working at all..."
    │
    ▼
Define Schema (Pydantic)
    │
    │ class Ticket:
    │     name: str
    │     email: str
    │     issue: str
    │
    ▼
System Prompt
    │
    │ "Extract data according to this schema"
    │
    ▼
LLM Processing (with response_format="json_object")
    │
    ▼
Raw JSON Response
    │
    │ {"name": "Vaibhav", "email": "abc@gmail.com", 
    │  "issue": "iPhone not working"}
    │
    ▼
Pydantic Validation
    │
    ▼
Typed Python Object
    │
    │ ticket.name → "Vaibhav"
    │ ticket.email → "abc@gmail.com"
    │ ticket.issue → "iPhone not working"
```

---

## 3. Real-Life Analogy

Socho ek **form** hai (like Google Form).

- **Unstructured text** = Customer ka random email/message
- **Pydantic schema** = Form ke fields (Name box, Email box, Issue box)
- **System prompt** = Form ke instructions ("Fill all fields")
- **JSON mode** = Form automatically formats data
- **Validation** = Form checks email is valid, name is text, etc.
- **Final object** = Filled form ka clean data

Traditional approach: Manually read email aur extract karo (error-prone)

AI approach: LLM automatically form fill kar deta hai!

---

## 4. Prerequisites / Concepts Used

Day 1-3 ke concepts plus:

1. **Pydantic** - Data validation library
2. **Classes** - Python blueprints for objects
3. **Type hints** - `name: str`, `age: int`
4. **JSON** - JavaScript Object Notation (data format)
5. **Schema** - Data structure definition
6. **response_format parameter** - Force JSON output
7. **Dictionary unpacking** - `**dict` syntax
8. **String methods** - `json.loads()`

---

## 5. Imports — Explain Every Import

### Imports 1-4: Same as Day 1

(os, Path, load_dotenv, Groq)

---

### NEW IMPORT: Pydantic

### Import 5:

```python
from pydantic import BaseModel
```

**Kya hai?**  
`BaseModel` ek class hai Pydantic library se.

**Kyun chahiye?**  
Data validation aur schema definition ke liye.

**Kaise use hota hai?**  
Is class ko inherit karke apni custom classes banate hain.

**Example:**
```python
class Person(BaseModel):  # Inheriting from BaseModel
    name: str
    age: int
```

**Built-in ya third-party?**  
Third-party (`pydantic` package).

**Pydantic kya karta hai?**
1. Data validation (automatic type checking)
2. Data serialization (Python objects → JSON)
3. Data parsing (JSON → Python objects)
4. Schema generation (automatic JSON schema creation)

---

## 6. Code Setup / Configuration

Same as Day 1-3 (lines 1-16).

---

## 7. Data Structures

### NEW CONCEPT: Pydantic Model Class

### Lines 18-22:

```python
class ticket(BaseModel):
    name: str
    email: str
    issue: str
```

---

## DEEP DIVE: Pydantic Classes

### What is a Class?

**Class** = Blueprint / Template for creating objects.

**Real-world analogy:**
```
Class = House blueprint
Object = Actual house built from blueprint

Blueprint defines:
- 3 bedrooms
- 2 bathrooms  
- 1 kitchen

Every house built from this blueprint will have these features.
```

---

### Python Class Syntax:

```python
class ClassName:
    # Class body
```

**Word-by-word:**
- `class` → Keyword (we're defining a class)
- `ClassName` → Name of the class (PascalCase convention)
- `:` → Body start
- Indented code → Class body

---

### Basic Class Example:

```python
class Person:
    pass  # Empty class

# Create an object
person1 = Person()
```

---

### Pydantic Model Class:

```python
class ticket(BaseModel):
    name: str
    email: str
    issue: str
```

**Word-by-word breakdown:**

- `class` → Keyword
- `ticket` → Class name (should be `Ticket` by PascalCase convention, but works)
- `(BaseModel)` → **Inheritance** - this class inherits from `BaseModel`
- `:` → Body start
- `name: str` → **Type-annotated attribute**
- `email: str` → Type-annotated attribute
- `issue: str` → Type-annotated attribute

---

### What is Inheritance?

```
BaseModel (parent class)
    │
    │ (provides validation, JSON conversion, etc.)
    │
    ├───────> ticket (child class)
            │
            └─ Inherits all BaseModel features
               + Adds specific fields (name, email, issue)
```

**Simple explanation:**  
`ticket` class ko `BaseModel` ki saari powers mil jati hain automatically.

---

### Type Hints (`name: str`):

```python
name: str
```

**Breakdown:**
- `name` → Attribute name
- `:` → Type annotation symbol
- `str` → Expected data type

**Meaning:**  
"`name` attribute hoga jiska type string hona chahiye."

**Other type examples:**
```python
age: int           # Integer
price: float       # Decimal number
is_active: bool    # True/False
tags: list[str]    # List of strings
data: dict         # Dictionary
count: int | None  # Integer or None (optional)
```

---

### Why Pydantic?

**Without Pydantic:**
```python
# Manual validation (error-prone)
data = {"name": "Vaibhav", "email": "abc@gmail.com", "issue": "iPhone issue"}

if "name" not in data:
    raise ValueError("Name missing")
if not isinstance(data["name"], str):
    raise ValueError("Name must be string")
if "email" not in data:
    raise ValueError("Email missing")
# ... more validation code
```

**With Pydantic:**
```python
# Automatic validation
class Ticket(BaseModel):
    name: str
    email: str
    issue: str

ticket = Ticket(**data)  # Automatically validates!
# If invalid, raises clear error
```

---

### Line 24:

```python
schema = ticket.model_json_schema()
```

**Word-by-word breakdown:**

- `schema` → Variable to store JSON schema
- `=` → Assignment
- `ticket` → Our Pydantic class
- `.` → Dot operator
- `model_json_schema()` → Pydantic method that generates JSON schema

**Complete meaning:**  
Pydantic class se automatically JSON schema generate karo.

---

## DEEP DIVE: JSON Schema

### What is JSON Schema?

JSON schema ek **specification** hai jo define karta hai ki JSON data kaisa hona chahiye.

### ticket.model_json_schema() output:

```json
{
    "title": "ticket",
    "type": "object",
    "properties": {
        "name": {
            "title": "Name",
            "type": "string"
        },
        "email": {
            "title": "Email",
            "type": "string"
        },
        "issue": {
            "title": "Issue",
            "type": "string"
        }
    },
    "required": ["name", "email", "issue"]
}
```

**What this schema says:**
- Response should be an **object** (dictionary)
- It should have 3 **properties**: name, email, issue
- All properties should be **strings**
- All properties are **required** (not optional)

---

### Why send schema to LLM?

**LLM ko bata rahe hain:**  
"Iss format mein data return karo, not any other format."

Without schema:
```
LLM might return: "The customer's name is Vaibhav and email is abc@gmail.com..."
(Unstructured text - hard to parse)
```

With schema:
```json
LLM returns: {"name": "Vaibhav", "email": "abc@gmail.com", "issue": "..."}
(Clean JSON - easy to parse)
```

---

### NEW CONCEPT: response_format Parameter

### Lines 27-29:

```python
response_format = {
    "type": "json_object",   
}
```

**Word-by-word breakdown:**

- `response_format` → Dictionary variable
- `=` → Assignment
- `{` → Dictionary start
- `"type"` → Key
- `:` → Key-value separator
- `"json_object"` → Value (special keyword)
- `}` → Dictionary end

**Complete meaning:**  
LLM ko force karo ki response **valid JSON object** format mein do.

---

## DEEP DIVE: response_format

### What does response_format do?

**Without response_format:**
```python
response = client.chat.completions.create(...)
# LLM might return plain text, markdown, code, anything
```

**With response_format={"type": "json_object"}:**
```python
response = client.chat.completions.create(..., response_format={"type": "json_object"})
# LLM MUST return valid JSON
# If it tries to return text, API forces JSON format
```

---

### Types of response_format:

**Type 1: Default (No response_format)**
```python
# LLM returns natural text
"The name is Vaibhav."
```

**Type 2: JSON Object**
```python
response_format = {"type": "json_object"}
# LLM returns JSON
{"name": "Vaibhav"}
```

**Type 3: JSON Schema (advanced - not all APIs)**
```python
response_format = {
    "type": "json_schema",
    "json_schema": schema
}
# LLM strictly follows schema structure
```

---

### Critical Rule:

**When using response_format="json_object", you MUST mention "JSON" in your prompt!**

```python
# BAD (will fail):
prompt = "Extract name and email"
response_format = {"type": "json_object"}

# GOOD:
prompt = "Extract name and email. Return as JSON."
response_format = {"type": "json_object"}
```

---

### Lines 31-33: System Prompt

```python
system_prompt = f"""extract the personal information from the ticket strictly based on this schema and give a json output{schema}
"""
```

**Word-by-word breakdown:**

- `system_prompt` → Variable
- `=` → Assignment
- `f"""..."""` → **F-string with triple quotes** (multi-line string)
- `{schema}` → Embedding the schema dictionary

**Complete meaning:**  
System ko instruction de rahe hain: "Is schema ke according data extract karo aur JSON output do."

**Why f-string?**  
Taki `schema` variable ki value embed ho jaye string mein.

**Runtime value:**
```
extract the personal information from the ticket strictly based on this schema and give a json output{'title': 'ticket', 'type': 'object', ...}
```

---

### Lines 36-39: System Message

```python
system_message = {
    "role": "system",
    "content": system_prompt
}
```

Same as Day 2 - system role with instructions.

---

### Lines 42: Unstructured Text

```python
text = "Hello My name is Vaibhav. Yesterday I broke up with my girlfriend sheetal I have an iphone which is not working at all. My address is delhi. My email is abc@gmail.com. My contact number is 82134"
```

**This is messy customer text!**

Contains:
- ✓ Name: "Vaibhav"
- ✓ Email: "abc@gmail.com"
- ✓ Issue: "iPhone not working"
- ✗ Irrelevant info: girlfriend breakup, address, partial phone number

**Challenge:** Extract only relevant data.

---

### Lines 45:

```python
prompt = f""" this is a customer ticket please extract personal information from this {text}"""
```

**User prompt:** Pass the messy text to LLM.

---

### Lines 47-50: User Message

```python
message = {
    "role": role,
    "content": prompt
}
```

Standard user message.

---

### Lines 53:

```python
messages = [system_message, message]
```

**Order:** System first, then user (as always).

---

### Lines 54:

```python
response = client.chat.completions.create(model=model, messages=messages, response_format=response_format)
```

**NEW: response_format parameter added!**

**Complete API call:**
- `model` → llama-3.3-70b-versatile
- `messages` → [system, user]
- `response_format` → {"type": "json_object"}

**LLM knows:**
1. Extract data from text (system prompt)
2. Follow schema structure (system prompt)
3. Return JSON format (response_format)

---

### Lines 55:

```python
answer = response.choices[0].message.content
```

Extract raw response text.

**Value (example):**
```json
{
    "name": "Vaibhav",
    "email": "abc@gmail.com",
    "issue": "iPhone not working"
}
```

**Note:** This is a **string**, not a Python dictionary yet!

---

### Lines 56:

```python
print(answer)
```

Print raw JSON string.

---

### NEW CONCEPT: JSON Parsing

### Lines 60:

```python
import json
```

**Kya hai?**  
`json` Python ki built-in library hai.

**Kyun chahiye?**  
JSON string ko Python dictionary mein convert karne ke liye.

**Built-in ya third-party?**  
Built-in.

---

### Lines 61:

```python
raw_json = answer
```

Clarifying variable name (raw JSON string).

---

### Lines 62:

```python
data_file = json.loads(raw_json)
```

**Word-by-word breakdown:**

- `data_file` → Variable (will store dictionary)
- `=` → Assignment
- `json` → JSON library
- `.` → Dot operator
- `loads` → **Load String** method
- `()` → Function call
- `raw_json` → JSON string to parse

**Complete meaning:**  
JSON string ko Python dictionary mein convert karo.

---

## DEEP DIVE: json.loads()

### What is json.loads()?

**loads** = **L**oad **S**tring

Converts JSON string → Python object (usually dict).

### Example:

```python
import json

# JSON string (text)
json_string = '{"name": "Vaibhav", "age": 25}'

# Parse to Python dict
data = json.loads(json_string)

print(type(json_string))  # <class 'str'>
print(type(data))         # <class 'dict'>

print(data["name"])       # "Vaibhav"
```

---

### json.loads() vs json.load()

**json.loads()** - Load from **string**
```python
json_string = '{"name": "Vaibhav"}'
data = json.loads(json_string)
```

**json.load()** - Load from **file**
```python
with open("data.json") as f:
    data = json.load(f)
```

---

### In our code:

```
Before json.loads():
raw_json = '{"name": "Vaibhav", "email": "abc@gmail.com", "issue": "iPhone not working"}'
Type: str (string)

After json.loads():
data_file = {"name": "Vaibhav", "email": "abc@gmail.com", "issue": "iPhone not working"}
Type: dict (dictionary)
```

---

### NEW CONCEPT: Dictionary Unpacking

### Lines 63:

```python
Ticket = ticket(**data_file)
```

**Word-by-word breakdown:**

- `Ticket` → Variable (will store ticket object)
- `=` → Assignment
- `ticket` → Our Pydantic class
- `()` → Calling the class (creating object)
- `**data_file` → **Dictionary unpacking operator**

**Complete meaning:**  
Dictionary ke key-value pairs ko arguments ki tarah pass karke ticket object banao.

---

## DEEP DIVE: ** (Dictionary Unpacking)

### What is **?

`**` operator dictionary ko **unpack** karta hai.

### Example without **:

```python
class Person(BaseModel):
    name: str
    age: int

# Manual way
person = Person(name="Vaibhav", age=25)
```

---

### Example with **:

```python
data = {"name": "Vaibhav", "age": 25}

# Unpacking way
person = Person(**data)

# ** expands to:
# person = Person(name="Vaibhav", age=25)
```

---

### Visualization:

```
data_file = {
    "name": "Vaibhav",
    "email": "abc@gmail.com",
    "issue": "iPhone not working"
}

ticket(**data_file)
    ↓
    ** unpacks to:
    ↓
ticket(
    name="Vaibhav",
    email="abc@gmail.com",
    issue="iPhone not working"
)
    ↓
Pydantic validates:
    ✓ name is string
    ✓ email is string
    ✓ issue is string
    ↓
Creates ticket object
```

---

### Why use **?

**Without ** (manual):**
```python
Ticket = ticket(
    name=data_file["name"],
    email=data_file["email"],
    issue=data_file["issue"]
)
```

**With ** (automatic):**
```python
Ticket = ticket(**data_file)
```

Much cleaner! Especially when many fields.

---

### Lines 66-68: Accessing Object Attributes

```python
print(Ticket.name)
print(Ticket.email)
print(Ticket.issue)
```

**Word-by-word:**

- `Ticket` → Our ticket object
- `.` → Dot operator (access attribute)
- `name` / `email` / `issue` → Attributes

**Complete meaning:**  
Object ke attributes directly access karo.

**Output:**
```
Vaibhav
abc@gmail.com
iPhone not working
```

---

### Why this is powerful:

**Traditional dictionary access:**
```python
print(data_file["name"])   # String key - typos possible
print(data_file["email"])  # No autocomplete
print(data_file["issue"])
```

**Pydantic object access:**
```python
print(Ticket.name)   # Attribute - autocomplete works!
print(Ticket.email)  # IDE helps you
print(Ticket.issue)  # Type checking
```

**Plus:**
- Typo protection (`Ticket.naem` → IDE error)
- Type validation automatic
- Better code completion
- Professional code structure

---

## 8. COMPLETE EXECUTION TRACE

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 1-4: Setup
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Imports ✓
load_dotenv() ✓
API key loaded ✓
Client created ✓
Model = "llama-3.3-70b-versatile"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 5: Define Pydantic Model
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ticket(BaseModel):
    name: str
    email: str
    issue: str

Blueprint created ✓

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 6: Generate JSON Schema
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

schema = ticket.model_json_schema()

schema = {
    "title": "ticket",
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "email": {"type": "string"},
        "issue": {"type": "string"}
    },
    "required": ["name", "email", "issue"]
}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 7: Configure response_format
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

response_format = {"type": "json_object"}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 8: Create System Prompt
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

system_prompt = f"""extract the personal information 
from the ticket strictly based on this schema and give 
a json output{schema}"""

system_message = {"role": "system", "content": system_prompt}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 9: Prepare User Text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

text = "Hello My name is Vaibhav. Yesterday I broke up 
with my girlfriend sheetal I have an iphone which is not 
working at all. My address is delhi. My email is 
abc@gmail.com. My contact number is 82134"

prompt = f"this is a customer ticket please extract 
personal information from this {text}"

message = {"role": "user", "content": prompt}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 10: Send to LLM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

messages = [system_message, message]

response = client.chat.completions.create(
    model=model,
    messages=messages,
    response_format=response_format  # Force JSON
)

LLM processes:
    ↓
    Reads system: "Extract per schema, return JSON"
    Reads user: "Here's messy ticket text"
    Reads schema: {name, email, issue required}
    Analyzes text: Finds Vaibhav, abc@gmail.com, iPhone issue
    Ignores irrelevant: girlfriend, address, partial phone
    Formats as JSON
    ↓
    Returns response

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 11: Extract Answer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

answer = response.choices[0].message.content

answer = '{"name": "Vaibhav", "email": "abc@gmail.com", 
"issue": "iPhone not working"}'

Type: str (JSON string)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 12: Print Raw JSON
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

print(answer)

Output:
{"name": "Vaibhav", "email": "abc@gmail.com", 
"issue": "iPhone not working"}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 13: Parse JSON
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

import json
raw_json = answer
data_file = json.loads(raw_json)

data_file = {
    "name": "Vaibhav",
    "email": "abc@gmail.com",
    "issue": "iPhone not working"
}

Type: dict (Python dictionary)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 14: Create Pydantic Object
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ticket = ticket(**data_file)

Unpacking:
    **data_file expands to:
    ↓
    ticket(
        name="Vaibhav",
        email="abc@gmail.com",
        issue="iPhone not working"
    )
    ↓
Pydantic validation:
    ✓ name is str
    ✓ email is str
    ✓ issue is str
    ↓
    Object created successfully

Ticket = <ticket object>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 15: Access Attributes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

print(Ticket.name)
Output: Vaibhav

print(Ticket.email)
Output: abc@gmail.com

print(Ticket.issue)
Output: iPhone not working

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PROGRAM ENDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 9. EXPECTED OUTPUT

```
{"name": "Vaibhav", "email": "abc@gmail.com", "issue": "iPhone not working"}
Vaibhav
abc@gmail.com
iPhone not working
```

---

## 10. Common Beginner Confusions

### Q1: Class vs Object mein kya difference hai?

**Answer:**

**Class** = Blueprint / Template
```python
class ticket(BaseModel):
    name: str
    email: str
    issue: str
# This is a blueprint (no actual data yet)
```

**Object** = Instance created from class
```python
Ticket = ticket(name="Vaibhav", email="abc@gmail.com", issue="iPhone issue")
# This is an actual ticket object (with real data)
```

**Analogy:**
```
Class = Cookie cutter (blueprint)
Object = Actual cookie made from that cutter
```

You can make many objects from one class:
```python
ticket1 = ticket(name="Vaibhav", ...)
ticket2 = ticket(name="Rahul", ...)
ticket3 = ticket(name="Priya", ...)
```

---

### Q2: Type hints mandatory hain kya?

**Answer:**

**Regular Python:** Optional
```python
class Person:
    name = ""  # No type hint needed
```

**Pydantic:** **Mandatory!**
```python
class Person(BaseModel):
    name: str  # Type hint required
    # Without type hint → Error
```

---

### Q3: Pydantic validation kaise kaam karta hai?

**Answer:**

**Automatic validation on object creation:**

```python
class ticket(BaseModel):
    name: str
    email: str
    issue: str

# Valid data
t1 = ticket(name="Vaibhav", email="abc@gmail.com", issue="Phone broken")  # ✓ Works

# Invalid data - wrong type
t2 = ticket(name=123, email="abc@gmail.com", issue="Phone broken")
# ✗ Error: name should be str, not int

# Invalid data - missing field
t3 = ticket(name="Vaibhav", email="abc@gmail.com")
# ✗ Error: issue field required
```

---

### Q4: JSON string vs Python dict kaise differentiate kare?

**Answer:**

```python
# JSON string (text with quotes around entire thing)
json_string = '{"name": "Vaibhav"}'
print(type(json_string))  # <class 'str'>
print(json_string[0])     # '{' (first character)

# Python dictionary (actual data structure)
python_dict = {"name": "Vaibhav"}
print(type(python_dict))  # <class 'dict'>
print(python_dict["name"]) # "Vaibhav" (access key)
```

**Visual difference:**
```python
JSON string:   '{"key": "value"}'  ← Quotes around entire thing
Python dict:   {"key": "value"}     ← No surrounding quotes
```

---

### Q5: ** (double star) kab use kare?

**Answer:**

Use `**` when you want to convert dictionary to function arguments:

```python
# You have a dictionary
data = {"name": "Vaibhav", "age": 25}

# You want to call a function
def create_person(name, age):
    # ...

# Without **
create_person(data["name"], data["age"])  # Manual

# With **
create_person(**data)  # Automatic unpacking
```

---

### Q6: response_format kab use kare?

**Answer:**

**Use response_format when:**
- ✓ You need structured data (JSON)
- ✓ You're parsing LLM output programmatically
- ✓ You have a schema to follow
- ✓ You need consistent format

**Don't use when:**
- ✗ You need human-readable text
- ✗ You're writing essays/articles
- ✗ Format doesn't matter

---

### Q7: Pydantic ke bina JSON parsing ho sakti hai?

**Answer:**

**Haan! But manually:**

```python
# Without Pydantic
data = json.loads(raw_json)
name = data["name"]    # Manual access
email = data["email"]  # No validation
issue = data["issue"]

# If key missing → KeyError
# If type wrong → No error (dangerous!)
```

**With Pydantic:**
```python
ticket = ticket(**data)
name = ticket.name   # Autocomplete
email = ticket.email # Validated
issue = ticket.issue

# Missing key → Clear error message
# Wrong type → Clear error message
```

---

### Q8: Schema LLM ko bhejte hain ya Python ko?

**Answer:**

**Both!**

**To LLM** (in system prompt):
```python
system_prompt = f"Return JSON matching {schema}"
# LLM uses schema to format response
```

**To Python** (for validation):
```python
ticket = ticket(**data)
# Pydantic uses schema to validate data
```

Schema is the **contract** between LLM and Python code.

---

## 11. Common Mistakes / Bugs

### Mistake 1: Forgetting to mention "JSON" in prompt

**Wrong:**
```python
system_prompt = "Extract name and email"
response_format = {"type": "json_object"}
# API error: Prompt must contain word "JSON"
```

**Correct:**
```python
system_prompt = "Extract name and email as JSON"
response_format = {"type": "json_object"}
```

---

### Mistake 2: Class naming (minor style issue)

**Current:**
```python
class ticket(BaseModel):  # lowercase
```

**Better (PEP 8 convention):**
```python
class Ticket(BaseModel):  # PascalCase
```

Not an error, but professional code uses PascalCase for classes.

---

### Mistake 3: Variable name collision

**Confusing:**
```python
class ticket(BaseModel):  # Class named 'ticket'
    ...

Ticket = ticket(...)  # Variable named 'Ticket'
```

**Clearer:**
```python
class Ticket(BaseModel):  # Class: Ticket
    ...

ticket_obj = Ticket(...)  # Variable: ticket_obj
# or
my_ticket = Ticket(...)
```

---

### Mistake 4: Forgetting json.loads()

**Wrong:**
```python
raw_json = '{"name": "Vaibhav"}'
ticket = ticket(**raw_json)  # Error! Can't unpack string
```

**Correct:**
```python
raw_json = '{"name": "Vaibhav"}'
data = json.loads(raw_json)  # Convert to dict first
ticket = ticket(**data)      # Now works
```

---

### Mistake 5: Wrong unpacking operator

**Wrong:**
```python
data = {"name": "Vaibhav"}
ticket = ticket(*data)  # Single * unpacks to keys only
# Equivalent to: ticket("name", "email", "issue")
# Error!
```

**Correct:**
```python
ticket = ticket(**data)  # Double ** unpacks to key=value pairs
# Equivalent to: ticket(name="Vaibhav", ...)
```

---

### Mistake 6: Not handling JSON parsing errors

**Current code has no error handling:**

```python
data_file = json.loads(raw_json)
# What if raw_json is not valid JSON?
```

**Better:**
```python
try:
    data_file = json.loads(raw_json)
except json.JSONDecodeError as e:
    print(f"Invalid JSON: {e}")
```

---

### Mistake 7: Not handling Pydantic validation errors

**Current code:**
```python
Ticket = ticket(**data_file)
# What if data doesn't match schema?
```

**Better:**
```python
from pydantic import ValidationError

try:
    Ticket = ticket(**data_file)
except ValidationError as e:
    print(f"Validation failed: {e}")
```

---

## 12. Professional Code Review

### ✅ Good Things:

1. **Structured output** - Using Pydantic for data validation
2. **JSON mode** - response_format ensures clean output
3. **Schema-driven** - Clear contract between LLM and code
4. **Type hints** - Code is self-documenting
5. **Separation** - Schema generation, API call, parsing are distinct steps

---

### 🔧 Improvements:

#### 1. **Add error handling**

```python
from pydantic import ValidationError

try:
    # JSON parsing
    data_file = json.loads(raw_json)
    
    # Pydantic validation
    ticket_obj = Ticket(**data_file)
    
    print(ticket_obj.name)
    print(ticket_obj.email)
    print(ticket_obj.issue)
    
except json.JSONDecodeError as e:
    print(f"JSON parsing failed: {e}")
except ValidationError as e:
    print(f"Data validation failed: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

#### 2. **Improve class naming**

```python
class Ticket(BaseModel):  # PascalCase
    name: str
    email: str
    issue: str

ticket_obj = Ticket(**data_file)
```

---

#### 3. **Add field descriptions**

```python
from pydantic import BaseModel, Field

class Ticket(BaseModel):
    name: str = Field(description="Customer's full name")
    email: str = Field(description="Customer's email address")
    issue: str = Field(description="Description of the technical issue")
```

---

#### 4. **Add email validation**

```python
from pydantic import BaseModel, EmailStr

class Ticket(BaseModel):
    name: str
    email: EmailStr  # Validates email format!
    issue: str
```

---

#### 5. **Make system prompt clearer**

**Current:**
```python
system_prompt = f"""extract the personal information from the ticket strictly based on this schema and give a json output{schema}"""
```

**Better:**
```python
system_prompt = f"""
You are a customer support data extraction assistant.

Extract the following information from the customer ticket:
- Customer name
- Email address
- Technical issue description

Ignore irrelevant information like personal life details, addresses, or partial contact numbers.

Return ONLY valid JSON matching this exact schema:
{schema}

Do NOT include any extra text or explanation.
"""
```

---

#### 6. **Organize better**

```python
# 1. Define data models
class Ticket(BaseModel):
    name: str
    email: EmailStr
    issue: str

# 2. Helper function
def extract_ticket_info(text: str) -> Ticket:
    schema = Ticket.model_json_schema()
    system_prompt = f"Extract info as JSON: {schema}"
    # ... API call
    data = json.loads(response.choices[0].message.content)
    return Ticket(**data)

# 3. Main execution
if __name__ == "__main__":
    text = "..."
    ticket = extract_ticket_info(text)
    print(f"Name: {ticket.name}")
    print(f"Email: {ticket.email}")
    print(f"Issue: {ticket.issue}")
```

---

## 13. What This Code Teaches You

New concepts from Day 4:

1. ✅ **Pydantic models** - Data validation and schemas
2. ✅ **Classes** - Object-oriented programming basics
3. ✅ **Type hints** - `name: str`, `email: str`
4. ✅ **JSON schema** - Data structure specification
5. ✅ **response_format** - Forcing JSON outputs
6. ✅ **json.loads()** - JSON string parsing
7. ✅ **Dictionary unpacking** - `**dict` syntax
8. ✅ **Dot notation** - `object.attribute` access
9. ✅ **Structured data extraction** - Messy text → Clean data

---

## 14. What To Learn Next

Day 4 ke baad:

### Immediate (Day 5):
1. **Complex schemas** - Nested models, lists
2. **File handling** - PDF/DOCX parsing
3. **Multiple object processing** - Loops with Pydantic
4. **Real-world application** - Resume parser

### Future:
5. **Advanced Pydantic** - Validators, computed fields
6. **Enum types** - Limited value options
7. **Optional fields** - `name: str | None`
8. **List fields** - `skills: list[str]`

---

## 15. Real-World Applications

Where is this pattern used?

### 1. Customer Support
```python
class SupportTicket(BaseModel):
    customer_name: str
    issue_category: str
    priority: str
    description: str
```

### 2. Resume Parsing
```python
class Resume(BaseModel):
    name: str
    email: str
    skills: list[str]
    experience_years: int
```

### 3. Invoice Processing
```python
class Invoice(BaseModel):
    invoice_number: str
    date: str
    total_amount: float
    items: list[dict]
```

### 4. Form Filling
```python
class RegistrationForm(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    address: str
```

---

## 16. Final Mental Model

```
Unstructured Text
    │
    ├─ Define Schema (Pydantic class)
    │   └─ What data do I need?
    │
    ├─ Generate JSON Schema
    │   └─ Tell LLM the format
    │
    ├─ System Prompt
    │   └─ "Extract per schema"
    │
    ├─ User Prompt
    │   └─ "Here's the messy text"
    │
    ├─ response_format="json_object"
    │   └─ Force JSON output
    │
    ├─ LLM Processing
    │   └─ Returns JSON string
    │
    ├─ json.loads()
    │   └─ JSON string → Python dict
    │
    └─ Pydantic(**dict)
        └─ Dict → Validated object
            └─ Access: object.attribute
```

### In one sentence:

**"Ye program Pydantic se schema define karta hai, LLM se JSON format mein data extract karta hai, aur validated Python objects create karta hai jisse type-safe access milta hai."**

---

## 17. Quick Reference

### Pydantic Basics:
```python
from pydantic import BaseModel

class MyModel(BaseModel):
    field1: str
    field2: int
    field3: list[str]

# Create object
obj = MyModel(field1="text", field2=123, field3=["a", "b"])

# Access
print(obj.field1)
```

### JSON Parsing:
```python
import json

json_string = '{"key": "value"}'
python_dict = json.loads(json_string)
```

### Dictionary Unpacking:
```python
data = {"name": "Vaibhav", "age": 25}
obj = MyClass(**data)
# Equivalent to: MyClass(name="Vaibhav", age=25)
```

---

**Amazing progress! 🎉**  
Tumne JSON mode aur Pydantic successfully master kar liya!

Next: Day 5 mein tumhe **complete resume parser project** milega - all concepts combined! 🚀
