import streamlit as st
from openai_client import client
from nutrition_analysis import analyze_image
from chat import send_chat_message

# --- App Setup ---
st.set_page_config(page_title="MyFitnessPal Assistant", layout="centered")
st.title("MyFitnessPal - Assistant")
st.caption("Upload a food label or chat about your fitness goals")

# --- State Initialization ---
if "thread" not in st.session_state:
    st.session_state.thread = client.beta.threads.create()

# --- File Upload Section ---
with st.expander("📤 Upload Food Label Image"):
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png", "webp"])
    if uploaded_file and st.button("Analyze Image"):
        response = analyze_image(st.session_state.thread, uploaded_file)
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        st.markdown(f"### 🧠 Nutrition Analysis\n{response}")

# --- Chat Section ---
st.markdown("---")
st.subheader("💬 Chat with the Assistant")
user_input = st.chat_input("Type your message...")
if user_input:
    st.chat_message("user").markdown(user_input)
    response = send_chat_message(st.session_state.thread, user_input)
    st.chat_message("assistant").markdown(response)