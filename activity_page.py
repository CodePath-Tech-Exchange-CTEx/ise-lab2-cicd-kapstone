#############################################################################
# activity_page.py
#
# This file contains the activity page for the app.
# It displays a user's recent 3 workouts, activity summary,
# and a share button to post a stat to the community.
#############################################################################

from datetime import date, datetime

import streamlit as st

from data_fetcher import add_user_workout, get_user_profile, get_user_workouts
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

    try:
        profile = get_user_profile(user_id)
        username = profile.get("username", user_id)
        user_image = profile.get("profile_image")
    except Exception:
        username = user_id
        user_image = None

    st.subheader("Log a Workout")
    with st.form("activity_workout_form"):
        date_col, start_col, end_col = st.columns(3)
        with date_col:
            workout_date = st.date_input("Workout date", value=date.today())
        with start_col:
            start_time = st.time_input("Start time", value=datetime.now().time(), step=300)
        with end_col:
            end_time = st.time_input("End time", value=datetime.now().time(), step=300)

        dist_col, steps_col, cal_col = st.columns(3)
        with dist_col:
            distance = st.number_input("Distance (miles)", min_value=0.0, step=0.1, format="%.1f")
        with steps_col:
            steps = st.number_input("Steps", min_value=0, step=100)
        with cal_col:
            calories_burned = st.number_input("Calories burned", min_value=0, step=10)

        content = st.text_area("Workout notes")
        post_image = st.file_uploader("Workout image", type=["jpg", "jpeg", "png"])
        submitted = st.form_submit_button("Log Workout")

    if submitted:
        start_timestamp = datetime.combine(workout_date, start_time)
        end_timestamp = datetime.combine(workout_date, end_time)

        if end_timestamp < start_timestamp:
            st.warning("End time must be after the start time.")
        elif distance == 0 and steps == 0 and calories_burned == 0:
            st.warning("Enter at least one workout stat before logging your workout.")
        elif len(content) > 280:
            st.warning("workout notes must be 280 characters or fewer")
        else:
            workout = add_user_workout(
                user_id,
                start_timestamp=start_timestamp,
                end_timestamp=end_timestamp,
                distance=float(distance),
                steps=int(steps),
                calories_burned=int(calories_burned),
            )
            activity_entry = {
                "username": username,
                "user_image": user_image,
                "timestamp": start_timestamp,
                "content": "\n\n".join(
                    part for part in [
                        content.strip(),
                        (
                            f"Distance: {workout['distance']} miles | "
                            f"Steps: {workout['steps']:,} | "
                            f"Calories: {workout['calories_burned']}"
                        ),
                    ] if part
                ),
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

    all_workouts = get_user_workouts(user_id) or []

    if not all_workouts:
        st.info("You have no recorded workouts yet. Get moving!")
        return

    def parse_timestamp(workout):
        ts = workout.get('start_timestamp', '')
        try:
            return datetime.strptime(str(ts), '%Y-%m-%d %H:%M:%S')
        except Exception:
            return datetime.min

    sorted_workouts = sorted(all_workouts, key=parse_timestamp, reverse=True)
    recent_workouts = sorted_workouts[:3]

    display_activity_summary(sorted_workouts)
    st.write("---")

    st.subheader("Recent Sessions")
    display_recent_workouts(recent_workouts)
    st.write("---")

