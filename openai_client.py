from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

try:
    assistant = client.beta.assistants.create(
        name="MyFitnessPal Assistant",
        instructions="You are a helpful assistant that analyzes nutrition labels and offers dietary insights.",
        tools=[{"type": "retrieval"}],
        model="gpt-4-1106-preview"
    )
    assistant_id = assistant.id
except Exception as e:
    # Fallback to manually supplied ID
    assistant_id = os.getenv("ASSISTANT_ID")
    print("Assistant creation failed. Using fallback ID.")

if not assistant_id:
    raise ValueError("No assistant could be created or loaded. Check your API key or ASSISTANT_ID.")
