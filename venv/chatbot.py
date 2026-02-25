import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

client = InferenceClient(
    api_key=os.getenv("HF_API_KEY"),
)

def get_completion(prompt, model="mistralai/Mistral-7B-Instruct-v0.2"):
    messages = [{"role": "user", "content": prompt}]
    
    response = client.chat_completion(
        model=model,
        messages=messages,
        temperature=0,
    )
    
    return response.choices[0].message.content


def get_completion_from_messages(messages, model="mistralai/Mistral-7B-Instruct-v0.2", temperature=0):
    
    response = client.chat_completion(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    print(str(response.choices[0].message))
    return response.choices[0].message.content


messages = [
    {'role': 'system', 'content': 'You are an assistant talk like that'},
    {'role': 'user', 'content': 'tell me a joke'},
    {'role': 'assistant', 'content': 'Why did the chicken cross the road?'},
    {'role': 'user', 'content': "I don't know"}
]

response = get_completion_from_messages(messages, temperature=1)
print(response)