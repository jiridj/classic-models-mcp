# Claude Desktop Configuration Guide

> 📖 **Documentation Index:** [docs/README.md](README.md) | [Main README](../README.md)

This guide explains how to configure Claude Desktop to use the Classic Models MCP server via both stdio (local) and SSE (remote) transports.

## Prerequisites

1. **Python 3.12** installed and available in your PATH
2. **Classic Models MCP Server** installed and dependencies installed:
   ```bash
   pip install -r requirements.txt
   ```
3. **Classic Models API** running and accessible
   - Local: `http://localhost:8000`
   - Remote: `https://qnap-jiri.myqnapcloud.com`

## Configuration File Location

Claude Desktop stores MCP server configurations in a JSON file:

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

## Option 1: Local Access via stdio (Recommended for Development)

This configuration runs the MCP server locally and communicates via standard input/output.

### Step 1: Create or Edit Configuration File

Open the Claude Desktop configuration file in your editor:

```bash
# macOS
open ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Or edit manually
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

### Step 2: Add MCP Server Configuration

Add the Classic Models MCP server to the `mcpServers` section:

```json
{
  "mcpServers": {
    "classic-models": {
      "command": "python3.12",
      "args": [
        "-m",
        "src.server"
      ],
      "env": {
        "CLASSIC_MODELS_API_URL": "http://localhost:8000",
        "TRANSPORT": "stdio"
      },
      "cwd": "/Users/jiri/Development/classic-models/classic-models-mcp"
    }
  }
}
```

**Important:** Replace `/Users/jiri/Development/classic-models/classic-models-mcp` with the actual path to your project directory.

### Step 3: Alternative Configuration (Using Full Path)

If Python is not in your PATH, use the full path to Python:

```json
{
  "mcpServers": {
    "classic-models": {
      "command": "/usr/local/bin/python3.12",
      "args": [
        "-m",
        "src.server"
      ],
      "env": {
        "CLASSIC_MODELS_API_URL": "http://localhost:8000",
        "TRANSPORT": "stdio"
      },
      "cwd": "/Users/jiri/Development/classic-models/classic-models-mcp"
    }
  }
}
```

### Step 4: Using Virtual Environment

If you're using a virtual environment, point to the Python in that environment:

```json
{
  "mcpServers": {
    "classic-models": {
      "command": "/Users/jiri/Development/classic-models/classic-models-mcp/venv/bin/python",
      "args": [
        "-m",
        "src.server"
      ],
      "env": {
        "CLASSIC_MODELS_API_URL": "http://localhost:8000",
        "TRANSPORT": "stdio"
      },
      "cwd": "/Users/jiri/Development/classic-models/classic-models-mcp"
    }
  }
}
```

### Step 5: Restart Claude Desktop

After saving the configuration file, restart Claude Desktop completely for the changes to take effect.

---

## Option 2: Remote Access via SSE

This configuration connects to a remotely running MCP server via Server-Sent Events (SSE).

### Step 1: Start the SSE Server

First, start the MCP server in SSE mode on your server:

```bash
cd /path/to/classic-models-mcp
TRANSPORT=sse python3.12 -m src.server
```

The server will start on port 3000 by default (or the port specified in `SSE_PORT` environment variable).

### Step 2: Configure Claude Desktop

Add the SSE server configuration to Claude Desktop:

```json
{
  "mcpServers": {
    "classic-models-remote": {
      "url": "http://localhost:3000/sse",
      "headers": {
        "Authorization": "Bearer demo-token"
      }
    }
  }
}
```

**For remote server access:**

```json
{
  "mcpServers": {
    "classic-models-remote": {
      "url": "https://your-server.com:3000/sse",
      "headers": {
        "Authorization": "Bearer your-secret-token-here"
      }
    }
  }
}
```

### Step 3: Environment Variables for SSE Server

When starting the SSE server, set these environment variables:

```bash
export CLASSIC_MODELS_API_URL="http://localhost:8000"
export SSE_PORT=3000
export SSE_BEARER_TOKEN="your-secret-token-here"
export TRANSPORT=sse

