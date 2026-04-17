#############################################################################
# data_fetcher_test.py
#
# This file contains tests for data_fetcher.py.
#
# You will write these tests in Unit 3.
#############################################################################
import unittest
from data_fetcher import add_user_post, get_user_workouts, get_user_sensor_data, get_user_profile, get_user_posts, posts_table


class TestDataFetcher(unittest.TestCase):

    def setUp(self):
        self.original_posts = [post.copy() for post in posts_table]

    def tearDown(self):
        posts_table[:] = self.original_posts

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


if __name__ == "__main__":
    unittest.main()
