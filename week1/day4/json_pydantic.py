import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

# is load_dotenv se hanmare env me jitni bhi chizen hoti hai isme aa jata hai
load_dotenv()

# ISKA matlab hum hamari jo api key hai wo is variable me store kar rhe hain
my_api_key = os.getenv("GROQ_API_KEY")

# agar api key nhi hui to ye function execute hoga
if not my_api_key:
    raise ValueError("API key kha hai bhaiii")

# jo hamara client hai like abhi hum groq use kar rhe hai to usko kaise pata chalega hum konsi api key use kar rhe hai uske liye hum ye niche wala function use krenge
client=Groq(api_key=my_api_key)


# model define krenge withour any spelling mistakes
model="llama-3.3-70b-versatile"

# role define krenge hum hamara 
role="user"

# pydantic ke hisab se structure karna
from pydantic import BaseModel

# fir hum ek class banate hai or humko jo bhi chizen chahiye wo hum isme likh dete hain
class ticket(BaseModel):
    name:str
    email:str
    issue:str

schema=ticket.model_json_schema()

# isme hum batate hai ki response konse format me chahiye humko ex -  json me
response_format={
    "type":"json_object",   
}
# system prompt de rhe hai ab hum
system_prompt=f"""extract the personal information from the ticket strictly based on this schema and give a json output{schema}
"""

# system ka role content and message

system_message={
    "role":"system",
    "content":system_prompt
}

# text
text="Hello My name is Vaibhav. Yesterday I broke up with my girlfriend sheetal I have an iphone which is not working at all. My address is delhi. My email is abc@gmail.com. My contact number is 82134"

# prompt likhenge fir as a user

prompt=f""" this is a customer ticket please extract personal information from this {text}"""

message={
    "role": role,
    "content": prompt
}


messages=[system_message, message]
response=client.chat.completions.create(model=model,messages=messages,response_format=response_format)
answer=response.choices[0].message.content
print(answer)

# isko direct padhna ho to kaise kre -

import json
raw_json=answer
data_file=json.loads(raw_json)
Ticket=ticket(**data_file)

# so to make it more easy for the user hum direct is ko paas kar sakte hain
print(Ticket.name)
print(Ticket.email)
print(Ticket.issue)
