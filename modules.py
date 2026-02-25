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
    if not workouts_list: 
        print("No workouts recorded.") 
        return None 

    
    total_dist = sum(w.get('distance', 0) for w in workouts_list) 
    # Line written by Gemini
    total_steps = sum(w.get('steps', 0) for w in workouts_list)
     # Line written by Gemini
    total_cals = sum(w.get('calories', 0) for w in workouts_list) 
    # Line written by Gemini

    # Header section 
    print("\n      Activity Summary")
    print("==============================") 
    print("\nTotals Summary") 
    # Change 'workouts' to 'workouts_list' here too
    print(f"Total Workouts: {len(workouts_list)}") 
    print(f"Total Distance: {total_dist:.1f} miles") 
    print(f"Total Steps: {total_steps:,}") 
    print(f"Total Calories: {total_cals}") 
    print("------------------------------") 

    for i, w in enumerate(workouts_list, 1): 
        # Line written by Gemini
        start = w.get('start_time', 'None') 
        # Line written by Gemini
        end = w.get('end_time', 'None') 
        # Line written by Gemini
        dist = w.get('distance', 0) 
        # Line written by Gemini
        steps = w.get('steps', 0) 
        # Line written by Gemini
        cals = w.get('calories', 0) 
        # Line written by Gemini

        print(f"\nWorkout {i}") 
        print(f"Start: {start}") 
        print(f"End: {end}") 
        print(f"Distance: {dist} miles") 
        print(f"Steps: {steps:,}") 
        print(f"Calories: {cals}") 
        print("------------------------------") 

    return None
    
    # Render the component using the HTML file in custom_components/
    create_component(workouts_list, "display_activity_summary") 


def display_recent_workouts(workouts_list=[]):
    """
    Displays a list of recent workouts using a custom HTML component.
    Each workout shows its distance, steps, and calories.

    Parameters:
        workouts_list (list): A list of workout dictionaries, each containing:
            - 'distance': miles traveled
            - 'steps': steps taken  
            - 'calories': calories burned
            - 'start_time': when the workout started
            - 'end_time': when the workout ended
    """

    # If no workouts, show a friendly message and stop
    if not workouts_list:
        st.info("No recent workouts to show.")
        return

    # Step A: Loop through workouts and build one big HTML string
    cards_html = ""  # start with empty string

    for i, workout in enumerate(workouts_list, start=1):
        # Safely get each value, defaulting if missing
        start    = workout.get('start_time', 'Unknown')
        end      = workout.get('end_time', 'Unknown')
        distance = workout.get('distance', 0)
        steps    = workout.get('steps', 0)
        calories = workout.get('calories', 0)

        # Build one card's HTML and add it to the string
        cards_html += f"""
        <div style="border: 1px solid #ddd;
                    padding: 14px;
                    border-radius: 10px;
                    background-color: #f9f9f9;
                    margin-bottom: 8px;">
            <p style="margin: 0 0 6px 0; font-weight: bold; color: #444;">
                Workout {i}
            </p>
            <p style="margin: 2px 0;">📍 <strong>Distance:</strong> {distance} miles</p>
            <p style="margin: 2px 0;">👟 <strong>Steps:</strong> {steps:,}</p>
            <p style="margin: 2px 0;">🔥 <strong>Calories:</strong> {calories}</p>
            <p style="margin: 6px 0 0 0; font-size: 0.8em; color: #888;">
                {start} → {end}
            </p>
        </div>
        """

    # Step B: Pass the finished HTML string to the component
    data = {
        'WORKOUT_CARDS': cards_html
    }
    create_component(data, "display_recent_workouts")


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
        if image:
            st.image(image, caption="Stay Motivated!", width='stretch')