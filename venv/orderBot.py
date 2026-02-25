import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import panel as pn

pn.extension()

load_dotenv()

# ----------- API SETUP -----------

api_key = os.getenv("HF_API_KEY")
if not api_key:
    raise ValueError("HF_API_KEY not found in environment variables")

client = InferenceClient(api_key=api_key)

# ----------- SAFE LLM FUNCTION -----------
#mistralai/Mistral-7B-Instruct-v0.2    ->>>>> previously used model
def get_completion_from_messages(messages, model="meta-llama/Meta-Llama-3-8B-Instruct", temperature=0):
    try:
        response = client.chat_completion(
            model=model,
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ LLM Error: {str(e)}"


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

chat_area = pn.Column(height=400, scroll=True)
inp = pn.widgets.TextInput(placeholder='Enter text here…')
button_conversation = pn.widgets.Button(name="Chat!")

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

    # Add user message
    context.append({'role': 'user', 'content': prompt})

    # Get assistant response
    response = get_completion_from_messages(context)

    # Add assistant message
    context.append({'role': 'assistant', 'content': response})

    # Update UI
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
    chat_area,
    inp,
    button_conversation,
)

# Start conversation automatically
initialize_chat()

dashboard.servable()