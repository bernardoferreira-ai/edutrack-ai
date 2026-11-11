# Change Proposal: migracao-env-para-secrets

## Why
Atualmente a aplicação EduTrack AI carrega variáveis de ambiente e URLs de conexão do Xano diretamente a partir de arquivos `.env` ou de `os.getenv()`. O Streamlit provê um mecanismo nativo e seguro para gestão de credenciais e parâmetros de configuração através de `st.secrets` mapeado no arquivo `.streamlit/secrets.toml`. A migração para `st.secrets` adequa a aplicação ao ecossistema nativo do Streamlit, facilitando o gerenciamento de configurações e garantindo compatibilidade com ambientes locais e em nuvem através de um fallback transparente para variáveis de ambiente.

## What Changes
- Configuração do arquivo `.streamlit/secrets.toml` com sintaxe TOML válida contendo as chaves de configuração do backend (ex.: `URL_BASE_ALT`).
- Criação de utilitário unificado de resolução de configurações (`get_config` / `get_secret`) que prioriza `st.secrets` e mantém fallback automático para `os.getenv` e `.env`.
- Migração da leitura de configurações nos serviços da aplicação (`services/auth_service.py`, `services/subject_service.py`, `services/task_service.py`).
- Suporte à resolução de configurações nos scripts Python (`scripts/calculate_progress.py`, `scripts/generate_student_report.py`).
- Garantia de que `.streamlit/secrets.toml` e `.streamlit/` permaneçam ignorados pelo controle de versão no `.gitignore`.

## Impact
- **Compatibilidade:** Total retrocompatibilidade com execução via terminal/CLI e ambientes sem Streamlit ativo.
- **Segurança:** Segredos e chaves sensíveis mantidos no padrão Streamlit e blindados contra commit acidental no Git.
- **Interface e Layout:** Nenhuma alteração visual, de componentes ou de comportamento nas páginas do Streamlit.
