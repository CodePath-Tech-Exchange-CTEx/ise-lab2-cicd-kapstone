#############################################################################
# community_page.py
#
# Revamped community page with polished UI.
#
#############################################################################

import streamlit as st
from data_fetcher import get_user_profile, get_user_posts, get_genai_advice
from modules import display_post, display_genai_advice
from datetime import datetime


def display_community_page(user_id):
    """Displays the community page for the given user."""

    st.markdown("""
    <div class="page-title">COMMUNITY</div>
    <div class="page-subtitle">See what your friends are up to</div>
    <hr class="custom-divider">
    """, unsafe_allow_html=True)

    # --- GenAI Advice Section ---
    st.markdown('<div class="section-title">Daily Motivation</div>', unsafe_allow_html=True)
    advice = get_genai_advice(user_id)
    if advice:
        display_genai_advice(advice['timestamp'], advice['content'], advice['image'])
    else:
        st.info("No advice available right now. Check back later!")

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    # --- Friends' Posts Section ---
    st.markdown('<div class="section-title">Friends\' Posts</div>', unsafe_allow_html=True)

    try:
        profile = get_user_profile(user_id)
    except Exception as e:
        st.error(f"Could not load your profile: {e}")
        return

    friend_ids = profile.get('friends', [])

    if not friend_ids:
        st.info("No friends added yet. Add some friends to see their posts!")
        return

    all_posts = []
    for friend_id in friend_ids:
        try:
            friend_posts = get_user_posts(friend_id)
            for post in friend_posts:
                post['user_id'] = post.get('user_id', friend_id)
            all_posts.extend(friend_posts)
        except Exception:
            continue

    if not all_posts:
        st.info("None of your friends have posted yet!")
        return

    def parse_timestamp(post):
        ts = post.get('timestamp', '')
        try:
            return datetime.strptime(str(ts), '%Y-%m-%d %H:%M:%S')
        except Exception:
            return datetime.min

    all_posts.sort(key=parse_timestamp, reverse=True)
    posts_to_show = all_posts[:10]

    st.markdown(f'<div style="font-size:12px;color:#4a5568;margin-bottom:16px;">{len(posts_to_show)} post(s) from your friends</div>', unsafe_allow_html=True)

    for post in posts_to_show:
        author_id = post.get('user_id', 'Unknown')

        try:
            friend_profile = get_user_profile(author_id)
            username = friend_profile.get('username', author_id)
            user_image = friend_profile.get('profile_image', None)
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

        # Skip posts with no content and no image
        if not content and not post_image:
            continue

        display_post(username, user_image, timestamp, content, post_image)