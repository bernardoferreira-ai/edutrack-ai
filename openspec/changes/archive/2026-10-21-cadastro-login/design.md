## Context

The user requested planning the implementation of a Python script in `pages/3_👤_Perfil.py` that enables user registration and login in EduTrack AI, utilizing the existing authentication endpoints (`auth/login`, `auth/signup`, `auth/me`) and the `user` table.

Per `AGENTS.md`:
- Scope is strictly bounded to what was explicitly requested.
- Responsibility ends at code generation (no deployment/push to Xano).
- Adheres to Streamlit conventions and Python error handling.

## Goals / Non-Goals

**Goals:**
- Implement `pages/3_👤_Perfil.py` providing tabs/interfaces for Login, Cadastro (Signup), and Perfil (when authenticated).
- Integrate with Xano's `auth/login`, `auth/signup`, and `auth/me` endpoints.
- Manage authentication state using Streamlit's `st.session_state` (`auth_token`, `user_profile`).
- Provide user feedback (success banners, error messages for invalid credentials, logout functionality).

**Non-Goals:**
- Creating new backend API endpoints or altering existing `.xs` files (out of scope).
- Creating new database tables (out of scope).
- Automated test suites (out of scope).
- Modifying other unrelated pages (out of scope).

## Decisions

### 1. Authentication Integration
- Connect to Xano authentication endpoints:
  - `POST /auth/signup` with payload `{"name": str, "email": str, "password": str}`
  - `POST /auth/login` with payload `{"email": str, "password": str}`
  - `GET /auth/me` with header `Authorization: Bearer <authToken>`
- Base API URL resolved via environment variables (`XANO_API_URL` or `URL_BASE_ALT`), falling back to a configurable default if not defined.

### 2. Streamlit Session State Management
- `st.session_state["auth_token"]`: stores the JWT/Auth token returned by Xano.
- `st.session_state["user_profile"]`: stores the user dictionary returned by `auth/me`.
- If `auth_token` is present:
  - Show user profile information (`name`, `email`, `role`, etc.).
  - Show a "Sair" (Logout) button that resets `auth_token` and `user_profile`.
- If `auth_token` is not present:
  - Show tabs for "Entrar" (Login) and "Cadastrar" (Signup).

### 3. Error Handling & Validation
- Validate non-empty fields before making HTTP requests.
- Wrap requests in `try...except requests.exceptions.RequestException` with user-friendly Streamlit messages (`st.error`).

## Risks / Trade-offs

- **[Risk]** Base URL not configured in `.env`.
  → **Mitigation**: Handle missing configuration gracefully in the UI with an informative warning guiding the user.

