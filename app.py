#############################################################################
# app.py
#
# This file contains the entrypoint for the app.
#
#############################################################################

import streamlit as st
from datetime import datetime
from modules import (inject_global_styles, display_my_custom_component,
                     display_post, display_genai_advice,
                     display_activity_summary, display_recent_workouts)
from data_fetcher import (get_user_posts, get_genai_advice, get_user_profile,
                          get_user_sensor_data, get_user_workouts)
from community_page import display_community_page
from activity_page import display_activity_page
from goal_setter_page import display_goal_setter_page

userId = 'user1'


def read_bytes(uploaded):
    return uploaded.read() if uploaded is not None else None


def display_app_page():
    """Displays the home page of the app."""
    if "posts" not in st.session_state:
        st.session_state["posts"] = []

    # Page header
    st.markdown("""
    <div class="page-title">SDS FITNESS</div>
    <div class="page-subtitle">Your personal fitness dashboard</div>
    <hr class="custom-divider">
    """, unsafe_allow_html=True)

    # Fetch workouts
    workouts = get_user_workouts(userId) or []

    # Activity Summary
    st.markdown('<div class="section-title">Activity Summary</div>', unsafe_allow_html=True)
    display_activity_summary(workouts)

    # Recent Workouts
    st.markdown('<div class="section-title">Recent Sessions</div>', unsafe_allow_html=True)
    display_recent_workouts(workouts)

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    # GenAI advice
    advice = get_genai_advice(userId)
    if advice:
        st.markdown('<div class="section-title">AI Coach</div>', unsafe_allow_html=True)
        display_genai_advice(advice['timestamp'], advice['content'], advice['image'])
        st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    # Post form
    st.markdown('<div class="section-title">Share a Workout</div>', unsafe_allow_html=True)
    with st.form("post_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            username = st.text_input("Username", placeholder="your username")
            user_image = st.file_uploader("Profile photo", type=["jpg", "jpeg", "png"])
        with col2:
            content = st.text_area("Workout description", placeholder="How did it go?", height=104)
            post_image = st.file_uploader("Workout photo", type=["jpg", "jpeg", "png"])

        submitted = st.form_submit_button("Post to Feed", use_container_width=True)

        if submitted:
            if username == "":
                st.warning("Please enter a username.")
            elif len(content) > 280 or len(content) < 1:
                st.warning("Description must be between 1 and 280 characters.")
            else:
                post = {
                    "username": username,
                    "user_image_bytes": read_bytes(user_image),
                    "timestamp": datetime.now(),
                    "content": content,
                    "post_image_bytes": read_bytes(post_image),
                }
                st.session_state["posts"].append(post)
                st.success("Posted!")

    if st.session_state["posts"]:
        st.markdown('<div class="section-title">Your Posts</div>', unsafe_allow_html=True)
        for p in reversed(st.session_state["posts"]):
            display_post(
                p["username"],
                p["user_image_bytes"],
                p["timestamp"],
                p["content"],
                p["post_image_bytes"],
            )


# This is the starting point for your app.
if __name__ == '__main__':
    st.set_page_config(
        page_title="SDS Fitness",
        page_icon="🏃",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    inject_global_styles()

    # Sidebar navigation
    with st.sidebar:
        st.markdown("""
        <div style="padding: 20px 0 28px 0;">
            <div style="font-family:'Barlow Condensed',sans-serif;font-size:26px;font-weight:800;color:#C6FF00;letter-spacing:1px;">SDS</div>
            <div style="font-size:11px;color:#4a5568;text-transform:uppercase;letter-spacing:2px;font-weight:600;">Fitness Tracker</div>
        </div>
        """, unsafe_allow_html=True)

        page = st.selectbox(
            "Navigate",
            ["Home", "Community", "Activity", "Goals"],
            label_visibility="visible"
        )

        st.markdown("""
        <div style="position:absolute;bottom:24px;left:20px;right:20px;">
            <div style="font-size:11px;color:#2a3040;text-transform:uppercase;letter-spacing:1.5px;font-weight:600;">Logged in as</div>
            <div style="font-size:13px;color:#4a5568;margin-top:2px;">remi_the_rems</div>
        </div>
        """, unsafe_allow_html=True)

    if page == "Home":
        display_app_page()
    elif page == "Community":
        display_community_page(userId)
    elif page == "Activity":
        display_activity_page(userId)
    elif page == "Goals":
        display_goal_setter_page()