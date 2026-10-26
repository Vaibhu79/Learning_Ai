import os 
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("Api Key Not FOund")

client=Groq(api_key=my_api_key)

model="llama-3.3-70b-versatile"


prompt="explain what is internet deeply"

message={
    "role":"user",
    "content":prompt
}

messages=[message]

response=client.chat.completions.create(model=model,messages=messages)
# print(response)
ans=response.choices[0].message.content
print(ans)


stream  = client.chat.completions.create(model=model, messages=messages, stream=True)

for chunks in stream:
    content = chunks.choices[0].delta.content #delta ka matlab jo text abhi abhi add hua hai
    if content:
        print(content, end="", flush = True)