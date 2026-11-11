# Design: migracao-env-para-secrets

## Overview
Migrar a obtenção de variáveis e parâmetros de conexão de arquivos `.env` para o mecanismo oficial do Streamlit (`st.secrets` com o arquivo `.streamlit/secrets.toml`), preservando compatibilidade com ferramentas de terminal e scripts avulsos.

## Arquitetura de Configuração

### 1. Resolução Hierárquica de Configurações
Para evitar que scripts avulsos (ex.: `calculate_progress.py`, `generate_student_report.py`) quebrem ao rodar sem a interface do Streamlit inicializada, o sistema implementará a resolução hierárquica através de `services/config.py`:

1. **`st.secrets`**: Tenta acessar `st.secrets[key]` ou `st.secrets.get(key)`. Captura exceções esperadas caso o contexto do Streamlit não esteja ativo ou o arquivo de secrets não exista (`FileNotFoundError`, `KeyError`, `AttributeError`, etc.).
2. **`os.getenv(key)`**: Caso a chave não seja encontrada em `st.secrets` ou o Streamlit não esteja disponível, recorre ao ambiente do sistema operacional.
3. **`.env` fallback**: Mantém a leitura secundária de `.env` caso a variável ainda não tenha sido definida, permitindo que desenvolvedores continuem utilizando `.env` em ambientes legados ou CLI.

### 2. Formato do arquivo `.streamlit/secrets.toml`
O arquivo `.streamlit/secrets.toml` utilizará a sintaxe TOML padrão:
```toml
URL_BASE_ALT = "https://x8ki-letl-twmt.n7.xano.io/api:dyXfRo9-"
```

### 3. Integração nos Serviços
Os serviços `AuthService`, `SubjectService` e `TaskService` importarão o utilitário `get_config(key, default=None)` de `services/config.py` para definir as URLs base do Xano e tokens padrão.

### 4. Segurança no Versionamento
A pasta `.streamlit/` já está declarada no `.gitignore`, garantindo que credenciais e URLs de secrets permaneçam fora dos commits do Git.
