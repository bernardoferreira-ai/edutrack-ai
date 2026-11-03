import os
import sys
import json
import argparse
from typing import List, Dict, Any, Optional, Union
import requests

def _load_env_file():
    """Simple parser to load environment variables from .env if present."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(os.path.dirname(current_dir), ".env")
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


def get_subject_tasks(
    subject_id: int,
    api_url: Optional[str] = None,
    auth_token: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Fetches academic tasks for a given subject from the CRUD API endpoint.
    """
    _load_env_file()
    base_url = (
        api_url
        or os.getenv("XANO_API_URL")
        or os.getenv("URL_BASE_ALT")
        or ""
    ).rstrip("/")

    token = auth_token or os.getenv("XANO_AUTH_TOKEN") or ""

    if not base_url:
        raise ValueError(
            "API URL not provided and neither XANO_API_URL nor URL_BASE_ALT is set in environment."
        )

    url = f"{base_url}/academic_tasks"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    params = {"subject_id": subject_id}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                return data
            return []
        
        err_msg = f"API returned status {response.status_code}"
        try:
            err_data = response.json()
            err_msg = err_data.get("message") or err_data.get("error") or err_msg
        except Exception:
            pass
        raise ConnectionError(f"Failed to fetch tasks: {err_msg}")
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Network error querying academic_tasks: {str(e)}")


def calculate_progress_from_tasks(
    tasks: List[Dict[str, Any]],
    subject_id: Optional[int] = None
) -> Dict[str, Any]:
    """
    Computes completion progress given a list of task records.
    Calculates progress_percentage as (completed_tasks / total_tasks) * 100.
    """
    total_tasks = len(tasks)
    completed_statuses = {"completed", "concluída", "concluida", "done"}

    completed_tasks = 0
    for task in tasks:
        status = str(task.get("status", "")).strip().lower()
        if status in completed_statuses:
            completed_tasks += 1

    pending_tasks = total_tasks - completed_tasks

    if total_tasks > 0:
        progress_percentage = round((completed_tasks / total_tasks) * 100.0, 2)
    else:
        progress_percentage = 0.0

    return {
        "subject_id": subject_id,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "progress_percentage": progress_percentage
    }


def calculate_subject_progress(
    subject_id: int,
    api_url: Optional[str] = None,
    auth_token: Optional[str] = None,
    as_json: bool = True
) -> Union[Dict[str, Any], str]:
    """
    Main function to fetch tasks and calculate progress for a specific subject.
    Returns a structured dictionary or formatted JSON string.
    """
    tasks = get_subject_tasks(subject_id, api_url=api_url, auth_token=auth_token)
    result = calculate_progress_from_tasks(tasks, subject_id=subject_id)

    if as_json:
        return json.dumps(result, indent=2, ensure_ascii=False)
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Calculate academic progress percentage for a subject based on its tasks."
    )
    parser.add_argument(
        "--subject-id",
        type=int,
        required=True,
        help="ID of the subject to calculate progress for"
    )
    parser.add_argument(
        "--api-url",
        type=str,
        default=None,
        help="Base API URL for Xano endpoints (optional, falls back to env)"
    )
    parser.add_argument(
        "--auth-token",
        type=str,
        default=None,
        help="Authentication Bearer token (optional, falls back to env)"
    )

    args = parser.parse_args()

    try:
        json_output = calculate_subject_progress(
            subject_id=args.subject_id,
            api_url=args.api_url,
            auth_token=args.auth_token,
            as_json=True
        )
        print(json_output)
    except Exception as e:
        error_result = {
            "subject_id": args.subject_id,
            "error": str(e)
        }
        print(json.dumps(error_result, indent=2, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

