import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

# .env file se environment variables load kar raha hai
load_dotenv()

# .env se GROQ_API_KEY read kar raha hai
my_api_key = os.getenv("GROQ_API_KEY")

# Agar API key nahi mili to error show karega
if not my_api_key:
    raise ValueError("api key kha hai bhai")

# Groq client create kar raha hai
client = Groq(api_key=my_api_key)

# Groq model
model = "openai/gpt-oss-120b"

# knowledge base banana for our llm taki wo answer kar paye

knowledge_base={
    "age": "harry ki age 55 hai",
    "class": "harry 12th me padhta hai"
}

def retrive_info(question):
    question=question.lower()

    if "age" in question:
        return knowledge_base["age"]
    elif "class" in question:
        return knowledge_base["class"]
    else:
        return "no information about this bs"



# user ka input
def ask_llm(question):

    context=retrive_info(question)
    # System ka instruction 
    sys_prompt = f"""Give answer in one line, and answer only based on this context do not hallucinate {context}"""

    # System message
    system_message = {
        "role": "system",
        "content": sys_prompt
    }

    # User message
    user_message = {
        "role": "user",
        "content": question
    }

    # IMPORTANT:
    # messages ke andar message dictionaries jayengi
    messages = [system_message,user_message]

    # Groq API ko request bhejna
    response = client.chat.completions.create( model=model, messages=messages)

    # LLM ka actual answer nikalna
    answer = response.choices[0].message.content

    return answer


question = "Do you know code with harry's age"

print(ask_llm(question))