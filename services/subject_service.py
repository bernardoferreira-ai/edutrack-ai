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
INITIAL_SUBJECTS = [
    {
        "id": 1,
        "name": "Innovation Lab",
        "code": "ILAB101",
        "teacher": "Prof. Coordenador",
        "professor": "Prof. Coordenador",
        "hours": 60,
        "semester": "2026.1",
        "dia_semana": "Seg",
        "color": "#4F46E5",
        "status": "active",
        "created_at": "2026-02-15T10:00:00Z"
    },
    {
        "id": 2,
        "name": "Engenharia de Software",
        "code": "ES201",
        "teacher": "Dra. Ana Silva",
        "professor": "Dra. Ana Silva",
        "hours": 80,
        "semester": "2026.1",
        "dia_semana": "Ter",
        "color": "#059669",
        "status": "active",
        "created_at": "2026-02-16T14:30:00Z"
    },
    {
        "id": 3,
        "name": "Cálculo Diferencial e Integral",
        "code": "MAT101",
        "teacher": "Dr. Carlos Mendes",
        "professor": "Dr. Carlos Mendes",
        "hours": 80,
        "semester": "2025.2",
        "dia_semana": "Qua",
        "color": "#6B7280",
        "status": "completed",
        "created_at": "2025-08-10T09:00:00Z"
    }
]

class SubjectService:
    def __init__(self, api_url: Optional[str] = None, auth_token: Optional[str] = None):
        _load_env_file()
        self.api_url = (
            api_url 
            or os.getenv("XANO_API_URL") 
            or os.getenv("URL_BASE_ALT")
            or os.getenv("XANO_SUBJECTS_URL")
        )
        if self.api_url:
            self.api_url = self.api_url.rstrip("/")
        self.auth_token = auth_token or os.getenv("XANO_AUTH_TOKEN")
        # In-memory fallback repository
        self._fallback_store: List[Dict[str, Any]] = [dict(s) for s in INITIAL_SUBJECTS]
        self._next_id: int = max([s["id"] for s in self._fallback_store], default=0) + 1

    def _headers(self, token: Optional[str] = None) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        active_token = token or self.auth_token
        if active_token:
            headers["Authorization"] = f"Bearer {active_token}"
        return headers

    def list_subjects(self, token: Optional[str] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
        active_token = token or self.auth_token
        if self.api_url and active_token:
            try:
                params = {"status": status} if status else {}
                url = f"{self.api_url}/subjects"
                resp = requests.get(url, headers=self._headers(active_token), params=params, timeout=5)
                if resp.status_code == 200:
                    return resp.json()
            except Exception:
                pass  # Fall back to in-memory store

        results = self._fallback_store
        if status:
            results = [s for s in results if s.get("status") == status]
        return [dict(s) for s in results]

    def get_subject(self, subject_id: int, token: Optional[str] = None) -> Optional[Dict[str, Any]]:
        active_token = token or self.auth_token
        if self.api_url and active_token:
            try:
                url = f"{self.api_url}/subjects/{subject_id}"
                resp = requests.get(url, headers=self._headers(active_token), timeout=5)
                if resp.status_code == 200:
                    return resp.json()
            except Exception:
                pass

        for s in self._fallback_store:
            if s.get("id") == subject_id:
                return dict(s)
        return None

    def create_subject(
        self,
        name: str,
        teacher: str = "",
        hours: Optional[int] = None,
        code: str = "",
        professor: str = "",
        semester: str = "",
        color: str = "",
        status: str = "active",
        dia_semana: str = "Seg",
        token: Optional[str] = None
    ) -> Dict[str, Any]:
        cleaned_name = name.strip()
        if not cleaned_name:
            raise ValueError("O nome da disciplina é obrigatório.")

        resolved_teacher = (teacher or professor).strip()
        payload = {
            "name": cleaned_name,
            "teacher": resolved_teacher,
        }
        if hours is not None:
            payload["hours"] = hours

        active_token = token or self.auth_token
        if self.api_url and active_token:
            try:
                url = f"{self.api_url}/subjects"
                resp = requests.post(url, headers=self._headers(active_token), json=payload, timeout=5)
                if resp.status_code in (200, 201):
                    return resp.json()
            except Exception:
                pass

        # Fallback creation
        record = {
            "id": self._next_id,
            "created_at": "2026-09-23T12:00:00Z",
            "name": cleaned_name,
            "teacher": resolved_teacher,
            "professor": resolved_teacher,
            "hours": hours or 60,
            "code": code.strip() if code else "",
            "semester": semester.strip() if semester else "2026.1",
            "dia_semana": dia_semana,
            "color": color.strip() if color else "#3B82F6",
            "status": status if status in ["active", "completed", "archived"] else "active",
        }
        self._next_id += 1
        self._fallback_store.append(record)
        return dict(record)

    def update_subject(self, subject_id: int, token: Optional[str] = None, **fields) -> Optional[Dict[str, Any]]:
        if "name" in fields and fields["name"] is not None and not str(fields["name"]).strip():
            raise ValueError("O nome da disciplina não pode ser vazio.")

        active_token = token or self.auth_token
        if self.api_url and active_token:
            try:
                url = f"{self.api_url}/subjects/{subject_id}"
                resp = requests.patch(url, headers=self._headers(active_token), json=fields, timeout=5)
                if resp.status_code == 200:
                    return resp.json()
            except Exception:
                pass

        for s in self._fallback_store:
            if s.get("id") == subject_id:
                for k, v in fields.items():
                    if v is not None:
                        s[k] = v.strip() if isinstance(v, str) else v
                        if k == "teacher":
                            s["professor"] = s[k]
                        elif k == "professor":
                            s["teacher"] = s[k]
                return dict(s)
        return None

    def delete_subject(self, subject_id: int, token: Optional[str] = None) -> bool:
        active_token = token or self.auth_token
        if self.api_url and active_token:
            try:
                url = f"{self.api_url}/subjects/{subject_id}"
                resp = requests.delete(url, headers=self._headers(active_token), timeout=5)
                if resp.status_code in (200, 204):
                    return True
            except Exception:
                pass

        for i, s in enumerate(self._fallback_store):
            if s.get("id") == subject_id:
                self._fallback_store.pop(i)
                return True
        return False

    def get_active_count(self, token: Optional[str] = None) -> int:
        subjects = self.list_subjects(token=token, status="active")
        return len(subjects)


# Default global instance for use across Streamlit pages
default_subject_service = SubjectService()
