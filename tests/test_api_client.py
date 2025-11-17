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


@pytest.mark.asyncio
async def test_api_client_initialize(monkeypatch):
    """initialize() should call ensure_authenticated."""
    client = APIClient()
    auth_called = {"called": False}

    async def fake_ensure_authenticated():
        auth_called["called"] = True

    monkeypatch.setattr(client.auth, "ensure_authenticated", fake_ensure_authenticated)

    await client.initialize()

    assert auth_called["called"] is True


@pytest.mark.asyncio
async def test_api_client_post(monkeypatch):
    """POST should send data and return response."""
    client = APIClient()

    async def fake_ensure_authenticated():
        return None

    def fake_get_headers():
        return {"Authorization": "Bearer test-token"}

    monkeypatch.setattr(client.auth, "ensure_authenticated", fake_ensure_authenticated)
    monkeypatch.setattr(client.auth, "get_headers", fake_get_headers)

    fake_response = FakeHTTPResponse(200, {"id": 1, "name": "Test"})

    def fake_async_client_factory(*args, **kwargs):
        return FakeAsyncClient([fake_response])

    import httpx

    monkeypatch.setattr(httpx, "AsyncClient", fake_async_client_factory)

    data = await client.post("/classic-models/api/v1/products/", {"name": "Test"})

    assert data == {"id": 1, "name": "Test"}


@pytest.mark.asyncio
async def test_api_client_put(monkeypatch):
    """PUT should send data and return response."""
    client = APIClient()

    async def fake_ensure_authenticated():
        return None

    def fake_get_headers():
        return {"Authorization": "Bearer test-token"}

    monkeypatch.setattr(client.auth, "ensure_authenticated", fake_ensure_authenticated)
    monkeypatch.setattr(client.auth, "get_headers", fake_get_headers)

    fake_response = FakeHTTPResponse(200, {"id": 1, "name": "Updated"})

    def fake_async_client_factory(*args, **kwargs):
        return FakeAsyncClient([fake_response])

    import httpx

    monkeypatch.setattr(httpx, "AsyncClient", fake_async_client_factory)

    data = await client.put("/classic-models/api/v1/products/1/", {"name": "Updated"})

    assert data == {"id": 1, "name": "Updated"}


@pytest.mark.asyncio
async def test_api_client_patch(monkeypatch):
    """PATCH should send data and return response."""
    client = APIClient()

    async def fake_ensure_authenticated():
        return None

    def fake_get_headers():
        return {"Authorization": "Bearer test-token"}

    monkeypatch.setattr(client.auth, "ensure_authenticated", fake_ensure_authenticated)
    monkeypatch.setattr(client.auth, "get_headers", fake_get_headers)

    fake_response = FakeHTTPResponse(200, {"id": 1, "name": "Patched"})

    def fake_async_client_factory(*args, **kwargs):
        return FakeAsyncClient([fake_response])

    import httpx

    monkeypatch.setattr(httpx, "AsyncClient", fake_async_client_factory)

    data = await client.patch("/classic-models/api/v1/products/1/", {"name": "Patched"})

    assert data == {"id": 1, "name": "Patched"}


@pytest.mark.asyncio
async def test_api_client_delete(monkeypatch):
    """DELETE should not return data."""
    client = APIClient()

    async def fake_ensure_authenticated():
        return None

    def fake_get_headers():
        return {"Authorization": "Bearer test-token"}

    monkeypatch.setattr(client.auth, "ensure_authenticated", fake_ensure_authenticated)
    monkeypatch.setattr(client.auth, "get_headers", fake_get_headers)

    fake_response = FakeHTTPResponse(204)

    def fake_async_client_factory(*args, **kwargs):
        return FakeAsyncClient([fake_response])

    import httpx

    monkeypatch.setattr(httpx, "AsyncClient", fake_async_client_factory)

    await client.delete("/classic-models/api/v1/products/1/")


