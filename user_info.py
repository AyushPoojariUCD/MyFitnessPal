import streamlit as st

def user_onboarding():
    steps = ["name", "goals", "activity", "details", "confirm"]

    if "step" not in st.session_state:
        st.session_state.step = 0
    if "user_data" not in st.session_state:
        st.session_state.user_data = {}

    step = st.session_state.step
    user_data = st.session_state.user_data

    # Step 1: Name
    if step == 0:
        st.subheader("MyFitnessPal")
        st.markdown("**What's your first name?**  \nLet's get to know a little about you.")
        user_data["name"] = st.text_input("First Name:", value=user_data.get("name", ""))
        if st.button("NEXT"):
            if user_data["name"]:
                st.session_state.step += 1

    # Step 2: Goals
    elif step == 1:
        st.subheader(f"Thanks {user_data['name']}!")
        st.markdown("**Now for your goals.**  \nSelect up to 3 that are important to you, including one weight goal.")
        options = [
            "Lose weight", "Maintain weight", "Gain weight",
            "Gain muscle", "Modify my diet", "Manage stress", "Increase step count"
        ]
        selected = st.multiselect("Goals", options, default=user_data.get("goals", []))
        if st.button("BACK"):
            st.session_state.step -= 1
        if st.button("NEXT"):
            if 1 <= len(selected) <= 3:
                user_data["goals"] = selected
                st.session_state.step += 1

    # Step 3: Activity
    elif step == 2:
        st.subheader("What is your baseline activity level?")
        st.caption("Not including workouts—we count that separately")
        activity = st.radio(
            "Activity Level",
            options=[
                "Not Very Active",
                "Lightly Active",
                "Active",
                "Very Active"
            ],
            index=["Not Very Active", "Lightly Active", "Active", "Very Active"].index(user_data.get("activity", "Lightly Active"))
        )
        if st.button("BACK"):
            st.session_state.step -= 1
        if st.button("NEXT"):
            user_data["activity"] = activity
            st.session_state.step += 1

    # Step 4: Personal Details
    elif step == 3:
        st.subheader("Tell us more about yourself")
        user_data["age"] = st.number_input("Age (years):", min_value=5, max_value=100, value=user_data.get("age", 25))
        user_data["height_ft"] = st.number_input("Height (feet):", min_value=1, max_value=8, value=user_data.get("height_ft", 5))
        user_data["height_in"] = st.number_input("Height (inches):", min_value=0, max_value=11, value=user_data.get("height_in", 7))
        user_data["weight"] = st.number_input("Current weight (lbs):", min_value=50.0, max_value=500.0, value=user_data.get("weight", 150.0))
        user_data["goal_weight"] = st.number_input("Goal weight (lbs):", min_value=50.0, max_value=500.0, value=user_data.get("goal_weight", 150.0))

        if st.button("BACK"):
            st.session_state.step -= 1
        if st.button("NEXT"):
            st.session_state.step += 1

    # Step 5: Confirmation
    elif step == 4:
        st.subheader("Review Your Information")
        st.markdown("Please verify your details before submitting")
        st.markdown(f"**Name:** {user_data['name']}")
        st.markdown(f"**Goals:** {', '.join(user_data['goals'])}")
        st.markdown(f"**Activity Level:** {user_data['activity']}")
        st.markdown(f"**Age:** {user_data['age']} years")
        st.markdown(f"**Height:** {user_data['height_ft']} ft {user_data['height_in']} in")
        st.markdown(f"**Current Weight:** {user_data['weight']} lbs")
        st.markdown(f"**Goal Weight:** {user_data['goal_weight']} lbs")

        if st.button("BACK"):
            st.session_state.step -= 1
        if st.button("SUBMIT"):
            return True

    return False
