"""Unit tests for APIClient."""
from typing import Any

import pytest

from src.api.client import APIClient


class FakeHTTPResponse:
    def __init__(self, status_code: int, json_data: dict | None = None, text: str = ""):
        self.status_code = status_code
        self._json_data = json_data or {}
        self.text = text or ""

    def raise_for_status(self) -> None:
        if 400 <= self.status_code:
            raise Exception(f"HTTP {self.status_code}")

    def json(self) -> dict:
        return self._json_data


class FakeAsyncClient:
    """Fake httpx.AsyncClient for testing."""

    def __init__(self, responses: list[FakeHTTPResponse]):
        self._responses = responses
        self.requests: list[dict[str, Any]] = []

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def request(self, *, method: str, url: str, headers: dict, json: dict | None, params: dict | None, timeout: float):
        self.requests.append(
            {
                "method": method,
                "url": url,
                "headers": headers,
                "json": json,
                "params": params,
                "timeout": timeout,
            }
        )
        if not self._responses:
            raise RuntimeError("No fake responses configured")
        return self._responses.pop(0)


@pytest.mark.asyncio
async def test_api_client_get_success(monkeypatch):
    """GET should return parsed JSON on success."""
    client = APIClient()

    # Stub auth to avoid real login
    async def fake_ensure_authenticated():
        return None

    def fake_get_headers():
        return {"Authorization": "Bearer test-token"}

    monkeypatch.setattr(client.auth, "ensure_authenticated", fake_ensure_authenticated)
    monkeypatch.setattr(client.auth, "get_headers", fake_get_headers)

    # Fake httpx.AsyncClient
    fake_response = FakeHTTPResponse(200, {"ok": True})

    def fake_async_client_factory(*args, **kwargs):
        return FakeAsyncClient([fake_response])

    import httpx

    monkeypatch.setattr(httpx, "AsyncClient", fake_async_client_factory)

    data = await client.get("/classic-models/api/v1/products/")

    assert data == {"ok": True}


@pytest.mark.asyncio
async def test_api_client_retries_on_401(monkeypatch):
    """Client should refresh token and retry once on 401."""
    client = APIClient()

    async def fake_ensure_authenticated():
        return None

    headers_calls = {"count": 0}

    def fake_get_headers():
        headers_calls["count"] += 1
        return {"Authorization": f"Bearer token-{headers_calls['count']}"}

    async def fake_refresh_access_token():
        headers_calls["refreshed"] = True

    monkeypatch.setattr(client.auth, "ensure_authenticated", fake_ensure_authenticated)
    monkeypatch.setattr(client.auth, "get_headers", fake_get_headers)
    monkeypatch.setattr(client.auth, "refresh_access_token", fake_refresh_access_token)

    # First response: 401, second: 200
    responses = [
        FakeHTTPResponse(401, text="Unauthorized"),
        FakeHTTPResponse(200, {"ok": True}),
    ]

    def fake_async_client_factory(*args, **kwargs):
        return FakeAsyncClient(responses)

    import httpx

    monkeypatch.setattr(httpx, "AsyncClient", fake_async_client_factory)

    data = await client.get("/classic-models/api/v1/products/")

    assert data == {"ok": True}
    # Should have called get_headers twice (before and after refresh)
    assert headers_calls["count"] == 2
    assert headers_calls.get("refreshed") is True



