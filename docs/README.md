# Classic Models MCP Server - Documentation

Welcome to the Classic Models MCP Server documentation. This directory contains comprehensive guides and references for using and developing with the MCP server.

## Documentation Index

### User Guides

- **[Claude Desktop Configuration](CLAUDE_DESKTOP_CONFIG.md)**  
  Step-by-step guide for configuring Claude Desktop to use this MCP server via stdio or SSE transport.

- **[Docker Setup](DOCKER.md)**  
  Guide for running the MCP server in Docker containers (SSE recommended, stdio possible).

- **[Authentication Guide](AUTHENTICATION.md)**  
  Explanation of how authentication works for both API and SSE transport.

- **[Tools Reference](TOOLS.md)**  
  Complete documentation for all 37 MCP tools, including parameters, examples, and use cases.

### Developer Guides

- **[Tool Documentation Guide](TOOL_DOCUMENTATION_GUIDE.md)**  
  Best practices for writing LLM-friendly tool documentation, including examples and templates.

## Quick Links

### Getting Started
1. [Installation](../README.md#installation) - Set up dependencies
2. [Configuration](../README.md#configuration) - Configure environment variables
3. [Claude Desktop Setup](CLAUDE_DESKTOP_CONFIG.md) - Connect Claude Desktop to the server

### Using Tools
1. [Tools Overview](TOOLS.md) - Browse all available tools
2. [Tool Naming Convention](../README.md#tool-naming-convention) - Understand tool naming patterns
3. [API Resources](../README.md#api-resources) - See what resources are available

### Development
1. [Project Structure](../README.md#development) - Understand the codebase
2. [Tool Documentation Guide](TOOL_DOCUMENTATION_GUIDE.md) - Learn how to document tools
3. [API Reference](https://github.com/jiridj/classic-models-api) - Classic Models API documentation

## Documentation Structure

```
docs/
├── README.md                    # This file - documentation index
├── CLAUDE_DESKTOP_CONFIG.md    # Claude Desktop setup guide
├── DOCKER.md                    # Docker setup and deployment guide
├── AUTHENTICATION.md            # Authentication and security guide
├── TOOLS.md                     # Complete tools reference
└── TOOL_DOCUMENTATION_GUIDE.md  # Developer documentation guide
```

## Contributing

When adding new tools or features:
1. Follow the [Tool Documentation Guide](TOOL_DOCUMENTATION_GUIDE.md) for consistent documentation
2. Update [TOOLS.md](TOOLS.md) with new tool documentation
3. Update this index if adding new documentation files

