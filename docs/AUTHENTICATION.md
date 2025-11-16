# Authentication Guide

> 📖 **Navigation:** [Documentation Index](README.md) | [Main README](../README.md)

This guide explains how authentication works in the Classic Models MCP server.

---

## 🎯 Two Types of Authentication

The MCP server uses **two separate authentication systems**:

| Type | Purpose | When Used |
|------|---------|-----------|
| **API Authentication** | Connect to Classic Models API | Always (for all API calls) |
| **SSE Transport Auth** | Secure remote MCP server access | Only when using SSE transport |

---

## 🔐 API Authentication (Classic Models API)

**What it does:** Authenticates the MCP server with the Classic Models API using JWT tokens.

### How It Works

```
┌─────────────────┐
│ Server Starts   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Auto-login      │ ← Uses credentials (demo/demo123)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Get JWT Tokens  │ ← Receives access + refresh tokens
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Store in Memory │ ← Tokens kept in memory
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Use for Requests│ ← Access token in Authorization header
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Auto-refresh    │ ← On 401 errors, refresh token
└─────────────────┘
```

### Credentials

**Default (for demo):**
- Username: `demo`
- Password: `demo123`

**Override with environment variables:**
```env
API_USERNAME=your-username
API_PASSWORD=your-password
```

### Token Management

| Aspect | Details |
|--------|---------|
| **Storage** | In memory only (not saved to disk) |
| **Refresh** | Automatic on 401 errors |
| **Fallback** | Re-login if refresh fails |
| **Header** | `Authorization: Bearer <access_token>` |

### Configuration

**Environment variables:**
```env
CLASSIC_MODELS_API_URL=http://localhost:8000
API_USERNAME=demo          # Optional (default: "demo")
API_PASSWORD=demo123       # Optional (default: "demo123")
```

**In code:**
- Location: `src/api/auth.py` - `AuthManager` class
- Auto-login: Happens on server startup
- Auto-refresh: Happens automatically on 401 errors

### Token Lifecycle

1. **Login** → Get access + refresh tokens
2. **Use** → Access token sent with every API request
3. **Refresh** → Automatically refresh when token expires
4. **Re-login** → If refresh fails, login again

**You don't need to do anything** - it all happens automatically!

---

## 🔒 SSE Transport Authentication (MCP Server)

**What it does:** Secures remote access to the MCP server when using SSE transport.

### How It Works

```
┌──────────────┐
│ Client       │
│ Connects     │
└──────┬───────┘
       │
       │ Sends: Authorization: Bearer <token>
       ▼
┌──────────────┐
│ MCP Server   │
│ Validates    │ ← Checks token matches
└──────┬───────┘
       │
       ├─ Valid → Connection allowed ✅
       │
       └─ Invalid → Connection rejected ❌ (401)
```

### Configuration

**Default token:** `demo-token`

**Override:**
```env
SSE_BEARER_TOKEN=your-secret-token-here
```

**Client configuration:**
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

> ⚠️ **Important:** The token in Claude Desktop config must match `SSE_BEARER_TOKEN` on the server.

### When Is It Used?

- ✅ **SSE transport** - Required
- ❌ **stdio transport** - Not used (local only)

---

## 📊 Quick Comparison

| Feature | API Authentication | SSE Transport Auth |
|---------|-------------------|-------------------|
| **Type** | JWT (access + refresh) | Bearer token |
| **Purpose** | Authenticate with API | Secure MCP server |
| **When** | All API requests | SSE connections only |
| **Default** | demo/demo123 | demo-token |
| **Config** | `API_USERNAME`, `API_PASSWORD` | `SSE_BEARER_TOKEN` |
| **Storage** | In memory | N/A (validated per request) |
| **Auto-refresh** | ✅ Yes | N/A |

---

## ⚙️ Configuration Examples

### Development (Default)

```env
# .env file
CLASSIC_MODELS_API_URL=http://localhost:8000
TRANSPORT=stdio
# Uses defaults: demo/demo123 for API
# Uses default: demo-token for SSE (if used)
```

### Production (Custom)

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

---

## 🔧 Troubleshooting

### ❌ "Failed to login"

**Check:**
1. ✅ API is running and accessible
2. ✅ Credentials are correct
3. ✅ `CLASSIC_MODELS_API_URL` is correct

**Test:**
```bash
curl http://localhost:8000/classic-models/api/auth/login/ \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"demo123"}'
```

### ❌ "401 Unauthorized" on API requests

**This should auto-fix:**
- Server automatically refreshes token on 401
- If refresh fails, it re-logins automatically

**If it persists:**
- Check API credentials haven't changed
- Verify API is still running
- Check server logs

### ❌ "401 Unauthorized" on SSE connection

**Check:**
1. ✅ `SSE_BEARER_TOKEN` matches client config
2. ✅ Token is in Authorization header
3. ✅ Transport is set to "sse"

**Verify:**
```bash
# On server
echo $SSE_BEARER_TOKEN

# In Claude Desktop config
# Should match the token above
```

### ❌ Tokens not persisting

**This is expected:**
- Tokens are stored in memory only
- Server re-authenticates on restart
- This is by design for security

---

## 🔒 Security Best Practices

### For Production

1. **Use strong tokens:**
   ```bash
   # Generate secure token
   SSE_BEARER_TOKEN=$(openssl rand -hex 32)
   ```

2. **Use environment variables:**
   - Don't hardcode credentials
   - Use secrets management (Docker secrets, Kubernetes secrets, etc.)

3. **Use HTTPS:**
   - For remote SSE access
   - Protects token in transit

4. **Rotate tokens:**
   - Change bearer tokens periodically
   - Update credentials if compromised

### Current Security Status

| Aspect | Status | Notes |
|--------|--------|-------|
| **Default credentials** | ⚠️ Hardcoded | OK for demo, change for production |
| **Token storage** | ✅ In memory | Secure, but lost on restart |
| **Auto-refresh** | ✅ Enabled | Handles token expiration |
| **HTTPS support** | ⚠️ Manual setup | Configure reverse proxy for production |

---

## 📚 Related Documentation

- [Claude Desktop Configuration](CLAUDE_DESKTOP_CONFIG.md) - How to configure authentication
- [Docker Setup](DOCKER.md) - Running with authentication in Docker
- [Main README](../README.md) - Configuration overview

---

## 💡 Key Takeaways

1. **API authentication is automatic** - You don't need to do anything
2. **SSE authentication requires matching tokens** - Token in client must match server
3. **Defaults work for development** - Change for production
4. **Tokens are in memory** - They don't persist across restarts (by design)

---

**Questions?** Check the [troubleshooting section](#-troubleshooting) or see [Claude Desktop Configuration](CLAUDE_DESKTOP_CONFIG.md).
