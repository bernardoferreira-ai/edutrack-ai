import os

def _load_env_file():
    """Carrega variáveis de ambiente do arquivo .env como fallback."""
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

def get_config(key: str, default: str | None = None) -> str | None:
    """
    Recupera uma configuração com a seguinte prioridade:
    1. st.secrets (Streamlit secrets - .streamlit/secrets.toml)
    2. os.getenv (Variáveis de ambiente)
    3. .env (Arquivo .env local como fallback)
    4. default fornecido
    """
    # 1. Tentar Streamlit secrets
    try:
        import streamlit as st
        if hasattr(st, "secrets") and st.secrets is not None:
            if key in st.secrets:
                val = st.secrets[key]
                if val is not None:
                    return str(val)
    except Exception:
        pass

    # 2. os.getenv
    val = os.getenv(key)
    if val:
        return val

    # 3. .env fallback
    _load_env_file()
    val = os.getenv(key)
    if val:
        return val

    return default

# Alias para compatibilidade
get_secret = get_config
