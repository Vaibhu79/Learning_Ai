import os
from dotenv import load_dotenv
from pathlib import Path
from groq import Groq
import numpy as np
from sentence_transformers import SentenceTransformer


# ye ek sentance ko embading me convert karne ke kaam aata hai or iske liye hum alag alag models use karte hai
model = SentenceTransformer("all-MiniLM-L6-v2") #384

text= " machine learing is fun"

# similarity kaise pata kare kisi 2 chizon ke bich - using cosine similarity or usme 2 imputs le kar jinko compare krenge

def cosice_sim(a,b):
    return np.dot(a,b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )

#  ab hum isko yha use krenge

t1="their are 20 paid leaves"
t2 = "there are 20 paid days "

# ab hum uppar jo bhi variables hai unki embading karenge agar 0.5 ya close to 1 aata hai means kinda same or similar 1 matlab ekdum same and -minus me aaye matlab bilkul similar nhi

v1 = model.encode(t1)
v2 = model.encode(t2)

print(cosice_sim(v1,v2))

# embading=model.encode(text)
# print(embading.shape)
# print(embading[:10])