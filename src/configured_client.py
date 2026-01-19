import os
from src.external_api import fetch_user

def get_user_from_env(user_id: int) -> dict:
    base_url = os.getenv("BASE_URL", "https://default.api.com")
    timeout = int(os.getenv("TIMEOUT", "5"))
    return fetch_user(user_id, base_url=base_url, timeout=timeout)