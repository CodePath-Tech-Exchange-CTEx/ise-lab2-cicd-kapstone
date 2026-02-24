#############################################################################
# modules_test.py
#
# This file contains tests for modules.py.
#
# You will write these tests in Unit 2.
#############################################################################

import unittest
from streamlit.testing.v1 import AppTest
from modules import display_post, display_activity_summary, display_genai_advice, display_recent_workouts


class TestDisplayPost(unittest.TestCase):
    """Tests the display_post function."""

    def test_post_without_image(self):
        """Tests that a post renders username and content correctly."""
        at = AppTest.from_file("app.py")
        at.run()
        at.text_input[1].set_value("testuser")
        at.text_area[0].set_value("testcontent")
        at.button[0].click().run()
        self.assertEqual(at.markdown[0].value, "testuser")
        self.assertEqual(at.markdown[1].value, "testcontent")
        self.assertIsNotNone(at.caption[0].value)

    def test_no_username(self):
        """Tests that a warning is shown when no username is entered."""
        at = AppTest.from_file("app.py")
        at.run()
        at.text_area[0].set_value("testcontent")
        at.button[0].click().run()
        self.assertEqual(at.warning[0].value, "please enter username")

    def test_content_too_long(self):
        """Tests that a warning is shown when content exceeds 280 characters."""
        at = AppTest.from_file("app.py")
        at.run()
        at.text_input[1].set_value("testuser")
        at.text_area[0].set_value("a" * 281)
        at.button[0].click().run()
        self.assertEqual(at.warning[0].value, "description must be between 1 and 280 characters")

    def test_no_content(self):
        """Tests that a warning is shown when no content is entered."""
        at = AppTest.from_file("app.py")
        at.run()
        at.text_input[1].set_value("testuser")
        at.button[0].click().run()
        self.assertEqual(at.warning[0].value, "description must be between 1 and 280 characters")


class TestDisplayActivitySummary(unittest.TestCase):
    """Tests the display_activity_summary function."""

    def test_summary_with_valid_data(self):
        """Tests summary calculation with a standard list of workouts."""
        sample_workouts = [
            {'distance': 5.2, 'steps': 7000, 'calories': 300},
            {'distance': 3.1, 'steps': 4000, 'calories': 200}
        ]
        try:
            display_activity_summary(sample_workouts)
            success = True
        except Exception as e:
            success = False
            print(f"Test failed with error: {e}")
        self.assertTrue(success, "Function crashed with valid data")

    def test_summary_empty_list(self):
        """Tests the function's ability to handle an empty workout list."""
        try:
            display_activity_summary([])
            success = True
        except Exception:
            success = False
        self.assertTrue(success, "Function crashed on an empty list")

    def test_summary_missing_keys(self):
        """Tests handling dictionaries with missing keys."""
        buggy_workouts = [
            {'distance': 1.0},
            {'steps': 500}
        ]
        try:
            display_activity_summary(buggy_workouts)
            success = True
        except Exception:
            success = False
        self.assertTrue(success, "Function crashed when workout data was incomplete")


class TestDisplayGenAiAdvice(unittest.TestCase):
    """Tests the display_genai_advice function."""

    def test_function_signature(self):
        """Tests that display_genai_advice accepts the correct parameters."""
        import inspect
        sig = inspect.signature(display_genai_advice)
        params = list(sig.parameters.keys())
        self.assertIn("timestamp", params)
        self.assertIn("content", params)
        self.assertIn("image", params)

    def test_returns_none(self):
        """Tests that display_genai_advice returns None."""
        import inspect
        sig = inspect.signature(display_genai_advice)
        ret = sig.return_annotation
        self.assertIn(ret, [inspect.Parameter.empty, None])


class TestDisplayRecentWorkouts(unittest.TestCase):
    """Tests the display_recent_workouts function."""

    def test_display_recent_workouts_runs(self):
        """Tests if the function processes a list of workouts without crashing."""
        sample_data = [
            {'distance': 3.5, 'steps': 4500, 'calories': 250},
            {'distance': 1.2, 'steps': 1500, 'calories': 80}
        ]
        try:
            display_recent_workouts(sample_data)
            success = True
        except Exception:
            success = False
        self.assertTrue(success, "Function failed to process workout list")


if __name__ == "__main__":
    unittest.main()
    