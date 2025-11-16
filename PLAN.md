# Classic Models MCP Server - Implementation Plan

## Overview
Build an MCP (Model Context Protocol) server that exposes the Classic Models API as MCP tools and resources, accessible both locally via stdio and remotely via SSE with bearer token authentication.

## API Analysis Summary

The Classic Models API provides:
- **Authentication**: JWT-based (login, logout, signup, refresh, get current user)
- **Data Resources**:
  - Product Lines (CRUD)
  - Products (CRUD)
  - Offices (CRUD)
  - Employees (CRUD)
  - Customers (CRUD)
  - Orders (CRUD)
  - Payments (CRUD)
  - Order Details (CRUD)

All data endpoints require JWT authentication via Bearer token.

## Architecture

### Transport Layers
1. **stdio** - For local access (default)
2. **SSE (Server-Sent Events)** - For remote access with bearer token auth

### Core Components

1. **MCP Server Core**
   - Handle MCP protocol messages (JSON-RPC 2.0)
   - Support both stdio and SSE transports
   - Manage authentication state

2. **API Client**
   - HTTP client for Classic Models API
   - JWT token management (login, refresh, storage)
   - Error handling and retry logic

3. **MCP Tools**
   - Map API endpoints to MCP tools
   - Each CRUD operation becomes a tool
   - No authentication tools needed (credentials hardcoded)

4. **MCP Resources**
   - Expose data as resources (optional, for read operations)
   - Enable resource discovery

5. **Authentication Middleware**
   - Bearer token validation for SSE transport
   - Token storage and management

## Implementation Plan

### Phase 1: Project Setup
- [ ] Initialize Node.js/TypeScript project
- [ ] Set up dependencies:
  - `fastmcp` - FastMCP library
  - `httpx` or `requests` - HTTP client
  - `python-dotenv` - Environment configuration
  - Python 3.12
- [ ] Create project structure
- [ ] Set up configuration management

### Phase 2: Core MCP Server (stdio)
- [ ] Implement base MCP server with stdio transport
- [ ] Create API client wrapper
- [ ] Implement auto-login with hardcoded credentials on startup
- [ ] Test stdio transport locally

### Phase 3: API Tools Implementation
- [ ] Auto-authenticate with hardcoded credentials on startup
- [ ] Create tool definitions for each resource:
  - Product Lines: list, get, create, update, delete
  - Products: list, get, create, update, delete
  - Offices: list, get, create, update, delete
  - Employees: list, get, create, update, delete
  - Customers: list, get, create, update, delete
  - Orders: list, get, create, update, delete
  - Payments: list, get, create, update, delete
  - Order Details: list, get, create, update, delete
- [ ] Implement tool handlers
- [ ] Add parameter validation
- [ ] Error handling

### Phase 4: SSE Transport
- [ ] Implement SSE server endpoint
- [ ] Add bearer token authentication middleware
- [ ] Bridge SSE to MCP protocol
- [ ] Handle connection management
- [ ] Test remote access

### Phase 5: Configuration & Deployment
- [ ] Environment variables:
  - `CLASSIC_MODELS_API_URL` - API base URL
  - `SSE_PORT` - Port for SSE server (default: 3000)
  - `SSE_BEARER_TOKEN` - Token for SSE authentication
  - `JWT_STORAGE_PATH` - Path to store JWT tokens (optional)
- [ ] CLI arguments for transport selection
- [ ] Documentation
- [ ] Example configurations

### Phase 6: Testing & Validation
- [ ] Unit tests for API client
- [ ] Integration tests for MCP tools
- [ ] Test stdio transport
- [ ] Test SSE transport with authentication
- [ ] End-to-end testing

## Project Structure

```
classic-models-mcp/
├── src/
│   ├── server.py              # Main entry point with FastMCP
│   ├── api/
│   │   ├── client.py          # API HTTP client
│   │   ├── auth.py            # Authentication logic
│   │   └── types.py            # Python types/dataclasses
│   ├── tools/
│   │   ├── __init__.py        # Tool registry
│   │   ├── productlines.py
│   │   ├── products.py
│   │   ├── offices.py
│   │   ├── employees.py
│   │   ├── customers.py
│   │   ├── orders.py
│   │   ├── payments.py
│   │   └── orderdetails.py
│   └── config.py              # Configuration management
├── tests/
├── requirements.txt
├── pyproject.toml
├── .env.example
└── README.md
```

## Technical Decisions

### Language: Python 3.12 with FastMCP
- FastMCP provides easy MCP server implementation
- Python has excellent HTTP client libraries (requests, httpx)
- Good SSE support with FastAPI/Starlette

### Authentication Strategy
- **For API calls**: Hardcode demo credentials (username: `demo`, password: `demo123`)
- Auto-login on startup and store JWT token in memory
- Support token refresh automatically when expired
- **For SSE transport**: Use bearer token in Authorization header

### Tool Naming Convention
- `classic_models_list_{resource}` - List operations
- `classic_models_get_{resource}` - Get single item
- `classic_models_create_{resource}` - Create operations
- `classic_models_update_{resource}` - Update operations
- `classic_models_delete_{resource}` - Delete operations
- (No auth tools - credentials hardcoded, auto-login on startup)

### Error Handling
- Map HTTP errors to MCP errors
- Provide clear error messages
- Handle authentication failures gracefully

## Configuration Example

### .env
```env
CLASSIC_MODELS_API_URL=http://localhost:8000
SSE_PORT=3000
SSE_BEARER_TOKEN=your-secret-token-here
JWT_STORAGE_PATH=.tokens.json
```

### Usage

**stdio mode (local):**
```bash
node dist/server.js --transport stdio
```

**SSE mode (remote):**
```bash
node dist/server.js --transport sse --port 3000
```

## Next Steps

1. Review and approve this plan
2. Set up project structure
3. Begin Phase 1 implementation
4. Iterate through phases with testing

