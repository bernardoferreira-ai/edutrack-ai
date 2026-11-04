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

# Canonical defined in api/academic_tasks/academic_tasks.xs
TASKS_CANONICAL = "T4bwHPe_"

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

def _normalize_date_for_xano(d_str: Optional[str]) -> Optional[str]:
    """Converte datas DD/MM/YYYY para formato ISO YYYY-MM-DD exigido pelo Xano."""
    if not d_str:
        return None
    cleaned = d_str.strip()
    if "/" in cleaned:
        parts = cleaned.split("/")
        if len(parts) == 3 and len(parts[2]) == 4:
            return f"{parts[2]}-{parts[1].zfill(2)}-{parts[0].zfill(2)}"
    return cleaned


class TaskService:
    def __init__(self, api_url: Optional[str] = None, auth_token: Optional[str] = None):
        _load_env_file()
        self.api_url = (
            api_url 
            or os.getenv("XANO_TASKS_URL")
            or os.getenv("XANO_API_URL") 
            or os.getenv("URL_BASE_ALT")
        )
        if self.api_url:
            self.api_url = self.api_url.rstrip("/")
        self.auth_token = auth_token or os.getenv("XANO_AUTH_TOKEN")
        self._fallback_store: List[Dict[str, Any]] = [dict(t) for t in INITIAL_TASKS]
        self._next_id: int = max([t["id"] for t in self._fallback_store], default=0) + 1
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
            # 1. URL com o canonical do grupo Academic Tasks (T4bwHPe_)
            candidates.append(f"{host}/api:{TASKS_CANONICAL}/{suffix}")
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
                    last_resp = resp
                    continue
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

    def list_tasks(
        self,
        token: Optional[str] = None,
        subject_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        active_token = token or self.auth_token
        if active_token:
            try:
                params: Dict[str, Any] = {}
                if subject_id:
                    params["subject_id"] = int(subject_id)
                if status and status != "Todas":
                    mapped_status = status.lower()
                    if mapped_status in ["concluída", "concluida"]:
                        mapped_status = "completed"
                    elif mapped_status in ["pendente"]:
                        mapped_status = "pending"
                    params["status"] = mapped_status

                resp = self._dispatch_request("GET", "academic_tasks", token=active_token, params=params)
                if resp.status_code == 200:
                    data = resp.json()
                    if isinstance(data, list):
                        return data
                elif resp.status_code == 401:
                    pass
            except Exception:
                pass  # Fallback quando offline

        results = self._fallback_store
        if subject_id:
            results = [t for t in results if t.get("subject_id") == int(subject_id)]
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
        if active_token:
            try:
                resp = self._dispatch_request("GET", f"academic_tasks/{task_id}", token=active_token)
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

        resolved_desc = (description or "").strip()
        payload: Dict[str, Any] = {
            "title": cleaned_title,
            "subject_id": int(subject_id),
            "description": resolved_desc,
            "status": status if status in ["pending", "completed"] else "pending"
        }
        if due_date:
            normalized_date = _normalize_date_for_xano(due_date)
            if normalized_date:
                payload["due_date"] = normalized_date

        active_token = token or self.auth_token
        if active_token:
            resp = self._dispatch_request("POST", "academic_tasks", token=active_token, json=payload)
            if resp.status_code in (200, 201):
                record = resp.json()
                if "due_date" not in record or not record.get("due_date"):
                    record["due_date"] = due_date
                return record
            else:
                try:
                    err_msg = resp.json().get("message") or resp.text
                except Exception:
                    err_msg = resp.text
                raise RuntimeError(f"Erro do Xano ({resp.status_code}): {err_msg}")

        # Fallback creation
        record = {
            "id": self._next_id,
            "created_at": "2026-09-23T12:00:00Z",
            "title": cleaned_title,
            "subject_id": int(subject_id),
            "description": description.strip() if description else "",
            "due_date": due_date or "20/02/2026",
            "status": status if status in ["pending", "completed"] else "pending"
        }
        self._next_id += 1
        self._fallback_store.append(record)
        return dict(record)

    def update_task(self, task_id: int, token: Optional[str] = None, **fields) -> Optional[Dict[str, Any]]:
        active_token = token or self.auth_token
        payload = {}
        for k, v in fields.items():
            if v is not None:
                if k == "due_date" and isinstance(v, str):
                    payload[k] = _normalize_date_for_xano(v)
                elif k == "subject_id":
                    payload[k] = int(v)
                else:
                    payload[k] = v.strip() if isinstance(v, str) else v

        if active_token:
            resp = self._dispatch_request("PATCH", f"academic_tasks/{task_id}", token=active_token, json=payload)
            if resp.status_code == 200:
                return resp.json()
            else:
                try:
                    err_msg = resp.json().get("message") or resp.text
                except Exception:
                    err_msg = resp.text
                raise RuntimeError(f"Erro do Xano ({resp.status_code}): {err_msg}")

        for t in self._fallback_store:
            if t.get("id") == task_id:
                for k, v in fields.items():
                    if v is not None:
                        t[k] = v
                return dict(t)
        return None

    def delete_task(self, task_id: int, token: Optional[str] = None) -> bool:
        active_token = token or self.auth_token
        if active_token:
            resp = self._dispatch_request("DELETE", f"academic_tasks/{task_id}", token=active_token)
            if resp.status_code in (200, 204):
                return True
            else:
                try:
                    err_msg = resp.json().get("message") or resp.text
                except Exception:
                    err_msg = resp.text
                raise RuntimeError(f"Erro do Xano ({resp.status_code}): {err_msg}")

        for i, t in enumerate(self._fallback_store):
            if t.get("id") == task_id:
                self._fallback_store.pop(i)
                return True
        return False


# Default global instance
default_task_service = TaskService()
