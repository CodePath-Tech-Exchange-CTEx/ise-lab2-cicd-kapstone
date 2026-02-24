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
    """
    Displays a summary of total activity statistics across all workouts.
    
    Args:
        workouts_list: A list of dictionaries containing workout metrics.
    """ # Line written by Gemini
    # Calculate totals safely using .get() to avoid KeyErrors
    total_distance = sum(w.get('distance', 0) for w in workouts_list) 
    total_steps = sum(w.get('steps', 0) for w in workouts_list) 
    total_calories = sum(w.get('calories', 0) for w in workouts_list) 
    
    # Format distance to 1 decimal place as requested
    total_distance = round(total_distance, 1) 
    
    # Prepare the data dictionary for the HTML template
    data = {
        'TOTAL_DISTANCE': str(total_distance), 
        'TOTAL_STEPS': str(total_steps), 
        'TOTAL_CALORIES': str(total_calories), 
        'NUM_WORKOUTS': len(workouts_list) 
    } 
    
    # Render the component using the HTML file in custom_components/
    create_component(data, "display_activity_summary") 


def display_recent_workouts(workouts_list):
    """
    Displays a list of recent workouts, each showing distance, steps, and calories.
    """ # Line written by Gemini
    
    # We pass the list directly to the component. 
    # Your HTML will use a loop to display each one.
    data = {
        'WORKOUTS': workouts_list # Line written by Gemini
    } # Line written by Gemini
    
    create_component(data, "display_recent_workouts") # Line written by Gemini


def display_genai_advice(timestamp, content, image):
    def display_genai_advice(timestamp, content, image):
        import streamlit as st

    st.subheader("💡 AI-Powered Advice")
    st.caption(f"Generated on: {timestamp}")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### Your Personalized Advice")
        st.write(content)

    with col2:
        st.image(image, caption="Stay Motivated!", use_column_width=True)
    pass
