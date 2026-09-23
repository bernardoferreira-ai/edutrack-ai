import unittest
from services.subject_service import SubjectService

class TestSubjectService(unittest.TestCase):
    def setUp(self):
        # Create fresh service instance with no API URL (in-memory mode)
        self.service = SubjectService(api_url=None)

    def test_list_subjects(self):
        subjects = self.service.list_subjects()
        self.assertGreaterEqual(len(subjects), 3)

    def test_list_subjects_filter_active(self):
        active_subjects = self.service.list_subjects(status="active")
        for sub in active_subjects:
            self.assertEqual(sub["status"], "active")

    def test_get_subject_success(self):
        sub = self.service.get_subject(1)
        self.assertIsNotNone(sub)
        self.assertEqual(sub["name"], "Innovation Lab")

    def test_get_subject_not_found(self):
        sub = self.service.get_subject(9999)
        self.assertIsNone(sub)

    def test_create_subject_success(self):
        new_sub = self.service.create_subject(
            name="Inteligência Artificial",
            code="IA301",
            professor="Dr. Alan Turing",
            semester="2026.1",
            color="#10B981",
            status="active"
        )
        self.assertEqual(new_sub["name"], "Inteligência Artificial")
        self.assertEqual(new_sub["code"], "IA301")
        self.assertEqual(new_sub["status"], "active")

        # Verify it appears in list
        all_subs = self.service.list_subjects()
        names = [s["name"] for s in all_subs]
        self.assertIn("Inteligência Artificial", names)

    def test_create_subject_missing_name(self):
        with self.assertRaises(ValueError):
            self.service.create_subject(name="   ")

    def test_update_subject_success(self):
        updated = self.service.update_subject(1, professor="Prof. Novo", status="completed")
        self.assertIsNotNone(updated)
        self.assertEqual(updated["professor"], "Prof. Novo")
        self.assertEqual(updated["status"], "completed")

    def test_delete_subject_success(self):
        success = self.service.delete_subject(2)
        self.assertTrue(success)
        self.assertIsNone(self.service.get_subject(2))

    def test_get_active_count(self):
        initial_active = self.service.get_active_count()
        self.service.create_subject(name="Nova Matéria", status="active")
        self.assertEqual(self.service.get_active_count(), initial_active + 1)


if __name__ == "__main__":
    unittest.main()

