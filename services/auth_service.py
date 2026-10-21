import os
import requests
from typing import Dict, Any, Optional

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


class AuthService:
    def __init__(self, api_url: Optional[str] = None):
        _load_env_file()
        self.api_url = (
            api_url
            or os.getenv("XANO_API_URL")
            or os.getenv("URL_BASE_ALT")
            or os.getenv("XANO_AUTH_URL")
        )
        if self.api_url:
            self.api_url = self.api_url.rstrip("/")

        # In-memory storage for offline / testing fallback
        self._fallback_users: Dict[str, Dict[str, Any]] = {
            "aluno@edutrack.ai": {
                "id": 1,
                "name": "Aluno Exemplo",
                "email": "aluno@edutrack.ai",
                "password": "Password123",
                "role": "member",
                "created_at": "2026-10-01T10:00:00Z"
            }
        }

    def _get_headers(self, auth_token: Optional[str] = None) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"
        return headers

    def signup(self, name: str, email: str, password: str) -> Dict[str, Any]:
        """
        Registers a new user via POST /auth/signup.
        Saves user details into the user table.
        """
        name = name.strip() if name else ""
        email = email.strip().lower() if email else ""
        password = password.strip() if password else ""

        if not name or not email or not password:
            raise ValueError("Todos os campos (nome, email e senha) são obrigatórios.")

        if self.api_url:
            try:
                url = f"{self.api_url}/auth/signup"
                resp = requests.post(
                    url,
                    headers=self._get_headers(),
                    json={"name": name, "email": email, "password": password},
                    timeout=5
                )
                if resp.status_code in (200, 201):
                    return resp.json()
                
                # Parse error response
                err_data = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
                msg = err_data.get("message") or err_data.get("error") or f"Erro {resp.status_code} no cadastro."
                raise ValueError(msg)
            except requests.exceptions.RequestException as e:
                # If network connection fails, we can report or fallback
                raise ConnectionError(f"Falha de conexão com o servidor Xano: {str(e)}")

        # Fallback offline simulation when API URL is not set
        if email in self._fallback_users:
            raise ValueError("Já existe uma conta com este e-mail.")

        new_id = len(self._fallback_users) + 1
        user_record = {
            "id": new_id,
            "name": name,
            "email": email,
            "password": password,
            "role": "member",
            "created_at": "2026-10-21T10:00:00Z"
        }
        self._fallback_users[email] = user_record
        return {"authToken": f"mock_token_{new_id}", "user_id": new_id}

    def login(self, email: str, password: str) -> Dict[str, Any]:
        """
        Authenticates an existing user via POST /auth/login.
        Returns authToken and user_id.
        """
        email = email.strip().lower() if email else ""
        password = password.strip() if password else ""

        if not email or not password:
            raise ValueError("Email e senha são obrigatórios.")

        if self.api_url:
            try:
                url = f"{self.api_url}/auth/login"
                resp = requests.post(
                    url,
                    headers=self._get_headers(),
                    json={"email": email, "password": password},
                    timeout=5
                )
                if resp.status_code == 200:
                    return resp.json()

                err_data = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
                msg = err_data.get("message") or err_data.get("error") or "Credenciais inválidas."
                raise ValueError(msg)
            except requests.exceptions.RequestException as e:
                raise ConnectionError(f"Falha de conexão com o servidor Xano: {str(e)}")

        # Fallback offline simulation
        user = self._fallback_users.get(email)
        if not user or user["password"] != password:
            raise ValueError("Credenciais inválidas. Verifique seu e-mail e senha.")

        return {"authToken": f"mock_token_{user['id']}", "user_id": user["id"]}

    def get_me(self, auth_token: str) -> Dict[str, Any]:
        """
        Retrieves authenticated user profile via GET /auth/me.
        """
        if not auth_token:
            raise ValueError("Token de autenticação não fornecido.")

        if self.api_url:
            try:
                url = f"{self.api_url}/auth/me"
                resp = requests.get(
                    url,
                    headers=self._get_headers(auth_token),
                    timeout=5
                )
                if resp.status_code == 200:
                    return resp.json()

                err_data = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
                msg = err_data.get("message") or err_data.get("error") or "Sessão inválida ou expirada."
                raise ValueError(msg)
            except requests.exceptions.RequestException as e:
                raise ConnectionError(f"Falha de conexão com o servidor Xano: {str(e)}")

        # Fallback offline simulation
        for u in self._fallback_users.values():
            if f"mock_token_{u['id']}" == auth_token:
                return {
                    "id": u["id"],
                    "name": u["name"],
                    "email": u["email"],
                    "role": u.get("role", "member"),
                    "created_at": u.get("created_at")
                }

        return {
            "id": 1,
            "name": "Usuário EduTrack",
            "email": "usuario@edutrack.ai",
            "role": "member",
            "created_at": "2026-10-21T10:00:00Z"
        }

