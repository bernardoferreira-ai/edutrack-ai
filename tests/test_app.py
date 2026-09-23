import unittest
import os
from streamlit.testing.v1 import AppTest

APP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app.py"))

class TestStreamlitApp(unittest.TestCase):
    def test_dashboard_renders(self):
        at = AppTest.from_file(APP_PATH).run()
        self.assertEqual(len(at.exception), 0)
        self.assertTrue(any("EduTrack AI" in title.value for title in at.title))
        self.assertGreaterEqual(len(at.metric), 3)

    def test_disciplinas_view_renders(self):
        at = AppTest.from_file(APP_PATH).run()
        at.sidebar.radio[0].set_value("Disciplinas").run()
        self.assertEqual(len(at.exception), 0)
        self.assertTrue(any("Minhas Disciplinas" in h.value for h in at.header))

    def test_tarefas_view_renders(self):
        at = AppTest.from_file(APP_PATH).run()
        at.sidebar.radio[0].set_value("Tarefas").run()
        self.assertEqual(len(at.exception), 0)

if __name__ == "__main__":
    unittest.main()

