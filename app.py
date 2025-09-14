import gradio as gr
import openai
import os

# Configure OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = """
You are an AI Airline Service Assistant.
Provide helpful information about airline services including:
- Flight bookings and reservations
- Check-in procedures
- Baggage policies
- Flight status updates
- Loyalty programs and benefits
- Special assistance services
- Flight change and cancellation policies
"""

def airline_assistant(user_query):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=messages,
        max_tokens=500,
        temperature=0.7,
    )
    return response.choices[0].message['content']

iface = gr.Interface(
    fn=airline_assistant,
    inputs=gr.Textbox(lines=3, placeholder="Ask about: flight booking, baggage policy, check-in, flight status..."),
    outputs="text",
    title="AI Airline Service Assistant",
    description="Get assistance with airline services, bookings, and travel information"
)

iface.launch()
