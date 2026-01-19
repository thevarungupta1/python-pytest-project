

import requests

class ExternalApiError(RuntimeError):
    pass

def fetch_user(user_id: int, base_url: str, timeout: int = 5) -> dict:
    """
    Fetch user JSON from an external service.
    Raise ExternalApiError on HTTP errors or invalid data.
    """
    url = f"{base_url.rstrip('/')}/users/{user_id}"
    resp = requests.get(url, timeout=timeout)
    
    if resp.status_code != 200:
        raise ExternalApiError(f"HTTP {resp.status_code}")

    data = resp.json()
    if "id" not in data or "name" not in data:
        raise ExternalApiError("Invalid response schema")
    
    return data