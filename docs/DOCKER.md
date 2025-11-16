# Docker Setup Guide

This guide explains how to run the Classic Models MCP server in Docker containers, covering both SSE (recommended) and stdio transport modes.

> 📖 **Documentation Index:** [docs/README.md](README.md) | [Main README](../README.md)

## Overview

### SSE Transport (Recommended for Docker)

**✅ Recommended** - SSE transport works excellently in Docker:
- Standard web service pattern
- Easy port exposure
- Simple networking
- Production-ready

### stdio Transport (Possible but Complex)

**⚠️ Possible but not recommended** - stdio transport can work in Docker but:
- Requires running Docker as a command from Claude Desktop
- More complex configuration
- Slower startup (container initialization)
- Less efficient than native Python execution
- Better suited for local development without Docker

## Prerequisites

- Docker and Docker Compose installed
- Classic Models API accessible (local or remote)
- For stdio: Docker image built and available

## Quick Start (SSE - Recommended)

### 1. Build the Docker Image

```bash
docker build -t classic-models-mcp .
```

### 2. Run with Docker Compose

Create a `.env` file:

```env
CLASSIC_MODELS_API_URL=http://host.docker.internal:8000
SSE_PORT=3000
SSE_BEARER_TOKEN=your-secret-token-here
API_USERNAME=demo
API_PASSWORD=demo123
```

Start the service:

```bash
docker-compose up -d classic-models-mcp-sse
```

### 3. Configure Claude Desktop

Add to Claude Desktop config:

```json
{
  "mcpServers": {
    "classic-models-docker": {
      "url": "http://localhost:3000/sse",
      "headers": {
        "Authorization": "Bearer your-secret-token-here"
      }
    }
  }
}
```

### 4. Verify

Check logs:

```bash
docker-compose logs -f classic-models-mcp-sse
```

## Docker Compose Configuration

The `docker-compose.yml` file provides two services:

### SSE Service (Default)

```yaml
classic-models-mcp-sse:
  - Exposes port 3000
  - Runs in SSE mode
  - Auto-restarts on failure
  - Health checks enabled
```

**Start:**
```bash
docker-compose up -d classic-models-mcp-sse
```

### stdio Service (For Testing)

```yaml
classic-models-mcp-stdio:
  - Runs in stdio mode
  - Requires --profile stdio to start
  - Interactive mode enabled
```

**Start:**
```bash
docker-compose --profile stdio up -d classic-models-mcp-stdio
```

## Manual Docker Commands

### SSE Mode

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
  -e SSE_PORT=3000 \
  -e SSE_BEARER_TOKEN=demo-token \
  -e TRANSPORT=sse \
  classic-models-mcp
```

**Stop:**
```bash
docker stop classic-models-mcp
docker rm classic-models-mcp
```

### stdio Mode (Not Recommended)

**Run:**
```bash
docker run -it --rm \
  -e CLASSIC_MODELS_API_URL=http://host.docker.internal:8000 \
  -e TRANSPORT=stdio \
  classic-models-mcp
```

**Configure Claude Desktop for stdio Docker:**

```json
{
  "mcpServers": {
    "classic-models-docker-stdio": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e", "CLASSIC_MODELS_API_URL=http://host.docker.internal:8000",
        "-e", "TRANSPORT=stdio",
        "classic-models-mcp"
      ]
    }
  }
}
```

**⚠️ Note:** This is slower and more complex than running Python directly. Only use if you have specific requirements for containerization.

## Environment Variables

### Required

- `CLASSIC_MODELS_API_URL` - API base URL
  - Local API: `http://host.docker.internal:8000`
  - Remote API: `https://your-api-server.com`

### SSE-Specific

- `SSE_PORT` - Port for SSE server (default: 3000)
- `SSE_BEARER_TOKEN` - Bearer token for authentication
- `TRANSPORT=sse` - Transport mode

### Optional

- `API_USERNAME` - API username (default: demo)
- `API_PASSWORD` - API password (default: demo123)

## Networking

### Accessing Local API from Container

If your Classic Models API runs on the host machine:

**Linux:**
```env
CLASSIC_MODELS_API_URL=http://172.17.0.1:8000
```

**macOS/Windows:**
```env
CLASSIC_MODELS_API_URL=http://host.docker.internal:8000
```

### Accessing Remote API

```env
CLASSIC_MODELS_API_URL=https://qnap-jiri.myqnapcloud.com
```

### Docker Network

If running API in the same Docker network:

```yaml
services:
  classic-models-mcp-sse:
    networks:
      - mcp-network
    environment:
      - CLASSIC_MODELS_API_URL=http://api-service:8000
```

## Production Considerations

### Security

1. **Change Default Bearer Token:**
   ```env
   SSE_BEARER_TOKEN=$(openssl rand -hex 32)
   ```

2. **Use HTTPS:** Configure reverse proxy (nginx/traefik) for HTTPS

3. **Network Isolation:** Use Docker networks to isolate services

4. **Non-root User:** The Dockerfile already runs as non-root user

### Performance

1. **Resource Limits:**
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '0.5'
         memory: 512M
   ```

2. **Health Checks:** Already configured in docker-compose.yml

3. **Restart Policy:** Set to `unless-stopped` for auto-recovery

### Monitoring

**View Logs:**
```bash
docker-compose logs -f classic-models-mcp-sse
```

**Check Status:**
```bash
docker-compose ps
```

**Health Check:**
```bash
docker inspect --format='{{.State.Health.Status}}' classic-models-mcp-sse
```

## Troubleshooting

### Container Won't Start

**Check logs:**
```bash
docker-compose logs classic-models-mcp-sse
```

**Common issues:**
- API URL not accessible from container
- Port already in use
- Missing environment variables

### Cannot Connect to API

**Test connectivity:**
```bash
docker exec classic-models-mcp-sse curl http://host.docker.internal:8000
```

**Verify API URL:**
- Use `host.docker.internal` for host API (macOS/Windows)
- Use `172.17.0.1` for host API (Linux)
- Use service name if in same Docker network

### SSE Connection Refused

**Check port exposure:**
```bash
docker port classic-models-mcp-sse
```

**Verify bearer token:**
- Token in Claude Desktop config must match `SSE_BEARER_TOKEN`

### stdio Mode Issues

**Container exits immediately:**
- Ensure `-i` (interactive) flag is used
- Check that stdin is properly connected

**Slow performance:**
- This is expected - stdio via Docker adds overhead
- Consider using SSE mode or native Python execution

## Comparison: Docker vs Native

| Aspect | Native Python | Docker SSE | Docker stdio |
|--------|--------------|------------|--------------|
| **Setup Complexity** | Low | Medium | High |
| **Performance** | Best | Good | Slower |
| **Isolation** | None | Full | Full |
| **Portability** | Requires Python | Works anywhere | Works anywhere |
| **Production Ready** | Yes | Yes | Not recommended |
| **Recommended Use** | Development | Production | Testing only |

## Best Practices

1. **Use SSE in Docker** - It's designed for containerized services
2. **Use Native Python for stdio** - Better performance for local development
3. **Build Images with Tags** - Use version tags for production
4. **Use .env Files** - Keep secrets out of docker-compose.yml
5. **Monitor Logs** - Set up log aggregation for production
6. **Health Checks** - Already configured, monitor them

## Example Production Setup

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
      - SSE_PORT=3000
      - SSE_BEARER_TOKEN=${SSE_BEARER_TOKEN}
      - TRANSPORT=sse
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
    networks:
      - mcp-network
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Claude Desktop Configuration](CLAUDE_DESKTOP_CONFIG.md)

