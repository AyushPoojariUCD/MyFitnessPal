import streamlit as st
from openai_client import client
from nutrition_analysis import analyze_image
from chat import send_chat_message

# --- App Setup ---
st.set_page_config(page_title="MyFitnessPal Assistant", layout="centered")
st.title("MyFitnessPal - Assistant")
st.caption("Upload a food label or chat about your fitness goals")

# --- State Initialization ---
if "user_info_submitted" not in st.session_state:
    st.session_state.user_info_submitted = False
if "thread" not in st.session_state:
    st.session_state.thread = client.beta.threads.create()
if "intro_sent" not in st.session_state:
    st.session_state.intro_sent = False

# --- Step 1: User Info Form ---
if not st.session_state.user_info_submitted:
    with st.form("user_info_form"):
        st.subheader("👤 Tell us about yourself")
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=10, max_value=100)
        height_ft = st.number_input("Height (feet)", min_value=1, max_value=8)
        height_in = st.number_input("Height (inches)", min_value=0, max_value=11)
        weight = st.number_input("Current Weight (lbs)", min_value=50.0, max_value=500.0)
        goal_weight = st.number_input("Goal Weight (lbs)", min_value=50.0, max_value=500.0)
        activity_level = st.radio("Activity Level", [
            "Not Very Active", "Lightly Active", "Active", "Very Active"
        ])
        goals = st.multiselect(
            "Fitness Goals (select up to 3)",
            ["Lose weight", "Maintain weight", "Gain weight", "Gain muscle", "Modify my diet", "Manage stress", "Increase step count"]
        )
        submit = st.form_submit_button("Submit")

        if submit:
            st.session_state.user_info_submitted = True
            st.session_state.user_data = {
                "name": name,
                "age": age,
                "height": f"{height_ft} ft {height_in} in",
                "current_weight": f"{weight} lbs",
                "goal_weight": f"{goal_weight} lbs",
                "activity_level": activity_level,
                "goals": goals
            }
            st.success("User info submitted! Scroll down to start chatting.")
            st.experimental_rerun()

# --- Step 2: Summary + Intro Message + Main App ---
if st.session_state.user_info_submitted:
    user = st.session_state.user_data
    with st.expander("📋 User Information Summary", expanded=True):
        st.markdown(f"**Name:** {user['name']}")
        st.markdown(f"**Age:** {user['age']}")
        st.markdown(f"**Height:** {user['height']}")
        st.markdown(f"**Weight:** {user['current_weight']} → {user['goal_weight']}")
        st.markdown(f"**Activity Level:** {user['activity_level']}")
        st.markdown(f"**Goals:** {', '.join(user['goals'])}")

    # --- Send intro message once ---
    if not st.session_state.intro_sent:
        intro_message = (
            f"My name is {user['name']}. I'm {user['age']} years old, "
            f"{user['height']} tall, weighing {user['current_weight']}, aiming for {user['goal_weight']}. "
            f"My activity level is '{user['activity_level']}' and my fitness goals are: {', '.join(user['goals'])}."
        )
        assistant_response = send_chat_message(st.session_state.thread, intro_message)
        st.session_state.intro_sent = True
        st.session_state.intro_response = assistant_response

    if st.session_state.get("intro_response"):
        st.info("👋 Assistant initialized with your profile!")
        st.markdown(st.session_state.intro_response)

    # --- File Upload Section ---
    with st.expander("📤 Upload Food Label Image"):
        uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png", "webp"])
        if uploaded_file and st.button("Analyze Image"):
            response = analyze_image(st.session_state.thread, uploaded_file)
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            st.markdown(f"### 🧠 Nutrition Analysis\n{response}")

    # --- Chat Section ---
    st.markdown("---")
    st.subheader("💬 Chat with the MyFitnessPal")
    user_input = st.chat_input("Type your message...")
    if user_input:
        st.chat_message("user").markdown(user_input)
        response = send_chat_message(st.session_state.thread, user_input)
        st.chat_message("assistant").markdown(response)
