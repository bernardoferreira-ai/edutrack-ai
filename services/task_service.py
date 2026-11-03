import os
import requests
from typing import List, Dict, Optional, Any

def _load_env_file():
    """Simple parser to load variables from .env if present."""
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip('"').strip("'")
                        if k and not os.getenv(k):
                            os.environ[k] = v
        except Exception:
            pass

_load_env_file()

# Initial fallback sample data for standalone / offline mode
INITIAL_TASKS = [
    {
        "id": 1,
        "subject_id": 1,
        "title": "Tarefa 01: Configuração do Ambiente",
        "description": "Configuração inicial do ambiente de desenvolvimento",
        "due_date": "20/02/2026",
        "status": "completed",
        "created_at": "2026-02-15T10:00:00Z"
    },
    {
        "id": 2,
        "subject_id": 1,
        "title": "Tarefa 02: Modelagem das Tabelas",
        "description": "Modelagem dos schemas no Xano",
        "due_date": "05/03/2026",
        "status": "pending",
        "created_at": "2026-02-16T12:00:00Z"
    }
]

class TaskService:
    def __init__(self, api_url: Optional[str] = None, auth_token: Optional[str] = None):
        _load_env_file()
        self.api_url = (
            api_url 
            or os.getenv("XANO_API_URL") 
            or os.getenv("URL_BASE_ALT")
            or os.getenv("XANO_TASKS_URL")
        )
        if self.api_url:
            self.api_url = self.api_url.rstrip("/")
        self.auth_token = auth_token or os.getenv("XANO_AUTH_TOKEN")
        # In-memory fallback repository
        self._fallback_store: List[Dict[str, Any]] = [dict(t) for t in INITIAL_TASKS]
        self._next_id: int = max([t["id"] for t in self._fallback_store], default=0) + 1

    def _headers(self, token: Optional[str] = None) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        active_token = token or self.auth_token
        if active_token:
            headers["Authorization"] = f"Bearer {active_token}"
        return headers

    def list_tasks(
        self,
        token: Optional[str] = None,
        subject_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        active_token = token or self.auth_token
        if self.api_url and active_token:
            try:
                params: Dict[str, Any] = {}
                if subject_id:
                    params["subject_id"] = subject_id
                if status and status != "Todas":
                    # Normalize Portuguese label to backend standard if necessary
                    mapped_status = status.lower()
                    if mapped_status in ["concluída", "concluida"]:
                        mapped_status = "completed"
                    elif mapped_status in ["pendente"]:
                        mapped_status = "pending"
                    params["status"] = mapped_status

                url = f"{self.api_url}/academic_tasks"
                resp = requests.get(url, headers=self._headers(active_token), params=params, timeout=5)
                if resp.status_code == 200:
                    return resp.json()
            except Exception:
                pass  # Fall back to in-memory store

        results = self._fallback_store
        if subject_id:
            results = [t for t in results if t.get("subject_id") == subject_id]
        if status and status != "Todas":
            mapped_status = status.lower()
            if mapped_status in ["concluída", "concluida"]:
                mapped_status = "completed"
            elif mapped_status in ["pendente"]:
                mapped_status = "pending"
            results = [t for t in results if (t.get("status") or "").lower() == mapped_status]
        return [dict(t) for t in results]

    def get_task(self, task_id: int, token: Optional[str] = None) -> Optional[Dict[str, Any]]:
        active_token = token or self.auth_token
        if self.api_url and active_token:
            try:
                url = f"{self.api_url}/academic_tasks/{task_id}"
                resp = requests.get(url, headers=self._headers(active_token), timeout=5)
                if resp.status_code == 200:
                    return resp.json()
            except Exception:
                pass

        for t in self._fallback_store:
            if t.get("id") == task_id:
                return dict(t)
        return None

    def create_task(
        self,
        title: str,
        subject_id: int,
        description: str = "",
        due_date: Optional[str] = None,
        status: str = "pending",
        token: Optional[str] = None
    ) -> Dict[str, Any]:
        cleaned_title = title.strip()
        if not cleaned_title:
            raise ValueError("O título da tarefa é obrigatório.")

        payload: Dict[str, Any] = {
            "title": cleaned_title,
            "subject_id": subject_id,
            "status": status if status in ["pending", "completed"] else "pending"
        }
        if description:
            payload["description"] = description.strip()
        if due_date:
            payload["due_date"] = due_date

        active_token = token or self.auth_token
        if self.api_url and active_token:
            try:
                url = f"{self.api_url}/academic_tasks"
                resp = requests.post(url, headers=self._headers(active_token), json=payload, timeout=5)
                if resp.status_code in (200, 201):
                    return resp.json()
            except Exception:
                pass

        # Fallback creation
        record = {
            "id": self._next_id,
            "created_at": "2026-09-23T12:00:00Z",
            "title": cleaned_title,
            "subject_id": subject_id,
            "description": description.strip() if description else "",
            "due_date": due_date or "20/02/2026",
            "status": status if status in ["pending", "completed"] else "pending"
        }
        self._next_id += 1
        self._fallback_store.append(record)
        return dict(record)

    def update_task(self, task_id: int, token: Optional[str] = None, **fields) -> Optional[Dict[str, Any]]:
        active_token = token or self.auth_token
        if self.api_url and active_token:
            try:
                url = f"{self.api_url}/academic_tasks/{task_id}"
                resp = requests.patch(url, headers=self._headers(active_token), json=fields, timeout=5)
                if resp.status_code == 200:
                    return resp.json()
            except Exception:
                pass

        for t in self._fallback_store:
            if t.get("id") == task_id:
                for k, v in fields.items():
                    if v is not None:
                        t[k] = v.strip() if isinstance(v, str) else v
                return dict(t)
        return None

    def delete_task(self, task_id: int, token: Optional[str] = None) -> bool:
        active_token = token or self.auth_token
        if self.api_url and active_token:
            try:
                url = f"{self.api_url}/academic_tasks/{task_id}"
                resp = requests.delete(url, headers=self._headers(active_token), timeout=5)
                if resp.status_code in (200, 204):
                    return True
            except Exception:
                pass

        for i, t in enumerate(self._fallback_store):
            if t.get("id") == task_id:
                self._fallback_store.pop(i)
                return True
        return False


# Default global instance for use across Streamlit pages
default_task_service = TaskService()

