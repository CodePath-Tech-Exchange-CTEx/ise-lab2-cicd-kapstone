#############################################################################
# community_page.py
#
# This file contains the community page for the app.
# It displays the first 10 posts from a user's friends ordered by timestamp,
# and one piece of GenAI advice and encouragement.
#############################################################################

import streamlit as st
from data_fetcher import get_user_profile, get_user_posts, get_genai_advice
from modules import display_post, display_genai_advice
from datetime import datetime


def display_community_page(user_id):
    """Displays the community page for the given user.

    Shows the first 10 posts from the user's friends ordered by timestamp,
    and one piece of GenAI advice and encouragement.

    Parameters:
        user_id (str): the ID of the current user
    """

    st.title("🌍 Community")
    st.write("See what your friends are up to!")
    st.write("---")

    # --- GenAI Advice Section ---
    st.subheader("✨ Your Daily Motivation")
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

    # --- Friends' Posts Section ---
    st.subheader("📰 Friends' Posts")

    # Step 1: Get the current user's profile to find their friends
    try:
        profile = get_user_profile(user_id)
    except Exception as e:
        st.error(f"Could not load your profile: {e}")
        return

    friend_ids = profile.get('friends', [])

    if not friend_ids:
        st.info("You have no friends added yet. Add some friends to see their posts here!")
        return

    # Step 2: Collect all posts from each friend
    all_posts = []
    for friend_id in friend_ids:
        try:
            friend_posts = get_user_posts(friend_id)
            # Attach friend_id to each post in case it's missing
            for post in friend_posts:
                post['user_id'] = post.get('user_id', friend_id)
            all_posts.extend(friend_posts)
        except Exception:
            # If we can't get a friend's posts, skip them gracefully
            continue

    if not all_posts:
        st.info("None of your friends have posted yet!")
        return

    # Step 3: Sort all posts by timestamp (oldest first) and take first 10
    def parse_timestamp(post):
        ts = post.get('timestamp', '')
        try:
            return datetime.strptime(str(ts), '%Y-%m-%d %H:%M:%S')
        except Exception:
            return datetime.min

    all_posts.sort(key=parse_timestamp)
    posts_to_show = all_posts[:10]

    # Step 4: Display each post
    st.write(f"Showing {len(posts_to_show)} post(s) from your friends:")
    st.write("")

    for post in posts_to_show:
        author_id = post.get('user_id', 'Unknown')

        # Try to get the friend's profile for their username and image
        try:
            friend_profile = get_user_profile(author_id)
            username = friend_profile.get('username', author_id)
            user_image = friend_profile.get('profile_image', None)
        except Exception:
            username = author_id
            user_image = None

        # Parse timestamp safely
        ts = post.get('timestamp', '')
        try:
            timestamp = datetime.strptime(str(ts), '%Y-%m-%d %H:%M:%S')
        except Exception:
            timestamp = datetime.now()

        content = post.get('content', '')
        post_image = post.get('image', None)

        display_post(username, user_image, timestamp, content, post_image)
        st.write("---")
