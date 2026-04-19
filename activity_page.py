#############################################################################
# activity_page.py
#
# Revamped activity page with polished UI.
#
#############################################################################

import streamlit as st
import uuid
from datetime import datetime
from google.cloud import bigquery
from data_fetcher import get_user_workouts, get_client
from modules import display_activity_summary, display_recent_workouts

import os
project_id = os.environ.get("PROJECT_ID", "johnny-aryeetey-csudh")


def insert_post(user_id, content):
    """Inserts a new post into the Posts table in BigQuery."""
    post_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    query = f"""
    INSERT INTO `{project_id}.ISE.Posts` (PostId, AuthorId, Timestamp, ImageUrl, Content)
    VALUES (@post_id, @user_id, @timestamp, NULL, @content)
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("post_id", "STRING", post_id),
            bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
            bigquery.ScalarQueryParameter("timestamp", "STRING", timestamp),
            bigquery.ScalarQueryParameter("content", "STRING", content),
        ]
    )
    try:
        get_client().query(query, job_config=job_config).result()
        return True
    except Exception as e:
        st.error(f"Failed to share post: {e}")
        return False


def display_activity_page(user_id):
    """Displays the activity page for the given user."""

    st.markdown("""
    <div class="page-title">YOUR ACTIVITY</div>
    <div class="page-subtitle">Track your recent workouts and share your progress</div>
    <hr class="custom-divider">
    """, unsafe_allow_html=True)

    all_workouts = get_user_workouts(user_id) or []

    if not all_workouts:
        st.info("No recorded workouts yet. Get moving! 🏃")
        return

    # Sort by start_timestamp descending and take most recent 3
    def parse_timestamp(workout):
        ts = workout.get('start_timestamp', '')
        try:
            return datetime.strptime(str(ts), '%Y-%m-%d %H:%M:%S')
        except Exception:
            return datetime.min

    sorted_workouts = sorted(all_workouts, key=parse_timestamp, reverse=True)
    recent_workouts = sorted_workouts[:3]

    # Activity Summary
    st.markdown('<div class="section-title">Activity Summary</div>', unsafe_allow_html=True)
    display_activity_summary(recent_workouts)

    # Recent Workouts
    st.markdown('<div class="section-title">Recent Sessions</div>', unsafe_allow_html=True)
    display_recent_workouts(recent_workouts)

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    # Share section
    st.markdown("""
    <div class="section-title">Share With Community</div>
    <div style="font-size:13px;color:#8a93a8;margin-bottom:20px;">Proud of your progress? Share a stat with your friends!</div>
    """, unsafe_allow_html=True)

    latest = recent_workouts[0]
    steps = latest.get('steps') or 0
    calories = latest.get('calories_burned') or latest.get('calories') or 0
    distance = latest.get('distance') or 0

    stat_choice = st.selectbox(
        "Choose a stat to share:",
        options=["Steps", "Calories Burned", "Distance"],
        key="stat_choice"
    )

    if stat_choice == "Steps":
        share_message = f"Look at this, I walked {steps:,} steps today! 👟🔥 #FitnessGoals"
    elif stat_choice == "Calories Burned":
        share_message = f"Just burned {calories:,} calories in my latest workout! 🔥💪 #Fitness"
    else:
        dist_display = f"{distance:.1f}" if distance else "0"
        share_message = f"I covered {dist_display} miles in my latest workout! 🏃‍♀️ #Running"

    st.markdown(f"""
    <div style="background:var(--bg-card);border:1px solid var(--border-subtle);border-radius:12px;padding:16px 18px;margin:12px 0 18px 0;">
        <div style="font-size:11px;text-transform:uppercase;letter-spacing:1.5px;color:#4a5568;margin-bottom:6px;font-weight:600;">Preview</div>
        <div style="font-size:14px;color:var(--text-primary);">{share_message}</div>
    </div>
    """, unsafe_allow_html=True)

    if "share_success" not in st.session_state:
        st.session_state["share_success"] = False

    if st.button("📤 Share to Community", use_container_width=True):
        success = insert_post(user_id, share_message)
        if success:
            st.session_state["share_success"] = True

    if st.session_state.get("share_success"):
        st.success("✅ Your post has been shared with the community!")