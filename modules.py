#############################################################################
# modules.py
#
# This file contains modules that may be used throughout the app.
#
# You will write these in Unit 2. Do not change the names or inputs of any
# function other than the example.
#############################################################################

from internals import create_component


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
    """Write a good docstring here."""
    pass


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
    """Write a good docstring here."""
    pass


def display_genai_advice(timestamp, content, image):
    """Write a good docstring here."""
    pass
