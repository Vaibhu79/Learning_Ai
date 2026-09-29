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

prompt="Hii"
prompt2="Explain the big bang theory under 100 words"
prompt3="write 1000 words essay on Ai"

# ab humko apne jo prompts hai unko one by one bhejna hai as prompt to uske liye we will use loop 
prompts=[prompt,prompt2,prompt3]

for prompt in prompts:
    message={
    "role": role,
    "content": prompt
}
    messages=[message]
    response=client.chat.completions.create(model=model,messages=messages,max_tokens=50)
    usage=response.usage
    print(f"Prompt: {prompt} --> your tokens:{usage.prompt_tokens} completion tokens:{usage.completion_tokens} total tokens:{usage.total_tokens} finish reason:{response.choices[0].finish_reason}") 



# #for i in prompts:
#     message={
#     "role": role,
#     "content": prompt
# }
#     messages=[message]
#     response=client.chat.completions.create(model=model,messages=messages,max_tokens=50)
#     usage=response.usage
#     print(f"Prompt: {i} --> your tokens:{usage.prompt_tokens} completion tokens:{usage.completion_tokens} total tokens:{usage.total_tokens} finish reason:{response.choices[0].finish_reason}") 

