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
        self.assertEqual(at.write[0].value, "testuser") 
        self.assertEqual(at.write[1].value, "testcontent")
        self.assertIsNotNone(at.caption[0].value)
        self.assertEqual(len(at.image), 0)
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

    def test_foo(self):
        """Tests foo."""
        pass


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
