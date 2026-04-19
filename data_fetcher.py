#############################################################################
# data_fetcher.py
#
# This file contains functions to fetch data needed for the app.
#
# You will re-write these functions in Unit 3, and are welcome to alter the
# data returned in the meantime. We will replace this file with other data when
# testing earlier units.
#############################################################################

import os
import random
import uuid
from datetime import datetime
from google.cloud import bigquery
import vertexai
from vertexai.generative_models import GenerativeModel

project_id = os.environ.get("PROJECT_ID", "johnny-aryeetey-csudh")
client = None

def get_client():
    global client
    if client is None:
        client = bigquery.Client()
    return client

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

posts_table = [
    {
        'post_id': 'post1',
        'AuthorId': 'user1',
        'timestamp': '2026-01-01 00:00:00',
        'content': None,
        'image': 'https://example.com/workout.jpg',
    },
    {
        'post_id': 'post2',
        'AuthorId': 'user1',
        'timestamp': '2026-01-02 12:00:00',
        'content': 'Feeling sore but motivated.',
        'image': None,
    },
    {
        'post_id': 'post3',
        'AuthorId': 'user2',
        'timestamp': '2026-01-03 09:00:00',
        'content': 'Forgot my camera today!',
        'image': None,
    },
]

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
        'distance': None,
        'steps': 5200,
        'calories_burned': 300,
    },
    {
        'user_id': 'user2',
        'workout_id': 'workout3',
        'start_timestamp': '2024-01-03 06:30:00',
        'end_timestamp': '2024-01-03 07:00:00',
        'start_lat_lng': None,
        'end_lat_lng': None,
        'distance': 1.8,
        'steps': 2800,
        'calories_burned': 150,
    },
]


def user_exists(user_id):
    """Returns True when the given user ID exists in the in-memory user store."""
    return user_id in users


def get_available_user_ids():
    """Returns the list of valid user IDs."""
    return sorted(users.keys())


def add_user_profile(user_id, full_name, username, date_of_birth, profile_image, friends=None):
    """Adds a user profile to the in-memory data store used by the app."""
    normalized_user_id = (user_id or "").strip()
    normalized_username = (username or "").strip()

    if not normalized_user_id:
        raise ValueError("User ID is required.")
    if normalized_user_id in users:
        raise ValueError(f"User {normalized_user_id} already exists.")
    if not normalized_username:
        raise ValueError("Username is required.")

    normalized_friends = []
    for friend_id in friends or []:
        if friend_id in users and friend_id != normalized_user_id and friend_id not in normalized_friends:
            normalized_friends.append(friend_id)

    normalized_profile_image = profile_image
    if isinstance(profile_image, str):
        normalized_profile_image = profile_image.strip() or None

    users[normalized_user_id] = {
        'full_name': (full_name or "").strip(),
        'username': normalized_username,
        'date_of_birth': str(date_of_birth),
        'profile_image': normalized_profile_image,
        'friends': normalized_friends,
    }

    for friend_id in normalized_friends:
        friend_list = users[friend_id].setdefault('friends', [])
        if normalized_user_id not in friend_list:
            friend_list.append(normalized_user_id)

    return {
        'user_id': normalized_user_id,
        **users[normalized_user_id],
    }


def add_friends_to_user(user_id, friend_ids):
    """Adds one or more friends to an existing user profile."""
    if user_id not in users:
        raise ValueError(f'User {user_id} not found.')

    user_friends = users[user_id].setdefault('friends', [])
    added_friends = []

    for friend_id in friend_ids or []:
        if friend_id not in users or friend_id == user_id:
            continue
        if friend_id not in user_friends:
            user_friends.append(friend_id)
            added_friends.append(friend_id)

        reverse_friends = users[friend_id].setdefault('friends', [])
        if user_id not in reverse_friends:
            reverse_friends.append(user_id)

    return added_friends


def get_user_workouts(user_id):
    """Returns a list of workouts for the given user.

    Searches through the workouts table and returns all workouts
    that belong to the given user_id. Handles missing/null fields gracefully.

    Returns a list of dicts with keys:
        workout_id, start_timestamp, end_timestamp,
        start_lat_lng, end_lat_lng, distance, steps, calories_burned
    """
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


