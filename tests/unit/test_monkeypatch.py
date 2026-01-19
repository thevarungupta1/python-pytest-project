import pytest
from unittest.mock import MagicMock
from src.configured_client import get_user_from_env

@pytest.mark.unit
def test_get_user_from_env(monkeypatch):
    # patch env
    monkeypatch.setenv("BASE_URL", "https://mocked.api.com")
    monkeypatch.setenv("TIMEOUT", "10")
    
    # patch the underlying fetch_user dependency by patching requests.get
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.json.return_value = {"id": 5, "name": "Mocked User"}
    
    monkeypatch.setattr("src.external_api.requests.get", lambda url, timeout: fake_response)
    
    result = get_user_from_env(5)
    assert result["name"] == "Mocked User"