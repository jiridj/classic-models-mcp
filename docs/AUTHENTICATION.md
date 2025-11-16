# Authentication Guide

> 📖 **Documentation Index:** [docs/README.md](README.md) | [Main README](../README.md)

This document explains how authentication is handled in the Classic Models MCP server.

## Overview

The MCP server uses **two separate authentication mechanisms**:

1. **API Authentication** - For authenticating with the Classic Models API (JWT-based)
2. **SSE Transport Authentication** - For securing remote access to the MCP server (Bearer token)

## API Authentication (Classic Models API)

### How It Works

The MCP server automatically authenticates with the Classic Models API using JWT tokens.

#### Authentication Flow

```
1. Server Startup
   ↓
2. Auto-login with credentials
   ↓
3. Receive JWT access + refresh tokens
   ↓
4. Store tokens in memory
   ↓
5. Use access token for all API requests
   ↓
6. Auto-refresh on 401 errors
```

#### Implementation Details

**Location:** `src/api/auth.py` - `AuthManager` class

**Credentials:**
- **Default:** `demo` / `demo123` (hardcoded)
- **Override:** Set `API_USERNAME` and `API_PASSWORD` environment variables

**Token Management:**
- Tokens stored **in memory only** (not persisted)
- Access token included in `Authorization: Bearer <token>` header
- Automatic refresh on 401 Unauthorized responses
- Falls back to re-login if refresh fails

**Code Flow:**

```python
# On startup (src/server.py)
api_client = APIClient()
await api_client.initialize()  # Calls ensure_authenticated()

# In AuthManager (src/api/auth.py)
async def ensure_authenticated(self):
    if not self.access_token:
        await self.login()  # POST /classic-models/api/auth/login/

# On each API request (src/api/client.py)
async def _request(...):
    await self.auth.ensure_authenticated()  # Ensure token exists
    headers = self.auth.get_headers()  # Get Authorization header
    
    # If 401, refresh and retry
    if response.status_code == 401:
        await self.auth.refresh_access_token()
        # Retry request with new token
```

### Configuration

**Environment Variables:**
```env
API_USERNAME=demo          # Default: "demo"
API_PASSWORD=demo123       # Default: "demo123"
CLASSIC_MODELS_API_URL=http://localhost:8000
```

**In Code:**
```python
# src/config.py
self.api_username = os.getenv("API_USERNAME", "demo")
self.api_password = os.getenv("API_PASSWORD", "demo123")
```

### Token Lifecycle

1. **Initial Login:**
   - POST `/classic-models/api/auth/login/`
   - Receives: `{access: "...", refresh: "...", user: {...}}`
   - Stores both tokens in memory

2. **Token Usage:**
   - Access token sent in `Authorization: Bearer <token>` header
   - Used for all API requests

3. **Token Refresh:**
   - Triggered automatically on 401 responses
   - POST `/classic-models/api/auth/refresh/` with refresh token
   - Receives new access + refresh tokens
   - Updates stored tokens

4. **Re-authentication:**
   - If refresh fails, automatically re-logins
   - Seamless to the user (happens in background)

### Security Considerations

**Current Implementation:**
- ✅ Credentials can be overridden via environment variables
- ✅ Tokens stored in memory (not persisted to disk)
- ✅ Automatic token refresh
- ⚠️ Default credentials are hardcoded (demo/demo123)
- ⚠️ No token persistence (tokens lost on restart)

**For Production:**
- Use environment variables or secrets management
- Consider token persistence for faster startup
- Use secure credential storage (e.g., Docker secrets, Kubernetes secrets)

## SSE Transport Authentication (MCP Server)

### How It Works

When using SSE transport, the MCP server requires a bearer token for remote access.

#### Authentication Flow

```
1. Client connects to SSE endpoint
   ↓
2. Client sends Authorization: Bearer <token> header
   ↓
3. FastMCP validates token
   ↓
4. If valid: Connection established
   If invalid: Connection rejected (401)
```

#### Implementation Details

**Location:** `src/server.py`

**Token Configuration:**
- **Default:** `demo-token` (hardcoded)
- **Override:** Set `SSE_BEARER_TOKEN` environment variable

