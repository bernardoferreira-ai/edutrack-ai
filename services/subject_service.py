import os
import requests
from typing import List, Dict, Optional, Any

try:
    from services.config import get_config
except ImportError:
    try:
        from config import get_config
    except ImportError:
        def get_config(k, default=None):
            return os.getenv(k, default)

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
        self.api_url = (
            api_url 
            or get_config("XANO_SUBJECTS_URL")
            or get_config("XANO_API_URL") 
            or get_config("URL_BASE_ALT")
        )
        if self.api_url:
            self.api_url = self.api_url.rstrip("/")
        self.auth_token = auth_token or get_config("XANO_AUTH_TOKEN")
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
        token: Optional[str] = None,
        code: Optional[str] = None,
        professor: Optional[str] = None,
        semester: Optional[str] = None,
        color: Optional[str] = None,
        status: Optional[str] = None,
    ) -> Dict[str, Any]:
        cleaned_name = name.strip()
        if not cleaned_name:
            raise ValueError("O nome da disciplina é obrigatório.")

        resolved_teacher = (professor or teacher).strip()
        # Xano exige 'hours'; se não informado, define valor padrão de 60 horas
        resolved_hours = int(hours) if hours is not None else 60
        payload: Dict[str, Any] = {
            "name": cleaned_name,
            "teacher": resolved_teacher,
            "hours": resolved_hours,
        }
        if code:
            payload["code"] = code
        if semester:
            payload["semester"] = semester
        if color:
            payload["color"] = color
        if status:
            payload["status"] = status
        if dia_semana:
            payload["dia_semana"] = dia_semana

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
            "code": code or "",
            "teacher": resolved_teacher,
            "professor": resolved_teacher,
            "hours": resolved_hours,
            "semester": semester or "",
            "color": color or "#4F46E5",
            "dia_semana": dia_semana,
            "status": status or "active",
        }
        self._next_id += 1
        self._fallback_store.append(record)
        return dict(record)

    def update_subject(self, subject_id: int, token: Optional[str] = None, **fields) -> Optional[Dict[str, Any]]:
        if "name" in fields and fields["name"] is not None and not str(fields["name"]).strip():
            raise ValueError("O nome da disciplina não pode ser vazio.")

        active_token = token or self.auth_token

        # Sanitiza os campos recebidos (remove None, faz strip em strings)
        incoming = {}
        for k, v in fields.items():
            if v is not None:
                incoming[k] = v.strip() if isinstance(v, str) else v

        if active_token:
            # ── Estratégia de merge: busca o registro atual e mescla os campos
            # novos sobre ele, garantindo que todos os campos obrigatórios do
            # endpoint PATCH (name, teacher, hours) sejam sempre enviados, mesmo
            # quando o chamador atualiza apenas um subconjunto deles.
            current: Dict[str, Any] = {}
            try:
                resp_get = self._dispatch_request("GET", f"subjects/{subject_id}", token=active_token)
                if resp_get.status_code == 200:
                    current = resp_get.json() or {}
            except Exception:
                pass  # Se GET falhar, prossegue com o que foi passado

            # Campos obrigatórios no Xano — garante que nunca ficam ausentes
            REQUIRED_FIELDS = ("name", "teacher", "hours")
            payload: Dict[str, Any] = {}
            for field in REQUIRED_FIELDS:
                # Prioridade: valor novo (incoming) > valor atual (current) > "" / 0
                if field in incoming:
                    payload[field] = incoming[field]
                elif field in current and current[field] is not None:
                    payload[field] = current[field]
                else:
                    payload[field] = 0 if field == "hours" else ""

            # Inclui demais campos opcionais que foram explicitamente passados
            for k, v in incoming.items():
                if k not in payload:
                    payload[k] = v

            resp = self._dispatch_request("PATCH", f"subjects/{subject_id}", token=active_token, json=payload)
            if resp.status_code == 200:
                return resp.json()
            else:
                try:
                    err_msg = resp.json().get("message") or resp.text
                except Exception:
                    err_msg = resp.text
                raise RuntimeError(f"Erro do Xano ({resp.status_code}): {err_msg}")

        # Fallback offline: aplica apenas os campos recebidos no store local
        for s in self._fallback_store:
            if s.get("id") == subject_id:
                for k, v in incoming.items():
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

    def get_active_count(self) -> int:
        return sum(1 for subject in self._fallback_store if subject.get("status", "active") != "completed")


# Default global instance
default_subject_service = SubjectService()
