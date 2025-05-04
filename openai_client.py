import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

try:
    assistant = client.beta.assistants.create(
        name="MyFitnessPal Assistant",
        instructions="You are a helpful assistant that analyzes nutrition labels and offers dietary insights.",
        tools=[{"type": "retrieval"}],
        model="gpt-4-1106-preview"
    )
    assistant_id = assistant.id
except Exception as e:
    assistant_id = st.secrets.get("ASSISTANT_ID")
    st.warning("Assistant creation failed. Using fallback ID.")

if not assistant_id:
    raise ValueError("No assistant could be created or loaded. Check your API key or ASSISTANT_ID.")
