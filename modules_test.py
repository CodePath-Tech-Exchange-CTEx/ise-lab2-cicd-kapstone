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

# Write your tests below

class TestDisplayPost(unittest.TestCase):
    """Tests the display_post function."""
   
    def test_post_without_image(self):
        at = AppTest.from_file("app.py")
        at.run()
        at.text_input[0].set_value("testuser")
        at.text_area[0].set_value("testcontent")
        at.button[0].click().run()
        self.assertEqual(at.markdown[0].value, "testuser") 
        self.assertEqual(at.markdown[1].value, "testcontent")
        self.assertIsNotNone(at.caption[0].value)
    def test_no_username(self):
        at = AppTest.from_file("app.py")
        at.run()
        at.text_area[0].set_value("testcontent")
        at.button[0].click().run()
        self.assertEqual(at.warning[0].value,"please enter username")
    def test_content_too_long(self):
        at = AppTest.from_file("app.py")
        at.run()
        at.text_input[0].set_value("testuser")
        at.text_area[0].set_value("a" * 281)
        at.button[0].click().run()
        self.assertEqual(at.warning[0].value,"description must be between 1 and 280 characters")
    def test_no_content(self):
        at = AppTest.from_file("app.py")
        at.run()
        at.text_input[0].set_value("testuser")
        at.button[0].click().run()
        self.assertEqual(at.warning[0].value,"description must be between 1 and 280 characters")


        


class TestDisplayActivitySummary(unittest.TestCase):
    """Tests the display_activity_summary function."""

    def test_summary_with_valid_data(self):
        """Tests summary calculation with a standard list of workouts.""" # Line written by Gemini
        sample_workouts = [
            {'distance': 5.2, 'steps': 7000, 'calories': 300},
            {'distance': 3.1, 'steps': 4000, 'calories': 200}
        ] # Line written by Gemini
        try:
            display_activity_summary(sample_workouts) # Line written by Gemini
            success = True # Line written by Gemini
        except Exception as e:
            success = False # Line written by Gemini
            print(f"Test failed with error: {e}") # Line written by Gemini
        
        self.assertTrue(success, "Function crashed with valid data") # Line written by Gemini

    def test_summary_empty_list(self):
        """Tests the function's ability to handle an empty workout list (edge case).""" # Line written by Gemini
        try:
            display_activity_summary([]) # Line written by Gemini
            success = True # Line written by Gemini
        except Exception:
            success = False # Line written by Gemini
            
        self.assertTrue(success, "Function crashed on an empty list") # Line written by Gemini

    def test_summary_missing_keys(self):
        """Tests handling dictionaries with missing keys using .get() logic.""" # Line written by Gemini
        buggy_workouts = [
            {'distance': 1.0}, # Missing steps and calories
            {'steps': 500}     # Missing distance and calories
        ] # Line written by Gemini
        try:
            display_activity_summary(buggy_workouts) # Line written by Gemini
            success = True # Line written by Gemini
        except Exception:
            success = False # Line written by Gemini
            
        self.assertTrue(success, "Function crashed when workout data was incomplete") # Line written by Gemini


class TestDisplayGenAiAdvice(unittest.TestCase):
    """Tests the display_genai_advice function."""

    def test_foo(self):
        """Tests foo."""
        pass


class TestDisplayRecentWorkouts(unittest.TestCase):
    """Tests the display_recent_workouts function."""

    def test_foo(self):
        """Tests foo."""
        pass


if __name__ == "__main__":
    unittest.main()
