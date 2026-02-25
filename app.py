#############################################################################
# app.py
#
# This file contains the entrypoint for the app.
#
#############################################################################

import streamlit as st
from datetime import datetime
from modules import display_my_custom_component, display_post, display_genai_advice, display_activity_summary, display_recent_workouts
from data_fetcher import get_user_posts, get_genai_advice, get_user_profile, get_user_sensor_data, get_user_workouts

userId = 'user1'




def read_bytes(uploaded):
    return uploaded.read() if uploaded is not None else None

def display_app_page():
    """Displays the home page of the app."""
    if "posts" not in st.session_state:
        st.session_state["posts"] = []
    st.title('Welcome to SDS!')
    st.write("---")
    st.header("Your Fitness Dashboard")

    # Fetch workouts
    workouts = get_user_workouts(userId) or []

    # Activity Summary
    if "workouts" not in st.session_state:
        st.session_state.workouts = []

if st.button("Post"):
    workout_text = workout_description  

    miles_match = re.search(r"(\d+(\.\d+)?)\s*miles?", workout_text, re.IGNORECASE)
    steps_match = re.search(r"(\d+)\s*steps?", workout_text, re.IGNORECASE)
    calories_match = re.search(r"(\d+)\s*calories?", workout_text, re.IGNORECASE)

    miles = float(miles_match.group(1)) if miles_match else 0
    steps = int(steps_match.group(1)) if steps_match else 0
    calories = int(calories_match.group(1)) if calories_match else 0

    st.session_state.workouts.append({
        "miles": miles,
        "steps": steps,
        "calories": calories,
        "description": workout_text
    })


workouts = st.session_state.workouts

total_workouts = len(workouts)
total_distance = sum(w.get("miles", 0) for w in workouts)
total_steps = sum(w.get("steps", 0) for w in workouts)
total_calories = sum(w.get("calories", 0) for w in workouts)

st.subheader("Activity Summary")
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Workouts", total_workouts)
    st.metric("Total Steps", total_steps)
with col2:
    st.metric("Total Distance", f"{total_distance:.1f} miles")
    st.metric("Total Calories", total_calories)

st.subheader("Recent Sessions")
if workouts:
    for i, w in enumerate(reversed(workouts[-5:]), 1):  # show last 5 sessions
        st.write(f"{i}. {w['description']} — {w.get('miles', 0)} miles, {w.get('steps',0)} steps, {w.get('calories',0)} calories")
else:
    st.write("No recent workouts to show.")

    st.write("---")


 

    # Recent Workouts
    st.subheader("Recent Sessions")
    display_recent_workouts(workouts)
    st.write("---")

    # GenAI advice
    advice = get_genai_advice(userId)
    if advice:
        display_genai_advice(advice['timestamp'], advice['content'], advice['image'])
    st.write("---")

    # Display posts form
    with st.form("post_form"):
        username = st.text_input("Enter username")
        user_image = st.file_uploader("profile image", type=["jpg", "jpeg", "png"])
        content = st.text_area("workout description")
        post_image = st.file_uploader("workout image", type=["jpg", "jpeg", "png"])
        submitted = st.form_submit_button("Post")

    if submitted:
        if username == "":
            st.warning("please enter username")
        elif len(content) > 280 or len(content) < 1:
            st.warning("description must be between 1 and 280 characters")
        else:
            post = {
                "username": username,
                "user_image_bytes": read_bytes(user_image),
                "timestamp": datetime.now(),
                "content": content,
                "post_image_bytes": read_bytes(post_image),
            }
            st.session_state["posts"].append(post)

    for p in reversed(st.session_state["posts"]):
        display_post(
            p["username"],
            p["user_image_bytes"],
            p["timestamp"],
            p["content"],
            p["post_image_bytes"],
        )
        
# This is the starting point for your app. You do not need to change these lines
if __name__ == '__main__':
    display_app_page()