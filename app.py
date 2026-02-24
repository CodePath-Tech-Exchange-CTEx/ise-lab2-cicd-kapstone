#############################################################################
# app.py
#
# This file contains the entrypoint for the app.
#
#############################################################################

import streamlit as st
from datetime import datetime
from modules import display_my_custom_component, display_post, display_genai_advice, display_activity_summary, display_recent_workouts
from data_fetcher import get_user_posts, get_genai_advice, get_user_profile, get_user_sensor_data, get_user_workouts

userId = 'user1'


def display_app_page():
    """Displays the home page of the app."""
    st.title('Welcome to SDS!')

    # An example of displaying a custom component called "my_custom_component"
    value = st.text_input('Enter your name')
    display_my_custom_component(value)
   
   # Display post
    username = st.text_input("Enter username")
    user_image = st.file_uploader("profile image", type=["jpg", "jpeg", "png"])
    content = st.text_area("workout description")
    post_image = st.file_uploader("workout image", type=["jpg", "jpeg", "png"])
    if st.button("Post"):
        if username == "":
            st.warning("please enter username")
        elif len(content)> 280 or len(content)< 1:
            st.warning("description must be between 1 and 280 characters")
        else:    
            display_post(username, user_image, datetime.now(),content, post_image) 


# This is the starting point for your app. You do not need to change these lines
if __name__ == '__main__':
    display_app_page()
