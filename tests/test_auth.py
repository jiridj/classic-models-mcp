"""Unit tests for AuthManager."""
import pytest

from src.api.auth import AuthManager


class FakeResponse:
    def __init__(self, status_code: int, json_data: dict | None = None):
        self.status_code = status_code
        self._json_data = json_data or {}

    def raise_for_status(self) -> None:
        if 400 <= self.status_code:
            raise Exception(f"HTTP {self.status_code}")

    def json(self) -> dict:
        return self._json_data


@pytest.mark.asyncio
async def test_auth_login_sets_tokens_and_header(monkeypatch):
    """login() should store tokens and set Authorization header."""
    auth = AuthManager()

    async def fake_post(url: str, json: dict):
        assert url.endswith("/classic-models/api/auth/login/")
        # Ensure credentials passed through
        assert "username" in json and "password" in json
        return FakeResponse(
            200,
            {
                "access": "access-token",
                "refresh": "refresh-token",
                "user": {
                    "id": 1,
                    "username": json["username"],
                    "email": "user@example.com",
                    "first_name": "Test",
                    "last_name": "User",
                    "is_active": True,
                    "date_joined": "2024-01-01T00:00:00Z",
                },
            },
        )

    monkeypatch.setattr(auth.client, "post", fake_post)

    await auth.login()

    assert auth.access_token == "access-token"
    assert auth.refresh_token == "refresh-token"
    assert auth.client.headers["Authorization"] == "Bearer access-token"


@pytest.mark.asyncio
async def test_auth_refresh_access_token(monkeypatch):
    """refresh_access_token() should update tokens and header."""
    auth = AuthManager()
    auth.access_token = "old-access"
    auth.refresh_token = "old-refresh"

    async def fake_post(url: str, json: dict):
        assert url.endswith("/classic-models/api/auth/refresh/")
        assert json["refresh"] == "old-refresh"
        return FakeResponse(
            200,
            {
                "access": "new-access",
                "refresh": "new-refresh",
            },
        )

    monkeypatch.setattr(auth.client, "post", fake_post)

    await auth.refresh_access_token()

    assert auth.access_token == "new-access"
    assert auth.refresh_token == "new-refresh"
    assert auth.client.headers["Authorization"] == "Bearer new-access"


@pytest.mark.asyncio
async def test_auth_ensure_authenticated_calls_login(monkeypatch):
    """ensure_authenticated() should call login when no access token."""
    auth = AuthManager()
    called = {"login": False}

    async def fake_login():
        called["login"] = True

    monkeypatch.setattr(auth, "login", fake_login)

    await auth.ensure_authenticated()

    assert called["login"] is True


@pytest.mark.asyncio
async def test_auth_ensure_authenticated_skips_login_when_authenticated(monkeypatch):
    """ensure_authenticated() should not call login when already authenticated."""
    auth = AuthManager()
    auth.access_token = "existing-token"
    called = {"login": False}

    async def fake_login():
        called["login"] = True

    monkeypatch.setattr(auth, "login", fake_login)

    await auth.ensure_authenticated()

    assert called["login"] is False


@pytest.mark.asyncio
async def test_auth_login_handles_http_error(monkeypatch):
    """login() should raise exception on HTTP error."""
    import httpx
    auth = AuthManager()

    async def fake_post(url: str, json: dict):
        raise httpx.HTTPError("Connection error")

    monkeypatch.setattr(auth.client, "post", fake_post)

    with pytest.raises(Exception, match="Failed to login"):
        await auth.login()


@pytest.mark.asyncio
async def test_auth_refresh_access_token_no_refresh_token(monkeypatch):
    """refresh_access_token() should raise exception when no refresh token."""
    auth = AuthManager()
    auth.refresh_token = None

    with pytest.raises(Exception, match="No refresh token available"):
        await auth.refresh_access_token()


@pytest.mark.asyncio
async def test_auth_refresh_access_token_falls_back_to_login(monkeypatch):
    """refresh_access_token() should fall back to login on HTTP error."""
    import httpx
    auth = AuthManager()
    auth.refresh_token = "old-refresh"
    login_called = {"called": False}

    async def fake_post(url: str, json: dict):
        if "/refresh/" in url:
            raise httpx.HTTPError("HTTP error")
        return FakeResponse(200, {"access": "new-access", "refresh": "new-refresh"})

    async def fake_login():
        login_called["called"] = True
        auth.access_token = "new-access"
        auth.refresh_token = "new-refresh"

    monkeypatch.setattr(auth.client, "post", fake_post)
    monkeypatch.setattr(auth, "login", fake_login)

    await auth.refresh_access_token()

    assert login_called["called"] is True
    assert auth.access_token == "new-access"


@pytest.mark.asyncio
async def test_auth_get_headers_raises_when_not_authenticated():
    """get_headers() should raise exception when not authenticated."""
    auth = AuthManager()

    with pytest.raises(Exception, match="Not authenticated"):
        auth.get_headers()


@pytest.mark.asyncio
async def test_auth_get_headers_returns_headers_when_authenticated():
    """get_headers() should return Authorization header when authenticated."""
    auth = AuthManager()
    auth.access_token = "test-token"

    headers = auth.get_headers()

    assert headers == {"Authorization": "Bearer test-token"}


@pytest.mark.asyncio
async def test_auth_close_closes_client(monkeypatch):
    """close() should close the HTTP client."""
    auth = AuthManager()
    close_called = {"called": False}

    async def fake_aclose():
        close_called["called"] = True

    monkeypatch.setattr(auth.client, "aclose", fake_aclose)

    await auth.close()

    assert close_called["called"] is True



