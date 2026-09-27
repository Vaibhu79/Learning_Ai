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

# prompt likhenge fir as a user

prompt="Do you know code with harry?"

# message me hum hamara role or content/prompt jo bhi hai wo bhejte hai hum is message wale variable me or ye variable role or content he mangta hai
message={
    "role": role,
    "content": prompt
}

#humko ye message ek list ke form me bhejna hota hai so we can send multiple messages isliye hum message ko list bna ke bhejte hain 
messages=[message]

# response nikalne ke liye ki is prompt ko dala to response kya aya uske liye hum niche wala step follow karenge

response=client.chat.completions.create(model=model,messages=messages)

# fir hum is response ko print karwaenge
print(response)


# iska matlab hai ki humko sub khuch nhi chahiye jo main answer hai wo aata hai respone ke choices wale [0]th idx pe jo message hai or uske andar jo content hai humko wo chahiye
print(response.choices[0].message.content)