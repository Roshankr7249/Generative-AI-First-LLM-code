import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import panel as pn

pn.extension()

load_dotenv()

# Validate API key
api_key = os.getenv("HF_API_KEY")
if not api_key:
    raise ValueError("HF_API_KEY not found in environment variables")

client = InferenceClient(api_key=api_key)

# ----------- LLM FUNCTION -----------

def get_completion_from_messages(messages, model="mistralai/Mistral-7B-Instruct-v0.2", temperature=0):
    response = client.chat_completion(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content


# ----------- SYSTEM CONTEXT -----------

context = [{
    'role': 'system',
    'content': """
You are OrderBot, an automated service to collect orders for a pizza restaurant.
You first greet the customer, then collect the order,
and then ask if it's a pickup or delivery.
You wait to collect the entire order, then summarize it and check one final time
if the customer wants to add anything else.
If it's a delivery, you ask for an address.
Finally you collect the payment.
You respond in a short, friendly conversational style.
"""
}]

# ----------- UI COMPONENTS -----------

inp = pn.widgets.TextInput(placeholder='Enter text here…')
button_conversation = pn.widgets.Button(name="Chat!")
chat_area = pn.Column(height=400, scroll=True)


# ----------- AUTO START GREETING -----------

def initialize_chat():
    greeting = get_completion_from_messages(context)
    context.append({'role': 'assistant', 'content': greeting})

    chat_area.append(
        pn.Row(
            "Assistant:",
            pn.pane.Markdown(
                greeting,
                width=600,
                styles={
                    'background-color': '#F6F6F6',
                    'padding': '10px',
                    'border-radius': '8px'
                }
            )
        )
    )


# ----------- CHAT LOGIC -----------

def collect_messages(event):
    prompt = inp.value.strip()
    inp.value = ''

    if not prompt:
        return

    context.append({'role': 'user', 'content': prompt})
    response = get_completion_from_messages(context)
    context.append({'role': 'assistant', 'content': response})

    chat_area.append(
        pn.Row("User:", pn.pane.Markdown(prompt, width=600))
    )

    chat_area.append(
        pn.Row(
            "Assistant:",
            pn.pane.Markdown(
                response,
                width=600,
                styles={
                    'background-color': '#F6F6F6',
                    'padding': '10px',
                    'border-radius': '8px'
                }
            )
        )
    )


button_conversation.on_click(collect_messages)

# ----------- DASHBOARD -----------

dashboard = pn.Column(
    inp,
    button_conversation,
    chat_area
)

# 👇 THIS LINE TRIGGERS AUTO GREETING
initialize_chat()

dashboard.servable()


messages =  context.copy()
messages.append(
{'role':'system', 'content':'create a json summary of the previous food order. Itemize the price for each item\
 The fields should be 1) pizza, include size 2) list of toppings 3) list of drinks, include size   4) list of sides include size  5)total price '},    
)
 #The fields should be 1) pizza, price 2) list of toppings 3) list of drinks, include size include price  4) list of sides include size include price, 5)total price '},    

response = get_completion_from_messages(messages, temperature=0)
print(response)