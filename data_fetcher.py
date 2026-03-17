#############################################################################
# data_fetcher.py
#
# This file contains functions to fetch data needed for the app.
#
# You will re-write these functions in Unit 3, and are welcome to alter the
# data returned in the meantime. We will replace this file with other data when
# testing earlier units.
#############################################################################

import random

users = {
    'user1': {
        'full_name': 'Remi',
        'username': 'remi_the_rems',
        'date_of_birth': '1990-01-01',
        'profile_image': 'https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg',
        'friends': ['user2', 'user3', 'user4'],
    },
    'user2': {
        'full_name': 'Blake',
        'username': 'blake',
        'date_of_birth': '1990-01-01',
        'profile_image': 'https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg',
        'friends': ['user1'],
    },
    'user3': {
        'full_name': 'Jordan',
        'username': 'jordanjordanjordan',
        'date_of_birth': '1990-01-01',
        'profile_image': 'https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg',
        'friends': ['user1', 'user4'],
    },
    'user4': {
        'full_name': 'Gemmy',
        'username': 'gems',
        'date_of_birth': '1990-01-01',
        'profile_image': 'https://upload.wikimedia.org/wikipedia/commons/c/c8/Puma_shoes.jpg',
        'friends': ['user1', 'user3'],
    },
}


def get_user_workouts(user_id):
    """Returns a list of workouts for the given user.

    Searches through the workouts table and returns all workouts
    that belong to the given user_id. Handles missing/null fields gracefully.

    Returns a list of dicts with keys:
        workout_id, start_timestamp, end_timestamp,
        start_lat_lng, end_lat_lng, distance, steps, calories_burned
    """
    # This is our "table" of all workouts across all users
    workouts_table = [
        {
            'user_id': 'user1',
            'workout_id': 'workout1',
            'start_timestamp': '2024-01-01 07:00:00',
            'end_timestamp': '2024-01-01 07:30:00',
            'start_lat_lng': (36.166, -86.783),
            'end_lat_lng': (36.170, -86.780),
            'distance': 2.5,
            'steps': 4000,
            'calories_burned': 220,
        },
        {
            'user_id': 'user1',
            'workout_id': 'workout2',
            'start_timestamp': '2024-01-02 08:00:00',
            'end_timestamp': '2024-01-02 08:45:00',
            'start_lat_lng': (36.166, -86.783),
            'end_lat_lng': (36.175, -86.790),
            'distance': None,       # sometimes distance is not recorded
            'steps': 5200,
            'calories_burned': 300,
        },
        {
            'user_id': 'user2',
            'workout_id': 'workout3',
            'start_timestamp': '2024-01-03 06:30:00',
            'end_timestamp': '2024-01-03 07:00:00',
            'start_lat_lng': None,  # sometimes location is not recorded
            'end_lat_lng': None,
            'distance': 1.8,
            'steps': 2800,
            'calories_burned': 150,
        },
    ]

    result = []

    # Loop through every workout, only keep ones matching this user
    for workout in workouts_table:
        if workout['user_id'] == user_id:
            result.append({
                'workout_id': workout.get('workout_id'),
                'start_timestamp': workout.get('start_timestamp'),
                'end_timestamp': workout.get('end_timestamp'),
                'start_lat_lng': workout.get('start_lat_lng'),
                'end_lat_lng': workout.get('end_lat_lng'),
                'distance': workout.get('distance'),
                'steps': workout.get('steps'),
                'calories_burned': workout.get('calories_burned'),
            })

    return result


def get_user_sensor_data(user_id, workout_id):
    """Returns sensor data for a given workout.

    user_id is accepted for compatibility but filtering is done
    by workout_id since workout_ids are unique per user.

    Returns a list of dicts with keys:
        sensor_type, timestamp, data, units
    """
    # This is our "table" of all sensor readings across all workouts
    sensor_data_table = [
        {
            'workout_id': 'workout1',
            'sensor_type': 'heart_rate',
            'timestamp': '2024-01-01 07:05:00',
            'data': 120,
            'units': 'bpm',
        },
        {
            'workout_id': 'workout1',
            'sensor_type': 'accelerometer',
            'timestamp': '2024-01-01 07:10:00',
            'data': 9.8,
            'units': 'm/s^2',
        },
        {
            'workout_id': 'workout2',
            'sensor_type': 'temperature',
            'timestamp': '2024-01-02 08:15:00',
            'data': None,   # sometimes sensor data is missing
            'units': 'C',
        },
    ]

    sensor_data = []

    # Loop through every record, only keep ones matching this workout
    for record in sensor_data_table:
        if record['workout_id'] == workout_id:
            sensor_data.append({
                'sensor_type': record.get('sensor_type'),
                'timestamp': record.get('timestamp'),
                'data': record.get('data'),
                'units': record.get('units'),
            })

    return sensor_data


def get_user_profile(user_id):
    """Returns information about the given user.

    This function currently returns random data. You will re-write it in Unit 3.
    """
    if user_id not in users:
        raise ValueError(f'User {user_id} not found.')
    return users[user_id]


def get_user_posts(user_id):
    """Returns a list of a user's posts.

    This function currently returns random data. You will re-write it in Unit 3.
    """
    content = random.choice([
        'Had a great workout today!',
        'The AI really motivated me to push myself further, I ran 10 miles!',
    ])
    return [{
        'user_id': user_id,
        'post_id': 'post1',
        'timestamp': '2024-01-01 00:00:00',
        'content': content,
        'image': 'image_url',
    }]


def get_genai_advice(user_id):
    """Returns the most recent advice from the genai model.

    This function currently returns random data. You will re-write it in Unit 3.
    """
    advice = random.choice([
        'Your heart rate indicates you can push yourself further. You got this!',
        "You're doing great! Keep up the good work.",
        'You worked hard yesterday, take it easy today.',
        'You have burned 100 calories so far today!',
    ])
    image = random.choice([
        'https://plus.unsplash.com/premium_photo-1669048780129-051d670fa2d1?q=80&w=3870&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
        None,
    ])
    return {
        'advice_id': 'advice1',
        'timestamp': '2024-01-01 00:00:00',
        'content': advice,
        'image': image,
    }
