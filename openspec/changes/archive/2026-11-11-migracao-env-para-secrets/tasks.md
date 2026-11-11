# Tasks

## 1. Configuração e Segredos

- [x] 1.1 Configurar `.streamlit/secrets.toml` com sintaxe TOML válida a partir das chaves presentes no `.env` e validar que `.streamlit/` está coberto no `.gitignore`.
- [x] 1.2 Implementar utilitário `services/config.py` com a função de resolução de segredos (`get_secret` / `get_config`) priorizando `st.secrets` e com fallback para `os.getenv` / `.env`.

## 2. Migração dos Serviços e Scripts

- [x] 2.1 Atualizar `services/auth_service.py` para utilizar o resolvedor de configurações via secrets do Streamlit.
- [x] 2.2 Atualizar `services/subject_service.py` e `services/task_service.py` para utilizar o resolvedor de configurações via secrets do Streamlit.
- [x] 2.3 Atualizar os scripts CLI (`scripts/calculate_progress.py` e `scripts/generate_student_report.py`) para utilizar a resolução de secrets/ambiente.
