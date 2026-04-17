#############################################################################
# activity_page.py
#
# This file contains the activity page for the app.
# It displays a user's recent 3 workouts, activity summary,
# and a share button to post a stat to the community.
#############################################################################

from datetime import datetime

import streamlit as st

from data_fetcher import get_user_workouts
from modules import display_activity_summary, display_recent_workouts, display_post


def read_bytes(uploaded):
    return uploaded.read() if uploaded is not None else None


def display_activity_page(user_id):
    """Displays the activity page for the given user.

    Shows the 3 most recent workouts, an activity summary, and a share button
    that lets the user post a stat to the community.

    Parameters:
        user_id (str): the ID of the current user
    """

    st.title("Your Activity")
    st.write("Track your recent workouts and share your progress!")
    st.write("---")

    activity_posts_key = f"activity_posts_{user_id}"
    if activity_posts_key not in st.session_state:
        st.session_state[activity_posts_key] = []

    with st.form("activity_post_form"):
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
            activity_entry = {
                "username": username,
                "user_image": read_bytes(user_image),
                "timestamp": datetime.now(),
                "content": content,
                "post_image": read_bytes(post_image),
            }
            st.session_state[activity_posts_key].append(activity_entry)
            st.success("Your workout has been added to your Activity page.")

    activity_posts = st.session_state.get(activity_posts_key, [])
    if activity_posts:
        st.subheader("Your Logged Workouts")
        for post in reversed(activity_posts):
            display_post(
                post["username"],
                post["user_image"],
                post["timestamp"],
                post["content"],
                post["post_image"],
            )
            st.write("---")

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
    st.subheader("Recent Sessions")
    display_recent_workouts(recent_workouts)
    st.write("---")

