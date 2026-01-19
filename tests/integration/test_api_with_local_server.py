import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest
import requests 

pytestmark = pytest.mark.integration

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/users/1"):
            body = {"id": 1, "name": "Alice" }
            self.send_response(200)
        else:
            body = {"error": "not found" }
            self.send_response(404)
            
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode('utf-8'))
    
    def log_message(self, format, *args):
        return
    
@pytest.fixture(scope="module")
def api_server():
    server = ThreadingHTTPServer(("localhost", 0), Handler)
    host, port = server.server_address
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://{host}:{port}"
    server.shutdown()
    
def test_users_endpoint_success(api_server):
    r = requests.get(f"{api_server}/users/1", timeout=2)
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == 1
    assert "name" in data
    
def test_users_endpoint_not_found(api_server):
    r = requests.get(f"{api_server}/users/999", timeout=2)
    assert r.status_code == 404
    data = r.json()
    assert "error" in data