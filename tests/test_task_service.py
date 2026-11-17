import unittest

from services.task_service import TaskService


class TestTaskService(unittest.TestCase):
    def setUp(self):
        self.service = TaskService(api_url="https://example.com", auth_token="token")

    def test_create_task_omits_empty_description_from_payload(self):
        captured = {}

        class MockResponse:
            status_code = 201
            text = "{}"

            def json(self):
                return {"id": 1, "title": "Nova tarefa", "subject_id": 1, "status": "pending"}

        def fake_dispatch(method, endpoint_suffix, token=None, **kwargs):
            captured["method"] = method
            captured["endpoint_suffix"] = endpoint_suffix
            captured["json"] = kwargs.get("json")
            return MockResponse()

        self.service._dispatch_request = fake_dispatch

        created = self.service.create_task(
            title="Nova tarefa",
            subject_id=1,
            description="   ",
            token="token",
        )

        self.assertEqual(created["title"], "Nova tarefa")
        self.assertNotIn("description", captured["json"])
        self.assertEqual(captured["json"]["status"], "pending")

    def test_create_task_omits_none_description_from_payload(self):
        captured = {}

        class MockResponse:
            status_code = 201
            text = "{}"

            def json(self):
                return {"id": 1, "title": "Nova tarefa", "subject_id": 1, "status": "pending"}

        def fake_dispatch(method, endpoint_suffix, token=None, **kwargs):
            captured["json"] = kwargs.get("json")
            return MockResponse()

        self.service._dispatch_request = fake_dispatch

        self.service.create_task(
            title="Nova tarefa",
            subject_id=1,
            description=None,
            token="token",
        )

        self.assertNotIn("description", captured["json"])

    def test_update_task_sends_only_status(self):
        captured = {}

        class MockResponse:
            status_code = 200
            text = "{}"

            def json(self):
                return {"id": 1, "status": "completed"}

        def fake_dispatch(method, endpoint_suffix, token=None, **kwargs):
            captured["method"] = method
            captured["endpoint_suffix"] = endpoint_suffix
            captured["json"] = kwargs.get("json")
            return MockResponse()

        self.service._dispatch_request = fake_dispatch

        updated = self.service.update_task(1, token="token", status="completed")
        self.assertEqual(captured["method"], "PATCH")
        self.assertEqual(captured["endpoint_suffix"], "academic_tasks/1")
        self.assertEqual(captured["json"], {"status": "completed"})
        self.assertEqual(updated["status"], "completed")

    def test_delete_task_success(self):
        captured = {}

        class MockResponse:
            status_code = 200
            text = "null"

            def json(self):
                return None

        def fake_dispatch(method, endpoint_suffix, token=None, **kwargs):
            captured["method"] = method
            captured["endpoint_suffix"] = endpoint_suffix
            return MockResponse()

        self.service._dispatch_request = fake_dispatch

        res = self.service.delete_task(1, token="token")
        self.assertTrue(res)
        self.assertEqual(captured["method"], "DELETE")
        self.assertEqual(captured["endpoint_suffix"], "academic_tasks/1")


if __name__ == "__main__":
    unittest.main()
