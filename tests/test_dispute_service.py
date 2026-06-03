import importlib
import pytest

api_client_module = importlib.import_module("app.services.api_client")
from app.services.dispute_service import DisputeService


class DummyResponse:
    def __init__(self, status_code=200, json_data=None, text=None):
        self.status_code = status_code
        self._json_data = json_data or {}
        self._text = text if text is not None else ("" if json_data is None else "json")

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code}")

    def json(self):
        return self._json_data

    @property
    def text(self):
        return self._text


def test_get_disputes_builds_request(monkeypatch):
    captured = {}

    def fake_request(method, url, params, json, headers, timeout):
        captured["method"] = method
        captured["url"] = url
        captured["params"] = params
        captured["json"] = json
        captured["headers"] = headers
        captured["timeout"] = timeout
        return DummyResponse(json_data=[{"dispute_id": "DIS-1001", "status": "Pending"}])

    monkeypatch.setattr(api_client_module.requests, "request", fake_request)

    service = DisputeService(base_url="http://api.test", timeout=5)
    result = service.get_disputes(status="Pending", priority="High", limit=10)

    assert captured["method"] == "get"
    assert captured["url"] == "http://api.test/disputes"
    assert captured["params"] == {"limit": 10, "status": "Pending", "priority": "High"}
    assert result == [{"dispute_id": "DIS-1001", "status": "Pending"}]


def test_get_disputes_propagates_http_error(monkeypatch):
    def fake_request(method, url, params, json, headers, timeout):
        return DummyResponse(status_code=500, json_data={"error": "server"})

    monkeypatch.setattr(api_client_module.requests, "request", fake_request)

    service = DisputeService(base_url="http://api.test")
    with pytest.raises(Exception, match="HTTP 500"):
        service.get_disputes()
