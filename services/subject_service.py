import os
import requests
from typing import List, Dict, Optional, Any

# Initial fallback sample data for standalone / offline mode
INITIAL_SUBJECTS = [
    {
        "id": 1,
        "name": "Innovation Lab",
        "code": "ILAB101",
        "professor": "Prof. Coordenador",
        "semester": "2026.1",
        "color": "#4F46E5",
        "status": "active",
        "created_at": "2026-02-15T10:00:00Z"
    },
    {
        "id": 2,
        "name": "Engenharia de Software",
        "code": "ES201",
        "professor": "Dra. Ana Silva",
        "semester": "2026.1",
        "color": "#059669",
        "status": "active",
        "created_at": "2026-02-16T14:30:00Z"
    },
    {
        "id": 3,
        "name": "Cálculo Diferencial e Integral",
        "code": "MAT101",
        "professor": "Dr. Carlos Mendes",
        "semester": "2025.2",
        "color": "#6B7280",
        "status": "completed",
        "created_at": "2025-08-10T09:00:00Z"
    }
]

class SubjectService:
    def __init__(self, api_url: Optional[str] = None, auth_token: Optional[str] = None):
        self.api_url = (
            api_url 
            or os.getenv("XANO_API_URL") 
            or os.getenv("XANO_SUBJECTS_URL")
        )
        self.auth_token = auth_token or os.getenv("XANO_AUTH_TOKEN")
        # In-memory fallback repository
        self._fallback_store: List[Dict[str, Any]] = [dict(s) for s in INITIAL_SUBJECTS]
        self._next_id: int = max([s["id"] for s in self._fallback_store], default=0) + 1

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        return headers

    def list_subjects(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        if self.api_url:
            try:
                params = {"status": status} if status else {}
                url = f"{self.api_url.rstrip('/')}/subjects"
                resp = requests.get(url, headers=self._headers(), params=params, timeout=3)
                if resp.status_code == 200:
                    return resp.json()
            except Exception:
                pass  # Fall back to in-memory store

        results = self._fallback_store
        if status:
            results = [s for s in results if s.get("status") == status]
        return [dict(s) for s in results]

    def get_subject(self, subject_id: int) -> Optional[Dict[str, Any]]:
        if self.api_url:
            try:
                url = f"{self.api_url.rstrip('/')}/subjects/{subject_id}"
                resp = requests.get(url, headers=self._headers(), timeout=3)
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
        code: str = "",
        professor: str = "",
        semester: str = "",
        color: str = "",
        status: str = "active"
    ) -> Dict[str, Any]:
        cleaned_name = name.strip()
        if not cleaned_name:
            raise ValueError("O nome da disciplina é obrigatório.")

        payload = {
            "name": cleaned_name,
            "code": code.strip() if code else "",
            "professor": professor.strip() if professor else "",
            "semester": semester.strip() if semester else "",
            "color": color.strip() if color else "#3B82F6",
            "status": status if status in ["active", "completed", "archived"] else "active",
        }

        if self.api_url:
            try:
                url = f"{self.api_url.rstrip('/')}/subjects"
                resp = requests.post(url, headers=self._headers(), json=payload, timeout=3)
                if resp.status_code in (200, 201):
                    return resp.json()
            except Exception:
                pass

        # Fallback creation
        record = {
            "id": self._next_id,
            "created_at": "2026-09-23T12:00:00Z",
            **payload
        }
        self._next_id += 1
        self._fallback_store.append(record)
        return dict(record)

    def update_subject(self, subject_id: int, **fields) -> Optional[Dict[str, Any]]:
        if "name" in fields and not fields["name"].strip():
            raise ValueError("O nome da disciplina não pode ser vazio.")

        if self.api_url:
            try:
                url = f"{self.api_url.rstrip('/')}/subjects/{subject_id}"
                resp = requests.patch(url, headers=self._headers(), json=fields, timeout=3)
                if resp.status_code == 200:
                    return resp.json()
            except Exception:
                pass

        for s in self._fallback_store:
            if s.get("id") == subject_id:
                for k, v in fields.items():
                    if v is not None:
                        s[k] = v.strip() if isinstance(v, str) else v
                return dict(s)
        return None

    def delete_subject(self, subject_id: int) -> bool:
        if self.api_url:
            try:
                url = f"{self.api_url.rstrip('/')}/subjects/{subject_id}"
                resp = requests.delete(url, headers=self._headers(), timeout=3)
                if resp.status_code in (200, 204):
                    return True
            except Exception:
                pass

        for i, s in enumerate(self._fallback_store):
            if s.get("id") == subject_id:
                self._fallback_store.pop(i)
                return True
        return False

    def get_active_count(self) -> int:
        subjects = self.list_subjects(status="active")
        return len(subjects)


# Default global instance for use across Streamlit pages
default_subject_service = SubjectService()

