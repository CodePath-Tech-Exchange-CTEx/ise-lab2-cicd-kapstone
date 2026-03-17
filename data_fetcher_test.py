#############################################################################
# data_fetcher_test.py
#
# This file contains tests for data_fetcher.py.
#
# You will write these tests in Unit 3.
#############################################################################
import unittest
from data_fetcher import get_user_workouts, get_user_sensor_data


class TestDataFetcher(unittest.TestCase):

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


if __name__ == "__main__":
    unittest.main()