**Code:**
```python
# src/server.py
from fastmcp.auth import BearerTokenAuth

if config.transport == "sse":
    auth = BearerTokenAuth(token=config.sse_bearer_token)
    mcp = FastMCP(..., auth=auth)
```

**Client Configuration:**
```json
{
  "mcpServers": {
    "classic-models": {
      "url": "http://localhost:3000/sse",
      "headers": {
        "Authorization": "Bearer demo-token"
      }
    }
  }
}
```

### Configuration

**Environment Variables:**
```env
SSE_BEARER_TOKEN=your-secret-token-here  # Default: "demo-token"
```

**In Code:**
```python
# src/config.py
self.sse_bearer_token = os.getenv("SSE_BEARER_TOKEN", "demo-token")
```

### Security Considerations

**Current Implementation:**
- ✅ Token can be overridden via environment variable
- ✅ Token required for SSE connections
- ⚠️ Default token is hardcoded ("demo-token")
- ⚠️ No token rotation or expiration

**For Production:**
- Use a strong, randomly generated token
- Store token securely (environment variables, secrets management)
- Consider token rotation mechanisms
- Use HTTPS for SSE transport

## Authentication Summary

| Aspect | API Authentication | SSE Transport Auth |
|--------|-------------------|-------------------|
| **Type** | JWT (access + refresh) | Bearer token |
| **Purpose** | Authenticate with Classic Models API | Secure MCP server access |
| **When Used** | All API requests | SSE transport only |
| **Default Creds** | demo/demo123 | demo-token |
| **Configurable** | ✅ API_USERNAME, API_PASSWORD | ✅ SSE_BEARER_TOKEN |
| **Token Storage** | In memory | N/A (validated per request) |
| **Auto-refresh** | ✅ Yes | N/A |
| **Location** | `src/api/auth.py` | `src/server.py` |

## Configuration Examples

### Development (Default Credentials)

```env
# .env file
CLASSIC_MODELS_API_URL=http://localhost:8000
TRANSPORT=stdio
# Uses default: demo/demo123 for API
# Uses default: demo-token for SSE (if used)
```

### Production (Custom Credentials)

```env
# .env file
CLASSIC_MODELS_API_URL=https://api.example.com
API_USERNAME=production-user
API_PASSWORD=secure-password-here
SSE_BEARER_TOKEN=$(openssl rand -hex 32)
SSE_PORT=3000
TRANSPORT=sse
```

### Docker

```yaml
# docker-compose.yml
environment:
  - CLASSIC_MODELS_API_URL=http://host.docker.internal:8000
  - API_USERNAME=${API_USERNAME}
  - API_PASSWORD=${API_PASSWORD}
  - SSE_BEARER_TOKEN=${SSE_BEARER_TOKEN}
  - TRANSPORT=sse
```

## Troubleshooting

### API Authentication Issues

**Problem: "Failed to login"**
- Check API is running and accessible
- Verify credentials are correct
- Check `CLASSIC_MODELS_API_URL` is correct

**Problem: "401 Unauthorized" on requests**
- Token may have expired
- Auto-refresh should handle this, but check logs
- Verify API credentials haven't changed

**Problem: Tokens not persisting**
- This is expected - tokens are in memory only
- Server will re-authenticate on restart

### SSE Authentication Issues

**Problem: "401 Unauthorized" on SSE connection**
- Verify `SSE_BEARER_TOKEN` matches client config
- Check token is included in Authorization header
- Ensure transport is set to "sse"

**Problem: Connection refused**
- Verify SSE server is running
- Check port is correct
- Verify firewall settings

## Future Improvements

Potential enhancements for production use:

1. **Token Persistence:**
   - Store tokens in secure file or database
   - Reduce re-authentication on restart

2. **Credential Management:**
   - Integration with secrets management systems
   - Support for credential rotation

3. **Enhanced Security:**
   - Token expiration and rotation
   - Rate limiting
   - Audit logging

4. **Multiple User Support:**
   - Per-request authentication
   - User context management

## Related Documentation

- [Configuration Guide](../README.md#configuration)
- [Docker Setup](DOCKER.md)
- [Claude Desktop Configuration](CLAUDE_DESKTOP_CONFIG.md)