def add_user_workout(
    user_id,
    start_timestamp,
    end_timestamp,
    distance,
    steps,
    calories_burned,
    start_lat_lng=None,
    end_lat_lng=None,
):
    """Adds a workout to the in-memory data store used by the app."""
    def normalize_timestamp(value):
        if isinstance(value, datetime):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        return str(value)

    new_workout = {
        'user_id': user_id,
        'workout_id': str(uuid.uuid4()),
        'start_timestamp': normalize_timestamp(start_timestamp),
        'end_timestamp': normalize_timestamp(end_timestamp),
        'start_lat_lng': start_lat_lng,
        'end_lat_lng': end_lat_lng,
        'distance': distance,
        'steps': steps,
        'calories_burned': calories_burned,
    }
    workouts_table.append(new_workout)
    return new_workout


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

    This function currently returns random data.
    """
    if user_id not in users:
        raise ValueError(f'User {user_id} not found.')

    user_data = users[user_id]

    return {
        'full_name': user_data.get('full_name'),
        'username': user_data.get('username'),
        'date_of_birth': user_data.get('date_of_birth'),
        'profile_image': user_data.get('profile_image'),
        'friends': list(user_data.get('friends', []))
    }


def get_user_posts(user_id):
    """Returns a list of a user's posts.

    This function currently returns random data. You will re-write it in Unit 3.
    """
    result = []
    for post in posts_table:
        if post['AuthorId'] == user_id:
            result.append({
                'user_id': user_id,
                'post_id': post.get('post_id'),
                'timestamp': post.get('timestamp'),
                # If content is None, it becomes ""
                'content': post.get('content') or "", 
                # If image is None, it stays None
                'image': post.get('image') or None
            })
    result.sort(key=lambda post: str(post.get('timestamp', '')), reverse=True)
    return result


def add_user_post(user_id, content, image=None, timestamp=None):
    """Adds a post to the in-memory data store used by the app."""
    normalized_timestamp = timestamp or datetime.now()
    if isinstance(normalized_timestamp, datetime):
        normalized_timestamp = normalized_timestamp.strftime('%Y-%m-%d %H:%M:%S')

    new_post = {
        'post_id': str(uuid.uuid4()),
        'AuthorId': user_id,
        'timestamp': normalized_timestamp,
        'content': content or "",
        'image': image,
    }
    posts_table.append(new_post)
    return new_post


def get_genai_advice(user_id):
    """Returns advice from the Vertex AI model based on the user's workout data."""
    query = f"""
        SELECT WorkoutId, StartTimestamp, EndTimestamp, TotalDistance, TotalSteps, CaloriesBurned
        FROM `{project_id}.ISE.Workouts`
        WHERE UserId = @user_id
        ORDER BY StartTimestamp DESC
        LIMIT 3
    """
    try:
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("user_id", "STRING", user_id)]
        )
        rows = list(get_client().query(query, job_config=job_config).result())

        if rows:
            workout_summary = "\n".join([
                f"- Workout on {row['StartTimestamp']}: {row['TotalSteps']} steps, "
                f"{row['TotalDistance']} km, {row['CaloriesBurned']} calories burned"
                for row in rows
            ])
            prompt = f"""You are a friendly fitness coach. Based on the user's recent workouts, 
give them short, personalized, motivational fitness advice (2-3 sentences max). 
Vary your advice each time. Recent workouts:
{workout_summary}"""
        else:
            prompt = """You are a friendly fitness coach. Give a new user short, 
motivational fitness advice to get started (2-3 sentences max). Vary your advice each time."""

        vertexai.init(project=project_id, location="us-central1")
        model = GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        advice_text = response.text
    except Exception:
        advice_text = "Keep showing up for yourself. A steady routine beats a perfect one every time."

    image = None
    if random.random() < 0.4:
        image = 'https://plus.unsplash.com/premium_photo-1669048780129-051d670fa2d1?q=80&w=3870&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'

    return {
        'advice_id': str(uuid.uuid4()),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'content': advice_text,
        'image': image,
    }
