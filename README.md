# Classic Models MCP Server

An MCP (Model Context Protocol) server that exposes the Classic Models API as MCP tools, accessible both locally via stdio and remotely via SSE with bearer token authentication.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run server (stdio mode)
python -m src.server
```

See [Configuration](#configuration) and [Documentation](#documentation) sections below for detailed setup instructions.

## Features

- **37 MCP Tools** covering all Classic Models API resources
- **Dual Transport Support**: stdio (local) or SSE (remote)
- **Bearer Token Authentication** for secure remote access
- **Auto-authentication** with demo credentials
- **LLM-Optimized Documentation** for all tools

## Installation

### Prerequisites

- Python 3.12 or higher
- Classic Models API running (local or remote)

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or using `uv`:

```bash
uv pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root (or use environment variables):

```env
CLASSIC_MODELS_API_URL=http://localhost:8000
SSE_PORT=3000
SSE_BEARER_TOKEN=your-secret-token-here
TRANSPORT=stdio  # or "sse"
```

### Environment Variables

- `CLASSIC_MODELS_API_URL` - Base URL for the Classic Models API (default: `http://localhost:8000`)
- `SSE_PORT` - Port for SSE server (default: `3000`)
- `SSE_BEARER_TOKEN` - Bearer token for SSE authentication (default: `demo-token`)
- `TRANSPORT` - Transport mode: `stdio` or `sse` (default: `stdio`)
- `API_USERNAME` - API username (default: `demo`)
- `API_PASSWORD` - API password (default: `demo123`)

## Usage

### Running the Server

**Option 1: Native Python (Recommended for Development)**

**Local Access (stdio):**
```bash
python -m src.server
# Or explicitly:
TRANSPORT=stdio python -m src.server
```

**Remote Access (SSE):**
```bash
TRANSPORT=sse python -m src.server
# Server starts on port 3000 (or SSE_PORT from .env)
```

**Option 2: Docker (Recommended for Production)**

**SSE Mode:**
```bash
docker-compose up -d classic-models-mcp-sse
```

**Build and Run:**
```bash
docker build -t classic-models-mcp .
docker run -d -p 3000:3000 \
  -e CLASSIC_MODELS_API_URL=http://host.docker.internal:8000 \
  -e TRANSPORT=sse \
  classic-models-mcp
```

See [Docker Setup Guide](docs/DOCKER.md) for complete Docker instructions.

### Connecting Claude Desktop

For detailed Claude Desktop configuration instructions, see the [Claude Desktop Configuration Guide](docs/CLAUDE_DESKTOP_CONFIG.md).

**Quick Start (stdio):**

1. Add to Claude Desktop config file:
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

2. Restart Claude Desktop

See [docs/CLAUDE_DESKTOP_CONFIG.md](docs/CLAUDE_DESKTOP_CONFIG.md) for complete setup instructions including SSE configuration.

## API Resources

The server provides **37 tools** covering all CRUD operations for:

| Resource | Tools | Operations |
|----------|-------|------------|
| **Product Lines** | 5 | List, Get, Create, Update, Delete |
| **Products** | 5 | List, Get, Create, Update, Delete |
| **Offices** | 5 | List, Get, Create, Update, Delete |
| **Employees** | 5 | List, Get, Create, Update, Delete |
| **Customers** | 5 | List, Get, Create, Update, Delete |
| **Orders** | 5 | List, Get, Create, Update, Delete |
| **Payments** | 2 | Get, Update |
| **Order Details** | 5 | List, Get, Create, Update, Delete |

## Tool Naming Convention

Tools follow the pattern: `classic_models_{operation}_{resource}`

**Examples:**
- `classic_models_list_products` - List all products
- `classic_models_get_product` - Get a specific product
- `classic_models_create_product` - Create a new product
- `classic_models_update_product` - Update a product
- `classic_models_delete_product` - Delete a product

## Documentation

Comprehensive documentation is available in the [`docs/`](docs/) directory:

- **[Tools Reference](docs/TOOLS.md)**  
  Complete documentation for all 37 tools with parameters, examples, and use cases.

- **[Claude Desktop Configuration](docs/CLAUDE_DESKTOP_CONFIG.md)**  
  Step-by-step guide for configuring Claude Desktop via stdio or SSE.

- **[Docker Setup](docs/DOCKER.md)**  
  Guide for running the server in Docker (SSE recommended, stdio possible).

- **[Tool Documentation Guide](docs/TOOL_DOCUMENTATION_GUIDE.md)**  
  Best practices for writing LLM-friendly tool documentation.

- **[Documentation Index](docs/README.md)**  
  Overview of all available documentation.

## API Reference

This MCP server connects to the [Classic Models API](https://github.com/jiridj/classic-models-api), which provides a RESTful API for the Classic Models tutorial database.

- **Local API:** `http://localhost:8000/classic-models/api/schema/`
- **Public API:** `https://qnap-jiri.myqnapcloud.com/classic-models/api/schema/`

## Development

### Project Structure

```
classic-models-mcp/
├── src/
│   ├── server.py          # Main MCP server
│   ├── config.py          # Configuration management
│   ├── api/
│   │   ├── client.py      # API HTTP client
│   │   ├── auth.py        # Authentication manager
│   │   └── types.py       # Type definitions
│   └── tools/             # MCP tool implementations
│       ├── productlines.py
│       ├── products.py
│       ├── offices.py
│       ├── employees.py
│       ├── customers.py
│       ├── orders.py
│       ├── payments.py
│       └── orderdetails.py
├── docs/                   # Documentation
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

### Adding New Tools

1. Create a new tool file in `src/tools/`
2. Follow the [Tool Documentation Guide](docs/TOOL_DOCUMENTATION_GUIDE.md)
3. Register the tool in `src/server.py`
4. Update [docs/TOOLS.md](docs/TOOLS.md) with documentation

### Code Style

- Follow Python 3.12+ type hints
- Use async/await for all API calls
- Document all tools following the [Tool Documentation Guide](docs/TOOL_DOCUMENTATION_GUIDE.md)
- Include error handling and validation

## License

MIT

## Support

For issues, questions, or contributions:
- **API Issues:** [Classic Models API Repository](https://github.com/jiridj/classic-models-api)
- **MCP Server Issues:** Open an issue in this repository
