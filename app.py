#############################################################################
# app.py
#############################################################################

import streamlit as st

from modules import (
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


st.set_page_config(page_title="SDS Fitness App", layout="wide")


def apply_app_styles():
    """Applies shared spacing and typography styles across the app."""
    st.markdown(
        """
        <style>
        .block-container {
            max-width: 1100px;
            padding-top: 2rem;
            padding-bottom: 2.5rem;
        }
        h1 {
            font-size: 2.2rem !important;
            line-height: 1.2 !important;
            margin-bottom: 0.35rem !important;
        }
        h2 {
            font-size: 1.55rem !important;
            line-height: 1.25 !important;
            margin-top: 0.5rem !important;
            margin-bottom: 0.5rem !important;
        }
        h3 {
            font-size: 1.15rem !important;
            line-height: 1.35 !important;
        }
        p, li, label, [data-testid="stMarkdownContainer"] {
            font-size: 0.98rem !important;
            line-height: 1.55 !important;
        }
        [data-testid="stCaptionContainer"] {
            font-size: 0.86rem !important;
        }
        [data-testid="stVerticalBlock"] > [data-testid="stForm"] {
            border: 1px solid #e5e7eb;
            border-radius: 14px;
            padding: 1rem 1rem 0.25rem 1rem;
            background: #fafafa;
        }
        [data-testid="stButton"] > button,
        [data-testid="stFormSubmitButton"] > button {
            border-radius: 10px;
            font-size: 0.95rem;
            padding-top: 0.45rem;
            padding-bottom: 0.45rem;
        }
        [data-testid="stTextInput"] label,
        [data-testid="stTextArea"] label,
        [data-testid="stSelectbox"] label,
        [data-testid="stDateInput"] label,
        [data-testid="stTimeInput"] label,
        [data-testid="stNumberInput"] label,
        [data-testid="stFileUploader"] label,
        [data-testid="stMultiSelect"] label {
            font-weight: 600 !important;
            font-size: 0.95rem !important;
        }
        section[data-testid="stSidebar"] .block-container {
            padding-top: 1.25rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def display_app_page(user_id):
    """Displays the home page of the app for the selected user."""
    try:
        profile = get_user_profile(user_id)
        username = profile.get("username", user_id)
    except Exception:
        username = user_id

    st.title("Welcome to SDS!")
    st.header("Your Fitness Dashboard")

    workouts = get_user_workouts(user_id) or []
    recent_workout_count = len(workouts)

    stat_col1, stat_col2, stat_col3 = st.columns(3)
    stat_col1.metric("User Code", user_id)
    stat_col2.metric("Username", username)
    stat_col3.metric("Workouts Logged", recent_workout_count)

    st.write("---")

    display_activity_summary(workouts)
    st.write("---")

    st.subheader("Recent Sessions")
    display_recent_workouts(workouts)
    st.write("---")

    advice = get_genai_advice(user_id)
    if advice:
        display_genai_advice(advice["timestamp"], advice["content"], advice["image"])
    st.write("---")


if __name__ == "__main__":
    apply_app_styles()

    default_user_id = st.session_state.get("current_user_id", "user1")

    with st.sidebar:
        st.header("User Login")
        entered_user_id = st.text_input(
            "Enter your user code",
            value=default_user_id,
            help="Try one of these sample codes: " + ", ".join(get_available_user_ids()),
        ).strip()
        st.session_state["current_user_id"] = entered_user_id

    if not entered_user_id:
        st.sidebar.info("Create a profile to get started.")
        display_profile_page()
        st.stop()

    page = st.sidebar.selectbox(
        "Navigate",
        ["Home", "Community", "Activity", "Goal Setter", "Meal Plan", "Create Profile"],
    )

    if page == "Create Profile":
        display_profile_page()
        st.stop()

    if not user_exists(entered_user_id):
        st.error(
            "That user code was not found. Try one of these sample codes: "
            + ", ".join(get_available_user_ids())
        )
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
