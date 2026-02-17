import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

client = InferenceClient(
    api_key=os.getenv("HF_API_KEY"),
)

response = client.chat_completion(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    messages=[
        {"role": "user", "content": "Explain Large Language Models in one simple sentence."}
    ],
    max_tokens=100,
)

print(response.choices[0].message.content)