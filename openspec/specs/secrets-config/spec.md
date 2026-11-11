# secrets-config Specification

## Purpose
Define the configuration and secrets resolution mechanism for EduTrack AI, migrating environment variable retrieval from `.env` to Streamlit native secrets (`st.secrets`).

## Requirements

### Requirement: Streamlit Secrets Priority Resolution
The system SHALL retrieve configuration parameters (such as `URL_BASE_ALT`, `XANO_API_URL`, `XANO_AUTH_TOKEN`) primarily from Streamlit secrets (`st.secrets`) when running within a Streamlit application context.

#### Scenario: Running within Streamlit with secrets configured
- **WHEN** the application requests a configuration key and `st.secrets` contains the key
- **THEN** the system SHALL return the value from `st.secrets`

#### Scenario: Fallback to environment variables when secret key is absent
- **WHEN** the application requests a configuration key not present in `st.secrets` or when running outside Streamlit
- **THEN** the system SHALL fallback to `os.getenv` or `.env` to retrieve the key

### Requirement: Format Secrets in TOML Syntax
The system SHALL maintain secrets in `.streamlit/secrets.toml` using valid TOML key-value formatting and ensure this file is ignored by Git.

#### Scenario: Secrets file formatting
- **WHEN** secrets are stored in `.streamlit/secrets.toml`
- **THEN** each string value SHALL be enclosed in valid TOML quotes and `.gitignore` SHALL include `.streamlit/`

### Requirement: Update Service Modules to Use Secrets
The services (`auth_service`, `subject_service`, `task_service`) SHALL resolve backend URLs and configuration via the secrets mechanism.

#### Scenario: Service initialization
- **WHEN** an API service is instantiated without explicit URL overrides
- **THEN** the service SHALL obtain its base API URL and configuration using the secrets resolution mechanism
