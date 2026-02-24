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
        at.text_input[1].set_value("testuser")
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
        at.text_input[1].set_value("testuser")
        at.text_area[0].set_value("a" * 281)
        at.button[0].click().run()
        self.assertEqual(at.warning[0].value,"description must be between 1 and 280 characters")
    def test_no_content(self):
        at = AppTest.from_file("app.py")
        at.run()
        at.text_input[1].set_value("testuser")
        at.button[0].click().run()
        self.assertEqual(at.warning[0].value,"description must be between 1 and 280 characters")


        


class TestDisplayActivitySummary(unittest.TestCase):
    """Tests the display_activity_summary function."""

    def test_mockup_exact_data(self):
        mockup_data = [ # Line written by Gemini
            { # Workout 1
                "start_time": "7:30 AM", "end_time": "8:10 AM", 
                # Line written by Gemini
                "distance": 2.1, "steps": 3200, "calories": 260, 
                # Line written by Gemini
                "start_coords": (0,0), "end_coords": (0,0)
                 # Line written by Gemini
            }, 
            { # Workout 2
                "start_time": "1:00 PM", "end_time": "1:35 PM", 
                # Line written by Gemini
                "distance": 1.9, "steps": 2750, "calories": 210, 
                # Line written by Gemini
                "start_coords": (0,0), "end_coords": (0,0) 
                # Line written by Gemini
            },
            { # Workout 3
                "start_time": "6:45 PM", "end_time": "7:25 PM", 
                # Line written by Gemini
                "distance": 2.7, "steps": 3910, "calories": 270, 
                # Line written by Gemini
                "start_coords": (0,0), "end_coords": (0,0) 
                # Line written by Gemini
            } 
        ] 
        result = display_activity_summary(mockup_data) 
        # Line written by Gemini
        self.assertIsNone(result, "The function must return None.")
         # Line written by Gemini

        result = display_activity_summary([]) # Line written by Gemini
        self.assertIsNone(result) # Line written by Gemini

class TestDisplayGenAiAdvice(unittest.TestCase):

    def test_function_signature(self):
        import inspect
        sig = inspect.signature(display_genai_advice)
        params = list(sig.parameters.keys())
        self.assertIn("timestamp", params)
        self.assertIn("content", params)
        self.assertIn("image", params)

    def test_returns_none(self):
        import inspect
        sig = inspect.signature(display_genai_advice)
        ret = sig.return_annotation
        self.assertIn(ret, [inspect.Parameter.empty, None])


class TestDisplayRecentWorkouts(unittest.TestCase):
    """Tests for display_recent_workouts()"""

    @patch("modules.st")
    def test_empty_list_shows_info(self, mock_st):
        """Empty list should show an info message and stop early."""
        from modules import display_recent_workouts
        display_recent_workouts([])
        mock_st.info.assert_called_once()  # checks st.info() was called

    @patch("modules.create_component")
    def test_single_workout_creates_component(self, mock_create):
        """A single workout should call create_component once."""
        from modules import display_recent_workouts
        workouts = [
            {'start_time': '9am', 'end_time': '10am',
             'distance': 3, 'steps': 4000, 'calories': 250}
        ]
        display_recent_workouts(workouts)
        mock_create.assert_called_once()  # checks create_component was called

    @patch("modules.create_component")
    def test_workout_data_appears_in_html(self, mock_create):
        """The distance value should appear somewhere in the generated HTML."""
        from modules import display_recent_workouts
        workouts = [
            {'distance': 5, 'steps': 6000, 'calories': 300}
        ]
        display_recent_workouts(workouts)

        # Get what was passed to create_component
        passed_data = mock_create.call_args[0][0]  # first argument = the data dict
        self.assertIn('WORKOUT_CARDS', passed_data)
        self.assertIn('5', passed_data['WORKOUT_CARDS'])  # distance shows up

    @patch("modules.create_component")
    def test_missing_fields_default_to_zero(self, mock_create):
        """Workouts with missing keys should not crash."""
        from modules import display_recent_workouts
        display_recent_workouts([{}])  # completely empty workout dict
        mock_create.assert_called_once()


if __name__ == "__main__":
    unittest.main()
