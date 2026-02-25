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
    display_activity_summary(workouts)
    workouts = st.session_state.get("posts", [])

    total_workouts = len(workouts)
    total_dist = 0
    total_steps = 0
    total_cals = 0

for w in workouts:
    content = w.get("content", "")

    for word in content.split():
        if word.isdigit():
            num = int(word)
            if "mile" in content.lower() or "mi" in content.lower():
                total_dist += num
            if "step" in content.lower():
                total_steps += num
            if "cal" in content.lower():
                total_cals += num


    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Workouts", total_workouts)
    col2.metric("Total Distance", f"{total_dist} miles")
    col3.metric("Total Steps", total_steps)
    col4.metric("Total Calories", total_cals)

 

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