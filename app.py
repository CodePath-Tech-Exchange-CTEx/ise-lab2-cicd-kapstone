#############################################################################
# app.py  (updated to include Meal Plan page)
#############################################################################

import streamlit as st
from datetime import datetime
from modules import display_my_custom_component, display_post, display_genai_advice, display_activity_summary, display_recent_workouts
from data_fetcher import add_user_post, get_user_posts, get_genai_advice, get_user_profile, get_user_sensor_data, get_user_workouts
from community_page import display_community_page
from activity_page import display_activity_page
from meal_plan_page import display_meal_plan_page   # ← new import

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

    workouts = get_user_workouts(userId) or []

    display_activity_summary(workouts)
    st.write("---")

    st.subheader("Recent Sessions")
    display_recent_workouts(workouts)
    st.write("---")

    advice = get_genai_advice(userId)
    if advice:
        display_genai_advice(advice['timestamp'], advice['content'], advice['image'])
    st.write("---")

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
            post_image_bytes = read_bytes(post_image)
            post = {
                "username": username,
                "user_image_bytes": read_bytes(user_image),
                "timestamp": datetime.now(),
                "content": content,
                "post_image_bytes": post_image_bytes,
            }
            st.session_state["posts"].append(post)
            add_user_post(userId, content, image=post_image_bytes, timestamp=post["timestamp"])

    for p in reversed(st.session_state["posts"]):
        display_post(
            p["username"],
            p["user_image_bytes"],
            p["timestamp"],
            p["content"],
            p["post_image_bytes"],
        )


if __name__ == '__main__':
    page = st.sidebar.selectbox(
        "Navigate",
        ["Home", "Community", "Activity", "Meal Plan"],  # ← added Meal Plan
    )

    if page == "Home":
        display_app_page()
    elif page == "Community":
        display_community_page(userId)
    elif page == "Activity":
        display_activity_page(userId)
    elif page == "Meal Plan":
        display_meal_plan_page()