"""Unit tests for configuration."""
import os

from src.config import Config


def test_config_defaults(monkeypatch):
    """Config should use sensible defaults when env vars are not set."""
    # Ensure env vars are unset
    monkeypatch.delenv("CLASSIC_MODELS_API_URL", raising=False)
    monkeypatch.delenv("API_USERNAME", raising=False)
    monkeypatch.delenv("API_PASSWORD", raising=False)
    monkeypatch.delenv("SSE_PORT", raising=False)
    monkeypatch.delenv("SSE_BEARER_TOKEN", raising=False)
    monkeypatch.delenv("TRANSPORT", raising=False)

    config = Config()

    assert config.api_url == "http://localhost:8000"
    assert config.api_username == "demo"
    assert config.api_password == "demo123"
    assert config.sse_port == 3000
    assert config.sse_bearer_token == "demo-token"
    assert config.transport == "stdio"


def test_config_env_overrides(monkeypatch):
    """Config should respect environment variable overrides."""
    monkeypatch.setenv("CLASSIC_MODELS_API_URL", "https://api.example.com/")
    monkeypatch.setenv("API_USERNAME", "user1")
    monkeypatch.setenv("API_PASSWORD", "secret")
    monkeypatch.setenv("SSE_PORT", "4000")
    monkeypatch.setenv("SSE_BEARER_TOKEN", "token123")
    monkeypatch.setenv("TRANSPORT", "sse")

    config = Config()

    # Trailing slash should be stripped
    assert config.api_url == "https://api.example.com"
    assert config.api_username == "user1"
    assert config.api_password == "secret"
    assert config.sse_port == 4000
    assert config.sse_bearer_token == "token123"
    assert config.transport == "sse"



