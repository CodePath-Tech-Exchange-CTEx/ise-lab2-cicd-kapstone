#############################################################################
# modules_test.py
#
# This file contains tests for modules.py.
#
# You will write these tests in Unit 2.
#############################################################################

import unittest
from unittest.mock import patch, MagicMock
from streamlit.testing.v1 import AppTest
from modules import display_post, display_activity_summary, display_genai_advice, display_recent_workouts

# Write your tests below



        


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





if __name__ == "__main__":
    unittest.main()
