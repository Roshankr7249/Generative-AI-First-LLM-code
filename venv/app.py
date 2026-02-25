#import os
#from dotenv import load_dotenv
#from huggingface_hub import InferenceClient

#load_dotenv()

#client = InferenceClient(
#    api_key=os.getenv("HF_API_KEY"),
#)

#response = client.chat_completion(
    #model="mistralai/Mistral-7B-Instruct-v0.2",
   # messages=[
   #     {"role": "user", "content": "what is AEP (Adobe experience Platform)"}
  #  ],
 #   max_tokens=1000,
#)

#print(response.choices[0].message.content)



import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

client = InferenceClient(
    api_key=os.getenv("HF_API_KEY"),
)

fact_sheet_chair = """
OVERVIEW
- Part of a beautiful family of mid-century inspired office furniture...
(CUT FOR BREVITY)
"""

prompt = f"""
Your task is to help a marketing team create a 
description for a retail website of a product based 
on a technical fact sheet.

Write a product description based on the information 
provided in the technical specifications delimited by 
triple backticks.

Use at most 50 words.

Technical specifications: ```{fact_sheet_chair}```
"""

response = client.chat_completion(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    messages=[
        {"role": "user", "content": prompt}
    ],
    max_tokens=1000,
)

print(response.choices[0].message.content)