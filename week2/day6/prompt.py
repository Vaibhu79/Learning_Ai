import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key kha hai bhaiii")

client=Groq(api_key=my_api_key)

model="llama-3.3-70b-versatile"


def llm_func(prompt):
    message={
        "role":"user",
        "content":prompt
    }
    messages=[message]

    response=client.chat.completions.create(model=model,messages=messages)
    ans=response.choices[0].message.content
    return ans

# palihe hum ek bad prompt likh ke denge hamare llm ko 

bad_prompt="""
Role: You are a support assistant in an mobile or laptop company so work accordingly
task: you have to classify the issue in a category
constraint: you have c=to calssify the issue in 3 category which are billing , technical, return
output_format: your answer should be in 1 word only and should be in the 1 category given in constraints
#Example: For instance if a user compalin says he wants a refund then the category is Return
fallback: if issue is not related to any category in the constraints then the answer should be OTHER
this is a user complaint : MY girlfrind broke up with me"""

print(llm_func(bad_prompt))