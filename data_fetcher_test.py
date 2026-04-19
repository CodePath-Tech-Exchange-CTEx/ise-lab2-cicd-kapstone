#############################################################################
# data_fetcher_test.py
#
# This file contains tests for data_fetcher.py.
#
# You will write these tests in Unit 3.
#############################################################################
import unittest
from copy import deepcopy
from datetime import datetime

from data_fetcher import (
    add_friends_to_user,
    add_user_profile,
    add_user_post,
    add_user_workout,
    get_user_posts,
    get_user_profile,
    get_user_sensor_data,
    get_user_workouts,
    posts_table,
    users,
    workouts_table,
)


class TestDataFetcher(unittest.TestCase):

    def setUp(self):
        self.original_users = deepcopy(users)
        self.original_posts = [post.copy() for post in posts_table]
        self.original_workouts = [workout.copy() for workout in workouts_table]

    def tearDown(self):
        users.clear()
        users.update(deepcopy(self.original_users))
        posts_table[:] = self.original_posts
        workouts_table[:] = self.original_workouts

    def test_get_user_workouts_returns_correct_keys(self):
        workouts = get_user_workouts('user1')
        self.assertIsInstance(workouts, list)
        self.assertGreater(len(workouts), 0)

        expected_keys = {
            'workout_id',
            'start_timestamp',
            'end_timestamp',
            'start_lat_lng',
            'end_lat_lng',
            'distance',
            'steps',
            'calories_burned',
        }

        self.assertEqual(set(workouts[0].keys()), expected_keys)

    def test_get_user_workouts_valid_user_with_data(self):
        workouts = get_user_workouts('user1')
        self.assertEqual(len(workouts), 2)
        self.assertEqual(workouts[0]['workout_id'], 'workout1')

    def test_get_user_workouts_user_with_no_workouts(self):
        workouts = get_user_workouts('user999')
        self.assertEqual(workouts, [])

    def test_get_user_workouts_handles_missing_fields(self):
        workouts = get_user_workouts('user1')
        self.assertIsNone(workouts[1]['distance'])

    def test_get_user_sensor_data_returns_correct_keys(self):
        sensor_data = get_user_sensor_data('user1', 'workout1')
        self.assertIsInstance(sensor_data, list)
        self.assertGreater(len(sensor_data), 0)

        expected_keys = {
            'sensor_type',
            'timestamp',
            'data',
            'units',
        }

        self.assertEqual(set(sensor_data[0].keys()), expected_keys)

    def test_get_user_sensor_data_valid_workout_with_data(self):
        sensor_data = get_user_sensor_data('user1', 'workout1')
        self.assertEqual(len(sensor_data), 2)
        self.assertEqual(sensor_data[0]['sensor_type'], 'heart_rate')

    def test_get_user_sensor_data_workout_with_no_sensor_data(self):
        sensor_data = get_user_sensor_data('user1', 'workout999')
        self.assertEqual(sensor_data, [])

    def test_get_user_sensor_data_handles_missing_fields(self):
        sensor_data = get_user_sensor_data('user1', 'workout2')  # workout2 has None data
        self.assertIsInstance(sensor_data, list)
        self.assertGreater(len(sensor_data), 0)
        self.assertIsNone(sensor_data[0]['data'])  # temperature reading is None
        
    #User profile 
    def test_get_user_profile_returns_correct_keys(self):
        # Uses the real 'users' data from data_fetcher.py
        profile = get_user_profile('user1')
        expected_keys = {
            'full_name',
            'username',
            'date_of_birth',
            'profile_image',
            'friends',
        }
        self.assertEqual(set(profile.keys()), expected_keys)

    def test_get_user_profile_valid_user_with_data(self):
        profile = get_user_profile('user1')
        self.assertEqual(len(profile['friends']), 3)
        self.assertIn('user2', profile['friends'])

    def test_get_user_profile_no_friends(self):
        profile = get_user_profile('user2') 
        self.assertIsInstance(profile['friends'], list)

    def test_add_user_profile_is_returned_by_get_user_profile(self):
        created = add_user_profile(
            'user5',
            'Taylor Smith',
            'taylorsmith',
            '1995-05-15',
            'https://example.com/taylor.jpg',
            friends=['user1', 'user2'],
        )
        profile = get_user_profile('user5')
        self.assertEqual(created['user_id'], 'user5')
        self.assertEqual(profile['full_name'], 'Taylor Smith')
        self.assertEqual(profile['username'], 'taylorsmith')
        self.assertEqual(profile['date_of_birth'], '1995-05-15')
        self.assertEqual(profile['profile_image'], 'https://example.com/taylor.jpg')
        self.assertEqual(profile['friends'], ['user1', 'user2'])

    def test_add_user_profile_adds_reverse_friend_link(self):
        add_user_profile(
            'user5',
            'Taylor Smith',
            'taylorsmith',
            '1995-05-15',
            'https://example.com/taylor.jpg',
            friends=['user2'],
        )
        profile = get_user_profile('user2')
        self.assertIn('user5', profile['friends'])

    def test_add_friends_to_user_adds_two_way_friendship(self):
        add_user_profile(
            'user5',
            'Taylor Smith',
            'taylorsmith',
            '1995-05-15',
            'https://example.com/taylor.jpg',
        )
        added = add_friends_to_user('user5', ['user1'])
        user5_profile = get_user_profile('user5')
        user1_profile = get_user_profile('user1')
        self.assertEqual(added, ['user1'])
        self.assertIn('user1', user5_profile['friends'])
        self.assertIn('user5', user1_profile['friends'])
        
    #User Posts 

    def test_get_user_posts_returns_correct_keys(self):
        posts = get_user_posts('user1')
        self.assertIsInstance(posts, list)
        if len(posts) > 0:
            expected_keys = {
                'user_id',
                'post_id',
                'timestamp',
                'content',
                'image',
            }
            self.assertEqual(set(posts[0].keys()), expected_keys)

    def test_get_user_posts_valid_user_with_data(self):
        posts = get_user_posts('user1')
        self.assertEqual(len(posts), 2)
        self.assertEqual(posts[0]['post_id'], 'post2')

    def test_get_user_posts_user_with_no_posts(self):
        posts = get_user_posts('user4') 
        self.assertEqual(posts, [])

    def test_get_user_posts_handles_missing_fields(self):
        posts = get_user_posts('user1')
        post1 = next(p for p in posts if p['post_id'] == 'post1')
        self.assertEqual(post1['content'], "")

    def test_add_user_post_is_returned_in_latest_posts(self):
        created = add_user_post('user4', 'Testing a new community post.')
        posts = get_user_posts('user4')
        self.assertGreaterEqual(len(posts), 1)
        self.assertEqual(posts[0]['post_id'], created['post_id'])
        self.assertEqual(posts[0]['content'], 'Testing a new community post.')

    def test_add_user_workout_is_returned_in_latest_workouts(self):
        created = add_user_workout(
            'user4',
            start_timestamp=datetime(2026, 4, 19, 9, 0, 0),
            end_timestamp=datetime(2026, 4, 19, 10, 0, 0),
            distance=3.2,
            steps=5400,
            calories_burned=320,
        )
        workouts = get_user_workouts('user4')
        self.assertEqual(len(workouts), 1)
        self.assertEqual(workouts[0]['workout_id'], created['workout_id'])
        self.assertEqual(workouts[0]['distance'], 3.2)
        self.assertEqual(workouts[0]['steps'], 5400)
        self.assertEqual(workouts[0]['calories_burned'], 320)


if __name__ == "__main__":
    unittest.main()