@pytest.mark.asyncio
async def test_api_client_close(monkeypatch):
    """close() should close the auth manager."""
    client = APIClient()
    close_called = {"called": False}

    async def fake_close():
        close_called["called"] = True

    monkeypatch.setattr(client.auth, "close", fake_close)

    await client.close()

    assert close_called["called"] is True


@pytest.mark.asyncio
async def test_api_client_handles_http_status_error(monkeypatch):
    """_request should handle HTTPStatusError with JSON error."""
    client = APIClient()

    async def fake_ensure_authenticated():
        return None

    def fake_get_headers():
        return {"Authorization": "Bearer test-token"}

    monkeypatch.setattr(client.auth, "ensure_authenticated", fake_ensure_authenticated)
    monkeypatch.setattr(client.auth, "get_headers", fake_get_headers)

    class FakeHTTPStatusError(Exception):
        def __init__(self):
            self.response = FakeHTTPResponse(400, {"detail": "Bad request"})

    def fake_async_client_factory(*args, **kwargs):
        class FakeClient:
            async def __aenter__(self):
                return self

            async def __aexit__(self, *args):
                return False

            async def request(self, **kwargs):
                import httpx
                error = httpx.HTTPStatusError("Error", request=None, response=FakeHTTPResponse(400, {"detail": "Bad request"}))
                error.response = FakeHTTPResponse(400, {"detail": "Bad request"})
                raise error

        return FakeClient()

    import httpx

    monkeypatch.setattr(httpx, "AsyncClient", fake_async_client_factory)

    with pytest.raises(Exception, match="API request failed: 400"):
        await client.get("/classic-models/api/v1/products/")


@pytest.mark.asyncio
async def test_api_client_handles_http_status_error_non_json(monkeypatch):
    """_request should handle HTTPStatusError with non-JSON error text."""
    client = APIClient()

    async def fake_ensure_authenticated():
        return None

    def fake_get_headers():
        return {"Authorization": "Bearer test-token"}

    monkeypatch.setattr(client.auth, "ensure_authenticated", fake_ensure_authenticated)
    monkeypatch.setattr(client.auth, "get_headers", fake_get_headers)

    def fake_async_client_factory(*args, **kwargs):
        class FakeClient:
            async def __aenter__(self):
                return self

            async def __aexit__(self, *args):
                return False

            async def request(self, **kwargs):
                import httpx
                # Create response that can't be parsed as JSON
                response = FakeHTTPResponse(400, None)
                response.text = "Plain text error"
                # Make json() raise an exception
                response.json = lambda: __import__('json').loads("invalid")
                error = httpx.HTTPStatusError("Error", request=None, response=response)
                error.response = response
                raise error

        return FakeClient()

    import httpx

    monkeypatch.setattr(httpx, "AsyncClient", fake_async_client_factory)

    with pytest.raises(Exception, match="API request failed: 400"):
        await client.get("/classic-models/api/v1/products/")


@pytest.mark.asyncio
async def test_api_client_handles_request_error(monkeypatch):
    """_request should handle RequestError."""
    client = APIClient()

    async def fake_ensure_authenticated():
        return None

    def fake_get_headers():
        return {"Authorization": "Bearer test-token"}

    monkeypatch.setattr(client.auth, "ensure_authenticated", fake_ensure_authenticated)
    monkeypatch.setattr(client.auth, "get_headers", fake_get_headers)

    def fake_async_client_factory(*args, **kwargs):
        class FakeClient:
            async def __aenter__(self):
                return self

            async def __aexit__(self, *args):
                return False

            async def request(self, **kwargs):
                import httpx
                raise httpx.RequestError("Connection failed")

        return FakeClient()

    import httpx

    monkeypatch.setattr(httpx, "AsyncClient", fake_async_client_factory)

    with pytest.raises(Exception, match="Request failed"):
        await client.get("/classic-models/api/v1/products/")



