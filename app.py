#############################################################################
# app.py
#############################################################################

import streamlit as st
from modules import (
    inject_global_styles,
    display_activity_summary,
    display_genai_advice,
    display_recent_workouts,
)
from data_fetcher import (
    get_available_user_ids,
    get_genai_advice,
    get_user_profile,
    get_user_workouts,
    user_exists,
)
from community_page import display_community_page
from activity_page import display_activity_page
from goal_setter_page import display_goal_setter_page
from meal_plan_page import display_meal_plan_page
from profile_page import display_profile_page


st.set_page_config(page_title="SDS Fitness", page_icon="🏃", layout="wide")


def display_app_page(user_id):
    """Displays the home page of the app for the selected user."""
    try:
        profile = get_user_profile(user_id)
        username = profile.get("username", user_id)
    except Exception:
        username = user_id

    st.markdown(f"""
    <div class="page-title">SDS FITNESS</div>
    <div class="page-subtitle">Welcome back, <span style="color:#C6FF00;">{username}</span></div>
    <hr class="custom-divider">
    """, unsafe_allow_html=True)

    workouts = get_user_workouts(user_id) or []

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div style="background:#161b24;border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:16px 20px;">
            <div style="font-size:11px;text-transform:uppercase;letter-spacing:1.5px;color:#4a5568;font-weight:600;">User Code</div>
            <div style="font-family:'Barlow Condensed',sans-serif;font-size:24px;font-weight:700;color:#C6FF00;margin-top:4px;">{user_id}</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="background:#161b24;border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:16px 20px;">
            <div style="font-size:11px;text-transform:uppercase;letter-spacing:1.5px;color:#4a5568;font-weight:600;">Username</div>
            <div style="font-family:'Barlow Condensed',sans-serif;font-size:24px;font-weight:700;color:#f0f4ff;margin-top:4px;">{username}</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div style="background:#161b24;border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:16px 20px;">
            <div style="font-size:11px;text-transform:uppercase;letter-spacing:1.5px;color:#4a5568;font-weight:600;">Workouts Logged</div>
            <div style="font-family:'Barlow Condensed',sans-serif;font-size:24px;font-weight:700;color:#f0f4ff;margin-top:4px;">{len(workouts)}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)

    st.markdown('<div class="section-title">Activity Summary</div>', unsafe_allow_html=True)
    display_activity_summary(workouts)

    st.markdown('<div class="section-title">Recent Sessions</div>', unsafe_allow_html=True)
    display_recent_workouts(workouts)

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    advice = get_genai_advice(user_id)
    if advice:
        st.markdown('<div class="section-title">AI Coach</div>', unsafe_allow_html=True)
        display_genai_advice(advice["timestamp"], advice["content"], advice["image"])


if __name__ == "__main__":
    inject_global_styles()

    default_user_id = st.session_state.get("current_user_id", "user1")

    with st.sidebar:
        st.markdown("""
        <div style="padding: 20px 0 28px 0;">
            <div style="font-family:'Barlow Condensed',sans-serif;font-size:26px;font-weight:800;color:#C6FF00;letter-spacing:1px;">SDS</div>
            <div style="font-size:11px;color:#4a5568;text-transform:uppercase;letter-spacing:2px;font-weight:600;">Fitness Tracker</div>
        </div>
        """, unsafe_allow_html=True)

        entered_user_id = st.text_input(
            "User code",
            value=default_user_id,
            help="Try: " + ", ".join(get_available_user_ids()),
        ).strip()
        st.session_state["current_user_id"] = entered_user_id

        page = st.selectbox(
            "Navigate",
            ["Home", "Community", "Activity", "Goal Setter", "Meal Plan", "Create Profile"],
        )

    if page == "Create Profile":
        display_profile_page()
        st.stop()

    if not entered_user_id:
        st.info("Enter a user code to get started.")
        st.stop()

    if not user_exists(entered_user_id):
        st.error("User code not found. Try: " + ", ".join(get_available_user_ids()))
        st.stop()

    if page == "Home":
        display_app_page(entered_user_id)
    elif page == "Community":
        display_community_page(entered_user_id)
    elif page == "Activity":
        display_activity_page(entered_user_id)
    elif page == "Goal Setter":
        display_goal_setter_page()
    elif page == "Meal Plan":
        display_meal_plan_page()