## Context

The user requested a Python script in `scripts/calculate_progress.py` that computes the progress percentage (completed tasks / total tasks) for a given academic subject based on its tasks, returning a structured JSON object. The implementation must consume the existing CRUD endpoints.

Per `AGENTS.md`:
- Scope is strictly bounded to the requested script.
- No frontend alterations, no new Xano tables/endpoints, and no automated push/deploy.

## Goals / Non-Goals

**Goals:**
- Implement `scripts/calculate_progress.py` providing:
  - Function `calculate_subject_progress(subject_id: int, api_url: Optional[str] = None, auth_token: Optional[str] = None) -> Dict[str, Any]` (and helper returning JSON string).
  - Integration with `GET /academic_tasks?subject_id={id}` using `requests`.
  - Normalization of task status: treats `"completed"`, `"concluída"`, `"concluida"`, and `"done"` (case-insensitive) as completed.
  - Calculation formula: `round((completed_tasks / total_tasks) * 100, 2)` when `total_tasks > 0`, else `0.0`.
  - Standard JSON response format.
  - CLI execution via `argparse` allowing `python scripts/calculate_progress.py --subject-id <id>`.

**Non-Goals:**
- Modifying Streamlit pages (`pages/` or `app.py`) (out of scope).
- Creating new backend API endpoints or modifying Xano `.xs` files (out of scope).
- Automated test suites (out of scope).
- Deploying or syncing to Xano (strictly prohibited by `AGENTS.md` Rule #2).

## Decisions

### 1. File Location & CLI Interface
- File: `scripts/calculate_progress.py`
- Exposes:
  - Importable function: `calculate_subject_progress(...)`
  - CLI execution: `python scripts/calculate_progress.py --subject-id 1 [--auth-token <token>] [--api-url <url>]`
  - Output: formatted JSON printed to stdout.

### 2. API Communication & Authentication
- Reads `XANO_API_URL` or `URL_BASE_ALT` from environment / `.env`.
- Reads `XANO_AUTH_TOKEN` from environment / `.env` if not passed directly.
- Sends `GET {api_url}/academic_tasks?subject_id={subject_id}` with `Authorization: Bearer <token>`.
- Graceful offline / fallback handling: if no API is available, allows passing mock tasks list or returns a clean JSON error response.

### 3. Calculation & Output Schema
- Status matching logic:
  ```python
  is_completed = task.get("status", "").strip().lower() in ("completed", "concluída", "concluida", "done")
  ```
- Result dictionary / JSON:
  ```json
  {
    "subject_id": 1,
    "total_tasks": 5,
    "completed_tasks": 3,
    "pending_tasks": 2,
    "progress_percentage": 60.0
  }
  ```

## Risks / Trade-offs

- **[Risk]** Division by zero when a subject has 0 tasks.
  → **Mitigation**: Explicit check `if total_tasks == 0: progress_percentage = 0.0`.
- **[Risk]** Varied status strings stored in database.
  → **Mitigation**: Check status case-insensitively against multiple common completion aliases.

