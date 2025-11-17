# Docker Setup Guide

> 📖 **Navigation:** [Documentation Index](README.md) | [Main README](../README.md)

Run the Classic Models MCP server in Docker containers.

---

## 🎯 Should You Use Docker?

| Scenario | Recommendation |
|---------|----------------|
| **Development (local)** | ❌ Use native Python instead |
| **Production deployment** | ✅ Docker is great |
| **Remote access (HTTP)** | ✅ Docker works perfectly |
| **Local stdio** | ⚠️ Possible but not recommended |

---

## ✅ Prerequisites

- ✅ Docker installed
- ✅ Docker Compose installed (optional but recommended)
- ✅ Classic Models API accessible

---

## 🚀 Quick Start (HTTP Mode - Recommended)

### 1. Build the Image

```bash
docker build -t classic-models-mcp .
```

### 2. Create `.env` File

```env
CLASSIC_MODELS_API_URL=http://host.docker.internal:8000
HTTP_PORT=3000
HTTP_BEARER_TOKEN=your-secret-token-here
```

### 3. Start with Docker Compose

```bash
docker-compose up -d classic-models-mcp-http
```

### 4. Connect Claude Desktop

```json
{
  "mcpServers": {
    "classic-models": {
      "url": "http://localhost:3000/mcp/",
      "headers": {
        "Authorization": "Bearer your-secret-token-here"
      }
    }
  }
}
```

**Done!** 🎉

---

## 📋 Detailed Setup

### Using Docker Compose (Recommended)

**1. Create `.env` file:**
```env
CLASSIC_MODELS_API_URL=http://host.docker.internal:8000
HTTP_PORT=3000
HTTP_BEARER_TOKEN=your-secret-token-here
API_USERNAME=demo
API_PASSWORD=demo123
```

**2. Start the service:**
```bash
docker-compose up -d classic-models-mcp-http
```

**3. Check status:**
```bash
docker-compose ps
docker-compose logs -f classic-models-mcp-http
```

**4. Stop the service:**
```bash
docker-compose down
```

### Using Docker Directly

**Build:**
```bash
docker build -t classic-models-mcp .
```

**Run:**
```bash
docker run -d \
  --name classic-models-mcp \
  -p 3000:3000 \
  -e CLASSIC_MODELS_API_URL=http://host.docker.internal:8000 \
  -e HTTP_PORT=3000 \
  -e HTTP_BEARER_TOKEN=demo-token \
  -e TRANSPORT=http \
  classic-models-mcp
```

**Stop:**
```bash
docker stop classic-models-mcp
docker rm classic-models-mcp
```

---

## 🌐 Networking

### Accessing Local API from Container

**macOS/Windows:**
```env
CLASSIC_MODELS_API_URL=http://host.docker.internal:8000
```

**Linux:**
```env
CLASSIC_MODELS_API_URL=http://172.17.0.1:8000
```

### Accessing Remote API

```env
CLASSIC_MODELS_API_URL=https://qnap-jiri.myqnapcloud.com
```

### Same Docker Network

If API is in the same Docker network:

```yaml
services:
  classic-models-mcp-http:
    networks:
      - mcp-network
    environment:
      - CLASSIC_MODELS_API_URL=http://api-service:8000
```

---

## ⚙️ Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CLASSIC_MODELS_API_URL` | `http://localhost:8000` | API base URL |
| `HTTP_PORT` | `3000` | HTTP server port |
| `HTTP_BEARER_TOKEN` | `demo-token` | Bearer token for HTTP |
| `TRANSPORT` | `stdio` | Transport mode (`http` for Docker) |
| `API_USERNAME` | `demo` | API username |
| `API_PASSWORD` | `demo123` | API password |

---

## 🔧 Troubleshooting

### ❌ Container Won't Start

**Check logs:**
```bash
docker-compose logs classic-models-mcp-http
```

**Common issues:**
- API URL not accessible from container
- Port already in use
- Missing environment variables

### ❌ Cannot Connect to API

**Test connectivity:**
```bash
docker exec classic-models-mcp-http curl http://host.docker.internal:8000
```

**Fix networking:**
- Use `host.docker.internal` (macOS/Windows)
- Use `172.17.0.1` (Linux)
- Or use service name if in same network

### ❌ HTTP Connection Refused

**Check:**
1. ✅ Container is running: `docker ps`
2. ✅ Port is exposed: `docker port classic-models-mcp-http`
3. ✅ Bearer token matches
4. ✅ Firewall allows connections

---

## 🐳 stdio Mode (Not Recommended)

**Can it work?** Yes, but it's complex and slow.

**How to use:**
```bash
docker run -it --rm \
  -e CLASSIC_MODELS_API_URL=http://host.docker.internal:8000 \
  -e TRANSPORT=stdio \
  classic-models-mcp
```

**Claude Desktop config:**
```json
{
  "mcpServers": {
    "classic-models": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "CLASSIC_MODELS_API_URL=http://host.docker.internal:8000",
        "-e", "TRANSPORT=stdio",
        "classic-models-mcp"
      ]
    }
  }
}
```

**Why not recommended:**
- ⚠️ Slower startup (container initialization)
- ⚠️ More complex configuration
- ⚠️ Less efficient than native Python
- ✅ Better: Use native Python for stdio, Docker for HTTP

---

## 🏭 Production Setup

### Example Production Configuration

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  classic-models-mcp:
    build:
      context: .
      dockerfile: Dockerfile
    image: classic-models-mcp:v1.0.0
    ports:
      - "3000:3000"
    environment:
      - CLASSIC_MODELS_API_URL=${CLASSIC_MODELS_API_URL}
      - HTTP_PORT=3000
      - HTTP_BEARER_TOKEN=${HTTP_BEARER_TOKEN}
      - TRANSPORT=http
    restart: always
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
    healthcheck:
      test: ["CMD", "python", "-c", "import sys; sys.exit(0)"]
      interval: 30s
      timeout: 10s
      retries: 3
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### Production Best Practices

1. **Use strong tokens:**
   ```bash
   HTTP_BEARER_TOKEN=$(openssl rand -hex 32)
   ```

2. **Use HTTPS:** Configure reverse proxy (nginx/traefik)

3. **Set resource limits:** Prevent resource exhaustion

4. **Enable health checks:** Monitor container health

5. **Configure logging:** Set up log rotation

6. **Use secrets:** Store credentials securely

---

## 📊 Comparison

| Aspect | Native Python | Docker HTTP | Docker stdio |
|--------|--------------|------------|--------------|
| **Setup** | ⭐ Easy | ⭐⭐ Medium | ⭐⭐⭐ Complex |
| **Performance** | ⭐⭐⭐ Best | ⭐⭐ Good | ⭐ Slower |
| **Isolation** | ❌ None | ✅ Full | ✅ Full |
| **Production** | ✅ Yes | ✅✅ Best | ❌ Not recommended |
| **Use Case** | Development | Production | Testing only |

---

## 📚 Related Documentation

- [Claude Desktop Configuration](CLAUDE_DESKTOP_CONFIG.md) - Connect Claude Desktop
- [Authentication Guide](AUTHENTICATION.md) - Understand authentication
- [Main README](../README.md) - Project overview

---

## 💡 Key Takeaways

1. **Use Docker for HTTP** - Perfect for production
2. **Use native Python for stdio** - Better for development
3. **HTTP is recommended** - Works great in containers
4. **stdio in Docker is possible** - But not recommended

---

**Need help?** Check [troubleshooting](#-troubleshooting) or see [Claude Desktop Configuration](CLAUDE_DESKTOP_CONFIG.md).
