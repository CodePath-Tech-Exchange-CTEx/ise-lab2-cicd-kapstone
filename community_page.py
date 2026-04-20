#############################################################################
# community_page.py
#############################################################################

import streamlit as st
from data_fetcher import add_friends_to_user, add_user_post, get_available_user_ids, get_user_profile, get_user_posts, get_user_workouts
from modules import display_post
from datetime import datetime


def read_bytes(uploaded):
    return uploaded.read() if uploaded is not None else None


def display_community_page(user_id):
    """Displays the community page for the given user."""

    st.markdown("""
    <div class="page-title">COMMUNITY</div>
    <div class="page-subtitle">See what you and your friends are up to</div>
    <hr class="custom-divider">
    """, unsafe_allow_html=True)

    all_workouts = get_user_workouts(user_id) or []

    def parse_workout_timestamp(workout):
        ts = workout.get('start_timestamp', '')
        try:
            return datetime.strptime(str(ts), '%Y-%m-%d %H:%M:%S')
        except Exception:
            return datetime.min

    sorted_workouts = sorted(all_workouts, key=parse_workout_timestamp, reverse=True)
    recent_workouts = sorted_workouts[:3]

    try:
        profile = get_user_profile(user_id)
    except Exception as e:
        st.error(f"Could not load your profile: {e}")
        return

    share_col, friends_col = st.columns([1.6, 1])

    with share_col:
        st.markdown('<div class="section-title">Share With Community</div>', unsafe_allow_html=True)

        latest = recent_workouts[0] if recent_workouts else {}
        steps = latest.get('steps') or 0
        calories = latest.get('calories_burned') or latest.get('calories') or 0
        distance = latest.get('distance') or 0

        default_share_message = (
            f"My latest workout: {distance} miles, {steps:,} steps, {calories} calories burned!"
        )
        share_message = st.text_area(
            "Write your post",
            value=default_share_message,
            key="community_share_message",
            height=120,
        ).strip()
        share_image = st.file_uploader(
            "Add an image",
            type=["jpg", "jpeg", "png"],
            key="community_share_image",
        )

        if "share_success" not in st.session_state:
            st.session_state["share_success"] = False

        if st.button("📤 Share to Community", use_container_width=True):
            if not share_message:
                st.warning("Please enter a message before sharing.")
                st.session_state["share_success"] = False
            else:
                add_user_post(
                    user_id,
                    share_message,
                    image=read_bytes(share_image),
                    timestamp=datetime.now(),
                )
                st.session_state["share_success"] = True

        if st.session_state.get("share_success"):
            st.success("✅ Your post has been shared!")

    with friends_col:
        st.markdown('<div class="section-title">Manage Friends</div>', unsafe_allow_html=True)
        available_friends = [uid for uid in get_available_user_ids() if uid != user_id]
        selected_friends = st.multiselect(
            "Add friends",
            options=available_friends,
            default=profile.get('friends', []),
            key=f"community_friends_{user_id}",
        )

        if st.button("💾 Save Friends", use_container_width=True):
            newly_added = add_friends_to_user(user_id, selected_friends)
            if newly_added:
                st.success("Friends updated!")
            else:
                st.info("No new friends were added.")
            profile = get_user_profile(user_id)

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Community Feed</div>', unsafe_allow_html=True)

    friend_ids = profile.get('friends', [])
    author_ids = [user_id] + [fid for fid in friend_ids if fid != user_id]

    all_posts = []
    for author_id in author_ids:
        try:
            author_posts = get_user_posts(author_id)
            for post in author_posts:
                post['user_id'] = post.get('user_id', author_id)
            all_posts.extend(author_posts)
        except Exception:
            continue

    if not all_posts:
        st.info("No posts yet. Share your first update above!")
        return

    def parse_timestamp(post):
        ts = post.get('timestamp', '')
        try:
            return datetime.strptime(str(ts), '%Y-%m-%d %H:%M:%S')
        except Exception:
            return datetime.min

    all_posts.sort(key=parse_timestamp, reverse=True)
    posts_to_show = all_posts[:10]

    st.markdown(f'<div style="font-size:12px;color:#4a5568;margin-bottom:16px;">{len(posts_to_show)} recent post(s)</div>', unsafe_allow_html=True)

    for post in posts_to_show:
        author_id = post.get('user_id', 'Unknown')
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

        if not content and not post_image:
            continue

        display_post(username, user_image, timestamp, content, post_image)