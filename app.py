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
    workouts = st.session_state.get('posts', [])
    
    total_miles = 0.0
    total_steps = 0
    total_calories = 0

    for w in workouts:
        content = w.get('description') or w.get('text') or ""
        text = str(content).lower()
        
        import re
        nums = re.findall(r"(\d+\.?\d*)", text)
        
        if nums:
            val = float(nums[0])
            
        
            if "mile" in text:
                total_miles += val
            if "step" in text:
                total_steps += int(val)
            if "calor" in text:
                total_calories += int(val)

    st.markdown("## Activity Summary")
    c1, c2 = st.columns(2)
    c3, c4 = st.columns(2)
    
    c1.metric("Total Workouts", len(workouts))
    c2.metric("Total Distance", f"{total_miles} miles")
    c3.metric("Total Steps", f"{total_steps}")
    c4.metric("Total Calories", f"{total_calories}")

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