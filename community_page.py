#############################################################################
# community_page.py
#
# This file contains the community page for the app.
# It displays the latest posts from the current user and their friends,
# and one piece of GenAI advice and encouragement.
#############################################################################

import streamlit as st
from data_fetcher import add_user_post, get_user_profile, get_user_posts, get_genai_advice, get_user_workouts
from modules import display_post, display_genai_advice
from datetime import datetime


def display_community_page(user_id):
    """Displays the community page for the given user.

    Shows the latest posts from the current user and their friends,
    and one piece of GenAI advice and encouragement.

    Parameters:
        user_id (str): the ID of the current user
    """

    st.title("Community")
    st.write("See what you and your friends are up to!")
    st.write("---")

    # --- GenAI Advice Section ---
    st.subheader("Your Daily Motivation")
    advice = get_genai_advice(user_id)
    if advice:
        display_genai_advice(
            advice['timestamp'],
            advice['content'],
            advice['image']
        )
    else:
        st.info("No advice available right now. Check back later!")

    st.write("---")

    all_workouts = get_user_workouts(user_id) or []

    def parse_workout_timestamp(workout):
        ts = workout.get('start_timestamp', '')
        try:
            return datetime.strptime(str(ts), '%Y-%m-%d %H:%M:%S')
        except Exception:
            return datetime.min

    sorted_workouts = sorted(all_workouts, key=parse_workout_timestamp, reverse=True)
    recent_workouts = sorted_workouts[:3]

    st.subheader("Share With the Community")
    st.write("Proud of your progress? Share a stat with your friends!")

    latest = recent_workouts[0] if recent_workouts else {}
    steps = latest.get('steps') or 0
    calories = latest.get('calories_burned') or latest.get('calories') or 0
    distance = latest.get('distance') or 0

    stat_choice = st.selectbox(
        "Choose a stat to share:",
        options=["Steps", "Calories Burned", "Distance"],
        key="community_stat_choice"
    )

    if stat_choice == "Steps":
        share_message = f"Look at this, I walked {steps:,} steps today! #FitnessGoals"
    elif stat_choice == "Calories Burned":
        share_message = f"Just burned {calories} calories in my latest workout! #Fitness"
    else:
        share_message = f"I covered {distance} miles in my latest workout! #Running"

    st.write(f"**Preview:** {share_message}")

    if "share_success" not in st.session_state:
        st.session_state["share_success"] = False

    if st.button("Share to Community"):
        add_user_post(user_id, share_message, timestamp=datetime.now())
        st.session_state["share_success"] = True

    if st.session_state.get("share_success"):
        st.success("Your post has been shared with the community!")

    st.write("---")

    # --- Community Feed Section ---
    st.subheader("Community Feed")

    # Step 1: Get the current user's profile to find their friends
    try:
        profile = get_user_profile(user_id)
    except Exception as e:
        st.error(f"Could not load your profile: {e}")
        return

    friend_ids = profile.get('friends', [])
    author_ids = [user_id] + [friend_id for friend_id in friend_ids if friend_id != user_id]

    # Step 2: Collect all posts from the current user and each friend
    all_posts = []
    for author_id in author_ids:
        try:
            author_posts = get_user_posts(author_id)
            for post in author_posts:
                post['user_id'] = post.get('user_id', author_id)
            all_posts.extend(author_posts)
        except Exception:
            # If we can't get an author's posts, skip them gracefully
            continue

    if not all_posts:
        st.info("No posts are available yet. Share your first update above.")
        return

    # Step 3: Sort all posts by timestamp (newest first) and take the latest 10
    def parse_timestamp(post):
        ts = post.get('timestamp', '')
        try:
            return datetime.strptime(str(ts), '%Y-%m-%d %H:%M:%S')
        except Exception:
            return datetime.min

    all_posts.sort(key=parse_timestamp, reverse=True)
    posts_to_show = all_posts[:10]

    # Step 4: Display each post
    st.write(f"Showing {len(posts_to_show)} recent post(s):")
    st.write("")

    for post in posts_to_show:
        author_id = post.get('user_id', 'Unknown')

        # Try to get the author's profile for their username and image
        try:
            author_profile = get_user_profile(author_id)
            username = author_profile.get('username', author_id)
            user_image = author_profile.get('profile_image', None)
        except Exception:
            username = author_id
            user_image = None

        ts = post.get('timestamp', '')
        try:
            timestamp = datetime.strptime(str(ts), '%Y-%m-%d %H:%M:%S')
        except Exception:
            timestamp = datetime.now()

        content = post.get('content', '')
        post_image = post.get('image', None)

        display_post(username, user_image, timestamp, content, post_image)
        st.write("---")