python3.12 -m src.server
```

Or create a `.env` file:

```env
CLASSIC_MODELS_API_URL=http://localhost:8000
SSE_PORT=3000
SSE_BEARER_TOKEN=your-secret-token-here
TRANSPORT=sse
```

### Step 4: Restart Claude Desktop

After saving the configuration, restart Claude Desktop.

---

## Complete Configuration Example

Here's a complete example with both stdio and SSE configurations:

```json
{
  "mcpServers": {
    "classic-models-local": {
      "command": "python3.12",
      "args": [
        "-m",
        "src.server"
      ],
      "env": {
        "CLASSIC_MODELS_API_URL": "http://localhost:8000",
        "TRANSPORT": "stdio"
      },
      "cwd": "/Users/jiri/Development/classic-models/classic-models-mcp"
    },
    "classic-models-remote": {
      "url": "http://localhost:3000/sse",
      "headers": {
        "Authorization": "Bearer demo-token"
      }
    }
  }
}
```

---

## Verification

### Check Configuration Syntax

Ensure your JSON is valid. You can validate it using:

```bash
# macOS/Linux
python3 -m json.tool ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Or use an online JSON validator
```

### Test the Server Manually

Before configuring Claude Desktop, test the server manually:

**For stdio:**
```bash
cd /path/to/classic-models-mcp
TRANSPORT=stdio python3.12 -m src.server
```

**For SSE:**
```bash
cd /path/to/classic-models-mcp
TRANSPORT=sse python3.12 -m src.server
# Server should start and listen on port 3000
```

### Check Claude Desktop Logs

If the server doesn't appear in Claude Desktop:

1. Check Claude Desktop logs for errors
2. Verify the Python path is correct
3. Ensure all dependencies are installed
4. Check that the API server is running and accessible

---

## Troubleshooting

### Issue: Server Not Appearing in Claude Desktop

**Solutions:**
1. Verify JSON syntax is valid
2. Check that the `cwd` path is correct and absolute
3. Ensure Python 3.12 is in PATH or use full path
4. Restart Claude Desktop completely
5. Check Claude Desktop logs for error messages

### Issue: "Module not found" Errors

**Solutions:**
1. Install dependencies: `pip install -r requirements.txt`
2. Use a virtual environment and point to its Python
3. Verify the `cwd` is set to the project root

### Issue: "Connection refused" (SSE)

**Solutions:**
1. Verify the SSE server is running
2. Check the port number matches (default: 3000)
3. Verify firewall settings allow connections
4. Check the bearer token matches

### Issue: "Authentication failed"

**Solutions:**
1. Verify the API credentials (hardcoded as demo/demo123)
2. Check that the Classic Models API is running
3. Verify the `CLASSIC_MODELS_API_URL` is correct
4. Check API server logs for authentication errors

---

## Security Notes

### For Production Use

1. **Change Default Bearer Token:** Update `SSE_BEARER_TOKEN` to a strong, random token
2. **Use HTTPS:** For remote SSE access, use HTTPS instead of HTTP
3. **Restrict Access:** Configure firewall rules to limit access to the SSE port
4. **API Credentials:** The demo uses hardcoded credentials. For production, consider using environment variables or a secure credential store

### Environment Variables

You can override default credentials using environment variables:

```json
{
  "mcpServers": {
    "classic-models": {
      "command": "python3.12",
      "args": ["-m", "src.server"],
      "env": {
        "CLASSIC_MODELS_API_URL": "http://localhost:8000",
        "API_USERNAME": "your-username",
        "API_PASSWORD": "your-password",
        "TRANSPORT": "stdio"
      },
      "cwd": "/path/to/classic-models-mcp"
    }
  }
}
```

---

## Additional Resources

- [MCP Protocol Documentation](https://modelcontextprotocol.io)
- [Claude Desktop Documentation](https://claude.ai/docs)
- [Classic Models API Repository](https://github.com/jiridj/classic-models-api)

---

## Quick Reference

### stdio Configuration (Local)
```json
{
  "mcpServers": {
    "classic-models": {
      "command": "python3.12",
      "args": ["-m", "src.server"],
      "env": {
        "CLASSIC_MODELS_API_URL": "http://localhost:8000",
        "TRANSPORT": "stdio"
      },
      "cwd": "/absolute/path/to/classic-models-mcp"
    }
  }
}
```

### SSE Configuration (Remote)
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

