import os
from dotenv import load_dotenv
from groq import Groq
from langchain_text_splitters import (CharacterTextSplitter,RecursiveCharacterTextSplitter)


text = """One evening, Rahul was walking home when he saw a small puppy sitting alone near a park. The puppy looked scared and seemed to be lost.
Rahul gave the puppy some water and gently checked its collar for an address. He called the owner, who arrived after a few minutes and thanked Rahul for helping.
Rahul went home with a big smile, feeling happy that he had helped the little puppy find its family.
"""

# ab hum yha se dekhnege kitne types ki chunking hoti hai


#1 fixed size chunking

fixed = CharacterTextSplitter(
    separator="",
    chunk_size=100,
    chunk_overlap=0
)

print("// FIXED SIZE CHUNKING //")

for i,chunk in enumerate(fixed.split_text(text),1):
    print(f"\nChunk {i}:")
    print(chunk)
    print("fixed chunking over")



#  2 paragraph chunking
paragraph = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=100,
    chunk_overlap=0
)
print("")
print("// PARAGRAPH CHUNKING //")

for i,chunk in enumerate(paragraph.split_text(text),1):
    print(f"\nChunk {i}:")
    print(chunk)
    print("Paragraph chunking over")


#  recursive chunking 

recursive = RecursiveCharacterTextSplitter(
    chunk_size = 100,
    chunk_overlap=20  #yha pe 20 ka matlab 20 letters hai 20 words nhi
)

print("// RECURSIVE CHUNKING //")

for i,chunk in enumerate(recursive.split_text(text),1):
    print(f"\nChunk {i}:")
    print(chunk)
    print("recursive chunking over")


