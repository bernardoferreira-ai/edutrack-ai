import unittest
import os
from streamlit.testing.v1 import AppTest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DASHBOARD_PATH = os.path.join(ROOT, "app.py")
SUBJECTS_PATH = os.path.join(ROOT, "pages", "1_📚_Disciplinas.py")
TASKS_PATH = os.path.join(ROOT, "pages", "2_📝_Tarefas.py")


class TestStreamlitApp(unittest.TestCase):
    def test_dashboard_renders(self):
        at = AppTest.from_file(DASHBOARD_PATH).run()
        self.assertEqual(len(at.exception), 0)

        with open(DASHBOARD_PATH, "r", encoding="utf-8") as dashboard_file:
            dashboard_source = dashboard_file.read()

        for label in ("Disciplinas", "Tarefas", "Perfil & PDF", "Notas", "Anotações"):
            self.assertIn(f'label="{label}"', dashboard_source)

    def test_disciplinas_view_renders(self):
        at = AppTest.from_file(SUBJECTS_PATH).run()
        self.assertEqual(len(at.exception), 0)

    def test_tarefas_view_renders(self):
        at = AppTest.from_file(TASKS_PATH).run()
        self.assertEqual(len(at.exception), 0)


if __name__ == "__main__":
    unittest.main()

