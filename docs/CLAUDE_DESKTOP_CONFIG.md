# Claude Desktop Configuration Guide

> 📖 **Navigation:** [Documentation Index](README.md) | [Main README](../README.md)

This guide shows you how to connect Claude Desktop to the Classic Models MCP server.

---

## 🎯 Choose Your Setup

| Setup | Best For | Difficulty |
|-------|----------|------------|
| **stdio (Local)** | Development, local use | ⭐ Easy |
| **HTTP (Remote)** | Remote access, production | ⭐⭐ Medium |

---

## ✅ Before You Start

Make sure you have:

- ✅ **Python 3.12+** installed
- ✅ **Dependencies installed:** `pip install -r requirements.txt`
- ✅ **Classic Models API** running (local or remote)

---

## 📍 Find Your Config File

Claude Desktop stores settings in a JSON file:

| Platform | Location |
|---------|----------|
| **macOS** | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Windows** | `%APPDATA%\Claude\claude_desktop_config.json` |
| **Linux** | `~/.config/Claude/claude_desktop_config.json` |

**Quick open (macOS):**
```bash
open ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

---

## 🖥️ Option 1: stdio (Local) - Recommended for Development

**What it does:** Runs the server on your computer and communicates directly.

### Step-by-Step Setup

#### 1. Open the Config File

Open the Claude Desktop config file in any text editor.

#### 2. Add This Configuration

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

> ⚠️ **Important:** Replace `/absolute/path/to/classic-models-mcp` with your actual project path.

**How to find your path:**
```bash
# In your project directory, run:
pwd
```

#### 3. Alternative: Full Python Path

If `python3.12` isn't in your PATH, use the full path:

```json
{
  "mcpServers": {
    "classic-models": {
      "command": "/usr/local/bin/python3.12",
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

#### 4. Using a Virtual Environment

If you use a virtual environment:

```json
{
  "mcpServers": {
    "classic-models": {
      "command": "/path/to/venv/bin/python",
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

#### 5. Restart Claude Desktop

**Important:** Fully quit and restart Claude Desktop for changes to take effect.

---

## 🌐 Option 2: HTTP (Remote) - For Remote Access

**What it does:** Connects to a server running elsewhere via Streamable HTTP.

### Step-by-Step Setup

#### 1. Start the HTTP Server

On the server machine, run:

```bash
cd /path/to/classic-models-mcp
TRANSPORT=http python3.12 -m src.server
```

The server starts on port 3000 (or your `HTTP_PORT` setting).

#### 2. Configure Claude Desktop

Add this to your Claude Desktop config:

**For local server:**
```json
{
  "mcpServers": {
    "classic-models": {
      "url": "http://localhost:3000/mcp/",
      "headers": {
        "Authorization": "Bearer demo-token"
      }
    }
  }
}
```

**For remote server:**
```json
{
  "mcpServers": {
    "classic-models": {
      "url": "https://your-server.com:3000/mcp/",
      "headers": {
        "Authorization": "Bearer your-secret-token"
      }
    }
  }
}
```

> ⚠️ **Important:** The bearer token must match `HTTP_BEARER_TOKEN` on the server.

#### 3. Configure Server Environment

On the server, set these environment variables:

```bash
export CLASSIC_MODELS_API_URL="http://localhost:8000"
export HTTP_PORT=3000
export HTTP_BEARER_TOKEN="your-secret-token-here"
export TRANSPORT=http
```

Or use a `.env` file:
```env
CLASSIC_MODELS_API_URL=http://localhost:8000
HTTP_PORT=3000
HTTP_BEARER_TOKEN=your-secret-token-here
TRANSPORT=http
```

#### 4. Restart Claude Desktop

Fully quit and restart Claude Desktop.

---

## ✅ Verify It Works

### Test the Server First

Before configuring Claude Desktop, test the server:

**stdio mode:**
```bash
cd /path/to/classic-models-mcp
TRANSPORT=stdio python3.12 -m src.server
```

**HTTP mode:**
```bash
cd /path/to/classic-models-mcp
TRANSPORT=http python3.12 -m src.server
# Should see: Server listening on port 3000
```

### Check Your JSON

Validate your config file:

```bash
# macOS/Linux
python3 -m json.tool ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

### In Claude Desktop

After restarting, you should see:
- The server appears in Claude Desktop
- Tools are available when chatting
- No error messages

---

## 🔧 Troubleshooting

### ❌ Server Not Appearing

**Check:**
1. ✅ JSON syntax is valid (use validator above)
2. ✅ `cwd` path is absolute and correct
3. ✅ Python path is correct
4. ✅ Restarted Claude Desktop completely
5. ✅ Check Claude Desktop logs for errors

**Find logs:**
- macOS: `~/Library/Logs/Claude/`
- Windows: `%APPDATA%\Claude\logs\`
- Linux: `~/.config/Claude/logs/`

### ❌ "Module not found" Error

**Fix:**
1. Install dependencies: `pip install -r requirements.txt`
2. Use virtual environment Python path
3. Verify `cwd` points to project root

### ❌ "Connection refused" (HTTP)

**Fix:**
1. Verify HTTP server is running
2. Check port matches (default: 3000)
3. Check firewall settings
4. Verify bearer token matches

### ❌ "Authentication failed"

**Fix:**
1. Check API is running
2. Verify `CLASSIC_MODELS_API_URL` is correct
3. Check API credentials (default: demo/demo123)
4. See [Authentication Guide](AUTHENTICATION.md) for details

---

## 🔒 Security Tips

### For Production

1. **Change default bearer token:**
   ```bash
   HTTP_BEARER_TOKEN=$(openssl rand -hex 32)
   ```

2. **Use HTTPS** for remote HTTP access

3. **Use environment variables** for credentials:
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

## 📋 Quick Reference

### stdio Configuration (Copy & Paste)

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

### HTTP Configuration (Copy & Paste)

```json
{
  "mcpServers": {
    "classic-models": {
      "url": "http://localhost:3000/mcp/",
      "headers": {
        "Authorization": "Bearer demo-token"
      }
    }
  }
}
```

---

## 📚 Related Guides

- [Authentication Guide](AUTHENTICATION.md) - Understand authentication
- [Docker Setup](DOCKER.md) - Run in Docker
- [Tools Reference](TOOLS.md) - See available tools

---

## 🔗 Additional Resources

- [MCP Protocol Docs](https://modelcontextprotocol.io)
- [Claude Desktop Docs](https://claude.ai/docs)
- [Classic Models API](https://github.com/jiridj/classic-models-api)

---

**Need help?** Check the [troubleshooting section](#-troubleshooting) or open an issue.
