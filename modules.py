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
import os


# This one has been written for you as an example. You may change it as wanted.
def display_my_custom_component(value):
    """Displays a 'my custom component' which showcases an example of how custom
    components work.

    value: the name you'd like to be called by within the app
    """
    data = {
        'NAME': value,
    }
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
            try:
                st.image(user_image, width=50)
            except Exception:
                st.caption("Profile image unavailable")
    with col2:
        st.write(username)
    if post_image:
        try:
            if isinstance(post_image, str) and not (post_image.startswith("http://") or post_image.startswith("https://")):
                if os.path.exists(post_image):
                    st.image(post_image)
                else:
                    st.caption("Post image unavailable")
            else:
                st.image(post_image)
        except Exception:
            st.caption("Post image unavailable")
    st.write(content)
    st.caption(timestamp.strftime("%B %d, %Y at %I:%M %p"))


def display_activity_summary(workouts_list):
    if not workouts_list:
        st.write("No workouts recorded.")
        return None

    total_dist = sum(w.get('distance') or 0 for w in workouts_list)
    total_steps = sum(w.get('steps') or 0 for w in workouts_list)
    total_cals = sum((w.get('calories_burned') if w.get('calories_burned') is not None else w.get('calories')) or 0 for w in workouts_list)

    st.header("Activity Summary")
    st.write("==============================")
    st.subheader("Totals Summary")

    st.write(f"**Total Workouts:** {len(workouts_list)}")
    st.write(f"**Total Distance:** {total_dist:.1f} miles")
    st.write(f"**Total Steps:** {total_steps:,}")
    st.write(f"**Total Calories:** {total_cals}")
    st.write("------------------------------")

    for i, workout in enumerate(workouts_list, 1):
        start = workout.get('start_timestamp', 'Unknown')
        end = workout.get('end_timestamp', 'Unknown')
        dist = workout.get('distance', 0)
        steps = workout.get('steps', 0)
        calories = workout.get('calories_burned')
        if calories is None:
            calories = workout.get('calories', 0)

        st.write(f"### Workout {i}")
        st.write(f"**Start:** {start} | **End:** {end}")
        st.write(f"**Distance:** {dist} miles")
        st.write(f"**Steps:** {steps:,}")
        st.write(f"**Calories:** {calories}")
        st.write("------------------------------")

    return None


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

    if not workouts_list:
        st.info("No recent workouts to show.")
        return

    cards_html = ""

    for i, workout in enumerate(workouts_list, start=1):
        start = workout.get('start_timestamp', 'Unknown')
        end = workout.get('end_timestamp', 'Unknown')
        distance = workout.get('distance', 0)
        steps = workout.get('steps', 0)
        calories = workout.get('calories_burned')
        if calories is None:
            calories = workout.get('calories', 0)

        cards_html += f"""
        <div style="border: 1px solid #ddd;
                    padding: 14px;
                    border-radius: 10px;
                    background-color: #f9f9f9;
                    margin-bottom: 8px;">
            <p style="margin: 0 0 6px 0; font-weight: bold; color: #444;">
                Workout {i}
            </p>
            <p style="margin: 2px 0;"><strong>Distance:</strong> {distance} miles</p>
            <p style="margin: 2px 0;"><strong>Steps:</strong> {steps:,}</p>
            <p style="margin: 2px 0;"><strong>Calories:</strong> {calories}</p>
            <p style="margin: 6px 0 0 0; font-size: 0.8em; color: #888;">
                {start} to {end}
            </p>
        </div>
        """

    data = {
        'WORKOUT_CARDS': cards_html
    }
    create_component(data, "display_recent_workouts")


def display_genai_advice(timestamp, content, image):

    st.subheader("AI-Powered Advice")
    st.caption(f"Generated on: {timestamp}")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### Your Personalized Advice")
        st.write(content)

    with col2:
        if image:
            st.image(image, caption="Stay Motivated!", width=300)
