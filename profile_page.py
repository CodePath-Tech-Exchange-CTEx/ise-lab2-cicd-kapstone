#############################################################################
# profile_page.py
#
# This file contains the profile creation page for the app.
#############################################################################

from datetime import date

import streamlit as st

from data_fetcher import add_user_profile


def read_bytes(uploaded):
    return uploaded.read() if uploaded is not None else None


def display_profile_page():
    """Displays a page where a user can create a new client profile."""
    st.title("Create Client Profile")
    st.write("Add a new client with the same profile details as the built-in users.")
    st.write("---")

    with st.form("create_profile_form"):
        identity_col, details_col = st.columns(2)
        with identity_col:
            user_id = st.text_input("User code", help="Example: user5")
            full_name = st.text_input("Full name")
            username = st.text_input("Username")
        with details_col:
            date_of_birth = st.date_input(
                "Date of birth",
                value=date(2000, 1, 1),
                min_value=date(1900, 1, 1),
                max_value=date.today(),
            )
            profile_image = st.file_uploader(
                "Profile image",
                type=["jpg", "jpeg", "png"],
            )
        submitted = st.form_submit_button("Create Profile")

    if not submitted:
        return

    if not user_id.strip():
        st.warning("Please enter a user code.")
        return

    if not full_name.strip():
        st.warning("Please enter a full name.")
        return

    if not username.strip():
        st.warning("Please enter a username.")
        return

    try:
        created_profile = add_user_profile(
            user_id=user_id,
            full_name=full_name,
            username=username,
            date_of_birth=date_of_birth,
            profile_image=read_bytes(profile_image),
        )
    except ValueError as exc:
        st.error(str(exc))
        return

    st.session_state["current_user_id"] = created_profile["user_id"]
    st.success(f"Profile created for {created_profile['full_name']}. You can now use user code `{created_profile['user_id']}`.")

    st.subheader("Profile Preview")
    st.write(f"**Full Name:** {created_profile['full_name']}")
    st.write(f"**Username:** {created_profile['username']}")
    st.write(f"**Date of Birth:** {created_profile['date_of_birth']}")
    if created_profile['profile_image']:
        st.image(created_profile['profile_image'], width=150)
    else:
        st.write("**Profile Image:** None")
    st.write("**Friends:** Add friends from the Community page.")
