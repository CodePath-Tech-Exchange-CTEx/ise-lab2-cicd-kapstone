#############################################################################
# modules.py
#
# This file contains modules that may be used throughout the app.
#
# You will write these in Unit 2. Do not change the names or inputs of any
# function other than the example.
#############################################################################

from internals import create_component
import streamlit as st


# This one has been written for you as an example. You may change it as wanted.
def display_my_custom_component(value):
    """Displays a 'my custom component' which showcases an example of how custom
    components work.

    value: the name you'd like to be called by within the app
    """
    # Define any templated data from your HTML file. The contents of
    # 'value' will be inserted to the templated HTML file wherever '{{NAME}}'
    # occurs. You can add as many variables as you want.
    data = {
        'NAME': value,
    }
    # Register and display the component by providing the data and name
    # of the HTML file. HTML must be placed inside the "custom_components" folder.
    html_file_name = "my_custom_component"
    create_component(data, html_file_name)


def display_post(username, user_image, timestamp, content, post_image):
    """
    Displays the post from a user.

    Parameters:
        username (str): username for the user who made the post
        user_image (UploadedFile): image for the user who made the post
        timestamp (datetime): time the post was made
        content (str): description of post
        post_image (UploadedFile): image for the post

    Returns:
        Nothing
    """

    col1, col2 = st.columns(2)
    with col1:
        if user_image:
            st.image(user_image, width=50)
    with col2:
        st.write(username)
    if post_image:
        st.image(post_image)
    st.write(content)
    st.caption(timestamp.strftime("%B %d, %Y at %I:%M %p"))


def display_activity_summary(workouts_list):
    """Write a good docstring here."""
    pass


def display_recent_workouts(workouts_list):
    """Write a good docstring here."""
    pass


def display_genai_advice(timestamp, content, image):
    """Write a good docstring here."""
    pass
