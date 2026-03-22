#############################################################################
# activity_page.py
#
# This file contains the activity page for the app.
# It displays a user's recent 3 workouts, activity summary,
# and a share button to post a stat to the community.
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
    """Inserts a new post into the Posts table in BigQuery.

    Parameters:
        user_id (str): the ID of the user making the post
        content (str): the text content of the post

    Returns:
        bool: True if successful, False otherwise
    """
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
    """Displays the activity page for the given user.

    Shows the 3 most recent workouts, an activity summary, and a share button
    that lets the user post a stat to the community.

    Parameters:
        user_id (str): the ID of the current user
    """

    st.title("🏃 Your Activity")
    st.write("Track your recent workouts and share your progress!")
    st.write("---")

    # Step 1: Fetch all workouts for this user
    all_workouts = get_user_workouts(user_id) or []

    if not all_workouts:
        st.info("You have no recorded workouts yet. Get moving!")
        return

    # Step 2: Sort by start_timestamp descending and take the 3 most recent
    def parse_timestamp(workout):
        ts = workout.get('start_timestamp', '')
        try:
            return datetime.strptime(str(ts), '%Y-%m-%d %H:%M:%S')
        except Exception:
            return datetime.min

    sorted_workouts = sorted(all_workouts, key=parse_timestamp, reverse=True)
    recent_workouts = sorted_workouts[:3]

    # Step 3: Activity Summary (uses all recent 3 workouts)
    display_activity_summary(recent_workouts)
    st.write("---")

    # Step 4: Recent Workouts display
    st.subheader("🗓️ Recent Sessions")
    display_recent_workouts(recent_workouts)
    st.write("---")

    # Step 5: Share button section
    st.subheader("📣 Share With the Community")
    st.write("Proud of your progress? Share a stat with your friends!")

    # Pick best stat to share from the most recent workout
    latest = recent_workouts[0]
    steps = latest.get('steps') or 0
    calories = latest.get('calories_burned') or latest.get('calories') or 0
    distance = latest.get('distance') or 0

    # Let user choose which stat to share
    stat_choice = st.selectbox(
        "Choose a stat to share:",
        options=["Steps", "Calories Burned", "Distance"],
        key="stat_choice"
    )

    # Build the share message based on choice
    if stat_choice == "Steps":
        share_message = f"Look at this, I walked {steps:,} steps today! 👟🔥 #FitnessGoals"
    elif stat_choice == "Calories Burned":
        share_message = f"Just burned {calories} calories in my latest workout! 🔥💪 #Fitness"
    else:
        share_message = f"I covered {distance} miles in my latest workout! 🏃‍♀️ #Running"

    st.write(f"**Preview:** {share_message}")

    # Track share success in session state
    if "share_success" not in st.session_state:
        st.session_state["share_success"] = False

    if st.button("📤 Share to Community"):
        success = insert_post(user_id, share_message)
        if success:
            st.session_state["share_success"] = True

    if st.session_state.get("share_success"):
        st.success("✅ Your post has been shared with the community!")
