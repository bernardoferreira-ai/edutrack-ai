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

# Canonical defined in api/subjects/subjects.xs
SUBJECTS_CANONICAL = "yhqYbIq3"

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
            or os.getenv("XANO_SUBJECTS_URL")
            or os.getenv("XANO_API_URL") 
            or os.getenv("URL_BASE_ALT")
        )
        if self.api_url:
            self.api_url = self.api_url.rstrip("/")
        self.auth_token = auth_token or os.getenv("XANO_AUTH_TOKEN")
        self._fallback_store: List[Dict[str, Any]] = [dict(s) for s in INITIAL_SUBJECTS]
        self._next_id: int = max([s["id"] for s in self._fallback_store], default=0) + 1
        self._working_base_url: Optional[str] = None

    def _headers(self, token: Optional[str] = None) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        active_token = token or self.auth_token
        if active_token:
            headers["Authorization"] = f"Bearer {active_token}"
        return headers

    def _get_candidate_urls(self, endpoint_suffix: str) -> List[str]:
        """Gera URLs candidatas para o endpoint (canonical do grupo e fallback de URL_BASE_ALT)."""
        suffix = endpoint_suffix.lstrip("/")
        if self._working_base_url:
            return [f"{self._working_base_url}/{suffix}"]

        candidates = []
        base = self.api_url or "https://x8ki-letl-twmt.n7.xano.io/api:dyXfRo9-"
        
        if "/api:" in base:
            host = base.split("/api:")[0]
            # 1. URL com o canonical do grupo Subjects (yhqYbIq3)
            candidates.append(f"{host}/api:{SUBJECTS_CANONICAL}/{suffix}")
            # 2. URL com o grupo de URL_BASE_ALT
            candidates.append(f"{base}/{suffix}")
        else:
            candidates.append(f"{base}/{suffix}")

        return candidates

    def _dispatch_request(self, method: str, endpoint_suffix: str, token: Optional[str] = None, **kwargs) -> requests.Response:
        """Executa requisição tentando as URLs candidatas do Xano."""
        active_token = token or self.auth_token
        headers = self._headers(active_token)
        candidates = self._get_candidate_urls(endpoint_suffix)
        last_resp = None
        last_exc = None

        for url in candidates:
            try:
                resp = requests.request(method, url, headers=headers, timeout=6, **kwargs)
                if resp.status_code == 404 and len(candidates) > 1:
                    # Tenta o próximo candidato se 404
                    last_resp = resp
                    continue
                # Se respondeu (2xx, 4xx, 5xx), grava base funcional
                if resp.status_code < 500:
                    base_used = url.rsplit(f"/{endpoint_suffix.lstrip('/')}", 1)[0]
                    self._working_base_url = base_used
                return resp
            except Exception as e:
                last_exc = e

        if last_resp is not None:
            return last_resp
        if last_exc:
            raise last_exc
        raise RuntimeError("Não foi possível conectar ao servidor Xano.")

    def list_subjects(self, token: Optional[str] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
        active_token = token or self.auth_token
        if active_token:
            try:
                params = {"status": status} if status else {}
                resp = self._dispatch_request("GET", "subjects", token=active_token, params=params)
                if resp.status_code == 200:
                    data = resp.json()
                    if isinstance(data, list):
                        return data
                elif resp.status_code == 401:
                    pass  # Token inválido ou expirado, usa fallback
            except Exception:
                pass  # Fallback quando offline ou sem rede

        results = self._fallback_store
        if status:
            results = [s for s in results if s.get("status") == status]
        return [dict(s) for s in results]

    def get_subject(self, subject_id: int, token: Optional[str] = None) -> Optional[Dict[str, Any]]:
        active_token = token or self.auth_token
        if active_token:
            try:
                resp = self._dispatch_request("GET", f"subjects/{subject_id}", token=active_token)
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
        dia_semana: str = "Seg",
        token: Optional[str] = None
    ) -> Dict[str, Any]:
        cleaned_name = name.strip()
        if not cleaned_name:
            raise ValueError("O nome da disciplina é obrigatório.")

        resolved_teacher = teacher.strip()
        # Xano exige 'hours'; se não informado, define valor padrão de 60 horas
        resolved_hours = int(hours) if hours is not None else 60
        payload: Dict[str, Any] = {
            "name": cleaned_name,
            "teacher": resolved_teacher,
            "hours": resolved_hours,
        }

        active_token = token or self.auth_token
        if active_token:
            resp = self._dispatch_request("POST", "subjects", token=active_token, json=payload)
            if resp.status_code in (200, 201):
                record = resp.json()
                if "dia_semana" not in record:
                    record["dia_semana"] = dia_semana
                return record
            else:
                try:
                    err_json = resp.json()
                    err_msg = err_json.get("message") or str(err_json)
                except Exception:
                    err_msg = resp.text
                raise RuntimeError(f"Erro do Xano ({resp.status_code}): {err_msg}")

        # Fallback creation para uso offline
        record = {
            "id": self._next_id,
            "created_at": "2026-09-23T12:00:00Z",
            "name": cleaned_name,
            "teacher": resolved_teacher,
            "professor": resolved_teacher,
            "hours": hours or 60,
            "dia_semana": dia_semana,
            "status": "active",
        }
        self._next_id += 1
        self._fallback_store.append(record)
        return dict(record)

    def update_subject(self, subject_id: int, token: Optional[str] = None, **fields) -> Optional[Dict[str, Any]]:
        if "name" in fields and fields["name"] is not None and not str(fields["name"]).strip():
            raise ValueError("O nome da disciplina não pode ser vazio.")

        active_token = token or self.auth_token
        payload = {}
        for k, v in fields.items():
            if v is not None:
                payload[k] = v.strip() if isinstance(v, str) else v

        if active_token:
            resp = self._dispatch_request("PATCH", f"subjects/{subject_id}", token=active_token, json=payload)
            if resp.status_code == 200:
                return resp.json()
            else:
                try:
                    err_msg = resp.json().get("message") or resp.text
                except Exception:
                    err_msg = resp.text
                raise RuntimeError(f"Erro do Xano ({resp.status_code}): {err_msg}")

        for s in self._fallback_store:
            if s.get("id") == subject_id:
                for k, v in payload.items():
                    s[k] = v
                return dict(s)
        return None

    def delete_subject(self, subject_id: int, token: Optional[str] = None) -> bool:
        active_token = token or self.auth_token
        if active_token:
            resp = self._dispatch_request("DELETE", f"subjects/{subject_id}", token=active_token)
            if resp.status_code in (200, 204):
                return True
            else:
                try:
                    err_msg = resp.json().get("message") or resp.text
                except Exception:
                    err_msg = resp.text
                raise RuntimeError(f"Erro do Xano ({resp.status_code}): {err_msg}")

        for i, s in enumerate(self._fallback_store):
            if s.get("id") == subject_id:
                self._fallback_store.pop(i)
                return True
        return False


# Default global instance
default_subject_service = SubjectService()
