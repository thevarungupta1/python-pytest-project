# Verify our code handles api success/failure
# avoid any real HTTP/network calls

import pytest
from unittest.mock import MagicMock, patch
from src.external_api import fetch_user, ExternalApiError

@pytest.mark.unit
def test_fetch_user_success_with_patch():
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.json.return_value = {"id": 1, "name": "Alice"}    
    
    with patch("src.external_api.requests.get", return_value=fake_response) as mock_get:
        result = fetch_user(1, "http://fake.api")
        
        assert result["name"] == "Alice"
        mock_get.assert_called_once()
        called_url = mock_get.call_args[0][0]
        assert called_url.endswith("/users/1")
        
@pytest.mark.unit
def test_fetch_user_http_error():
    fake_response = MagicMock()
    fake_response.status_code = 500
    fake_response.json.return_value = {"error": "server"}
    
    with patch("src.external_api.requests.get", return_value=fake_response):
        with pytest.raises(ExternalApiError) as exc:
            fetch_user(2, "http://fake.api")
        
        assert "HTTP 500" in str(exc.value)
        
@pytest.mark.unit
def test_fetch_user_schema_error():
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.json.return_value = {"wrong": "shape"}  
    
    with patch("src.external_api.requests.get", return_value=fake_response):
        with pytest.raises(ExternalApiError) as exc:
            fetch_user(3, "http://fake.api")
        
        assert "schema" in str(exc.value).lower()
        