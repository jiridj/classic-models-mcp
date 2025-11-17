# Classic Models MCP Server

> **An MCP server that connects Claude Desktop to the Classic Models API**  
> Provides 37 tools for managing products, customers, orders, and more.

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🚀 Quick Start

Get up and running in 3 steps:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure (optional - uses defaults)
# Edit .env file or set environment variables

# 3. Run the server
python -m src.server
```

**Next:** [Connect Claude Desktop](docs/CLAUDE_DESKTOP_CONFIG.md) to start using the tools.

---

## ✨ What This Does

This MCP server acts as a bridge between **Claude Desktop** and the **Classic Models API**, giving you access to:

- 📦 **Products** - Manage product catalog
- 👥 **Customers** - Handle customer records
- 📋 **Orders** - Process and track orders
- 🏢 **Offices** - Manage office locations
- 👔 **Employees** - Employee management
- 💰 **Payments** - Payment tracking
- And more...

**37 tools total** covering all CRUD operations for 8 resource types.

---

## 📋 Table of Contents

- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Server](#-running-the-server)
- [Connecting Claude Desktop](#-connecting-claude-desktop)
- [Available Tools](#-available-tools)
- [Documentation](#-documentation)
- [Development](#-development)

---

## 📦 Installation

### Requirements

- **Python 3.12+** - [Download Python](https://www.python.org/downloads/)
- **Classic Models API** - Running locally or remotely
  - Local: `http://localhost:8000`
  - Remote: `https://qnap-jiri.myqnapcloud.com`

### Install Dependencies

**Option 1: Using Virtual Environment (Recommended)**

```bash
# Create virtual environment
python3.12 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Option 2: Global Installation**

```bash
pip install -r requirements.txt
```

**Option 3: Using `uv` (Faster)**

```bash
uv pip install -r requirements.txt
```

> 💡 **Tip:** Always activate the virtual environment before running the server or tests!

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# API Connection
CLASSIC_MODELS_API_URL=http://localhost:8000

# HTTP Server (for remote access)
HTTP_PORT=3000
HTTP_BEARER_TOKEN=your-secret-token-here

# Transport Mode
TRANSPORT=stdio  # or "http"

# API Credentials (optional - defaults to demo/demo123)
API_USERNAME=demo
API_PASSWORD=demo123
```

### Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `CLASSIC_MODELS_API_URL` | `http://localhost:8000` | Classic Models API base URL |
| `TRANSPORT` | `stdio` | Transport mode: `stdio` or `http` |
| `HTTP_PORT` | `3000` | Port for HTTP server |
| `HTTP_BEARER_TOKEN` | `demo-token` | Bearer token for HTTP authentication |
| `API_USERNAME` | `demo` | API username |
| `API_PASSWORD` | `demo123` | API password |

> 💡 **Tip:** For development, you can skip the `.env` file - defaults work fine!

---

## 🏃 Running the Server

### Option 1: Native Python (Recommended for Development)

**stdio mode** (local, default):
```bash
python -m src.server
```

**HTTP mode** (remote access):
```bash
TRANSPORT=http python -m src.server
```

### Option 2: Docker (Recommended for Production)

**Quick start:**
```bash
docker-compose up -d classic-models-mcp-http
```

**Full guide:** [Docker Setup](docs/DOCKER.md)

---

## 🔌 Connecting Claude Desktop

### Quick Setup (stdio)

1. **Open Claude Desktop config:**
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

2. **Add this configuration:**
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

3. **Restart Claude Desktop**

📖 **Full guide:** [Claude Desktop Configuration](docs/CLAUDE_DESKTOP_CONFIG.md)

---

## 🛠️ Available Tools

The server provides **37 tools** organized by resource:

| Resource | Tools | What You Can Do |
|----------|-------|----------------|
| **Products** | 5 | List, get, create, update, delete products |
| **Product Lines** | 5 | Manage product categories |
| **Customers** | 5 | Handle customer records |
| **Orders** | 5 | Process and track orders |
| **Order Details** | 5 | Manage order line items |
| **Employees** | 5 | Employee management |
| **Offices** | 5 | Office location management |
| **Payments** | 2 | View and update payments |

### Tool Naming Pattern

All tools follow this pattern: `classic_models_{operation}_{resource}`

**Examples:**
- `classic_models_list_products` - Get all products
- `classic_models_get_product` - Get one product
- `classic_models_create_product` - Add a new product
- `classic_models_update_product` - Modify a product
- `classic_models_delete_product` - Remove a product

📖 **Complete reference:** [Tools Documentation](docs/TOOLS.md)

---

## 📚 Documentation

All documentation is in the [`docs/`](docs/) folder:

| Guide | Description |
|-------|-------------|
| [**Tools Reference**](docs/TOOLS.md) | Complete documentation for all 37 tools |
| [**Claude Desktop Setup**](docs/CLAUDE_DESKTOP_CONFIG.md) | Step-by-step Claude Desktop configuration |
| [**Docker Guide**](docs/DOCKER.md) | Running in Docker containers |
| [**Authentication**](docs/AUTHENTICATION.md) | How authentication works |
| [**Documentation Index**](docs/README.md) | Overview of all docs |

---

## 🔗 API Reference

This MCP server connects to the **Classic Models API**:

- **Repository:** [jiridj/classic-models-api](https://github.com/jiridj/classic-models-api)
- **Local API Schema:** `http://localhost:8000/classic-models/api/schema/`
- **Public API Schema:** `https://qnap-jiri.myqnapcloud.com/classic-models/api/schema/`

---

## 💻 Development

### Project Structure

```
classic-models-mcp/
├── src/
│   ├── server.py          # Main MCP server entry point
│   ├── config.py          # Configuration management
│   ├── api/
│   │   ├── client.py      # HTTP client for API calls
│   │   ├── auth.py        # JWT authentication
│   │   └── types.py       # Type definitions
│   └── tools/             # MCP tool implementations
│       ├── products.py
│       ├── customers.py
│       └── ... (6 more)
├── docs/                  # Documentation
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

### Adding New Tools

1. Create tool file in `src/tools/`
2. Follow [Tool Documentation Guide](docs/TOOL_DOCUMENTATION_GUIDE.md)
3. Register in `src/server.py`
4. Update [docs/TOOLS.md](docs/TOOLS.md)

### Code Style

- Python 3.12+ type hints
- Async/await for API calls
- Comprehensive docstrings (see [Tool Documentation Guide](docs/TOOL_DOCUMENTATION_GUIDE.md))
- Error handling and validation

---

## ❓ Getting Help

- **Documentation:** Check the [docs/](docs/) folder
- **API Issues:** [Classic Models API Repository](https://github.com/jiridj/classic-models-api)
- **MCP Server Issues:** Open an issue in this repository

---

## 📄 License

MIT License - see LICENSE file for details

---

## 🙏 Acknowledgments

- Built with [FastMCP](https://github.com/jlowin/fastmcp)
- Connects to [Classic Models API](https://github.com/jiridj/classic-models-api)
- Uses the Classic Models tutorial database
