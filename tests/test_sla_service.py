import importlib

api_client_module = importlib.import_module("app.services.api_client")
from app.services.sla_service import SLAService


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


def test_get_dashboard_data_builds_sla_requests(monkeypatch):
    requests_seen = []

    def fake_request(method, url, params, json, headers, timeout):
        requests_seen.append((method, url, params))
        if url.endswith("/sla/summary"):
            return DummyResponse(json_data={
                "on_time_rate": 90.0,
                "resolution_sla_rate": 88.0,
                "open_breaches": 12,
                "avg_resolution_hours": 4.5,
            })
        if url.endswith("/sla/breach-trends"):
            return DummyResponse(json_data={"items": [{"day": "Mon", "breaches": 3}]})
        if url.endswith("/sla/resolution-times"):
            return DummyResponse(json_data={"items": [{"day": "Mon", "avg_hours": 4.2, "p95_hours": 6.1}]})
        if url.endswith("/sla/queue-health"):
            return DummyResponse(json_data={"items": [{"queue": "Fraud", "on_time_pct": 89, "slo_target_pct": 92, "open_cases": 8, "at_risk_cases": 1, "status": "At risk"}]})
        return DummyResponse(status_code=404, json_data={"error": "not found"})

    monkeypatch.setattr(api_client_module.requests, "request", fake_request)

    service = SLAService(base_url="http://api.test", timeout=5)
    result = service.get_dashboard_data(days=7)

    assert len(requests_seen) == 4
    assert requests_seen[1][2] == {"days": 7}
    assert requests_seen[2][2] == {"days": 7}
    assert result["is_fallback"] is False
    assert result["summary"]["open_breaches"] == 12
    assert result["breach_trends"][0]["breaches"] == 3


def test_get_dashboard_data_falls_back_on_api_error(monkeypatch):
    def fake_request(method, url, params, json, headers, timeout):
        return DummyResponse(status_code=500, json_data={"error": "server"})

    monkeypatch.setattr(api_client_module.requests, "request", fake_request)

    service = SLAService(base_url="http://api.test", timeout=5)
    result = service.get_dashboard_data(days=7)

    assert result["is_fallback"] is True
    assert "summary" in result
    assert len(result["breach_trends"]) > 0
