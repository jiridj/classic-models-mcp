# Documentation Index

> Welcome to the Classic Models MCP Server documentation

This directory contains all guides and references for using and developing with the MCP server.

---

## 📖 Quick Navigation

### 🚀 Getting Started

| Guide | When to Use |
|-------|-------------|
| **[Claude Desktop Setup](CLAUDE_DESKTOP_CONFIG.md)** | Setting up Claude Desktop to use the server |
| **[Docker Setup](DOCKER.md)** | Running the server in Docker |
| **[Authentication Guide](AUTHENTICATION.md)** | Understanding how authentication works |

### 📚 Reference

| Guide | What's Inside |
|-------|---------------|
| **[Tools Reference](TOOLS.md)** | Complete documentation for all 37 tools |
| **[Tool Documentation Guide](TOOL_DOCUMENTATION_GUIDE.md)** | How to write tool documentation |

---

## 📋 Documentation Overview

### User Guides

#### [Claude Desktop Configuration](CLAUDE_DESKTOP_CONFIG.md)
**Step-by-step guide for connecting Claude Desktop to the MCP server**

- ✅ stdio transport setup (local)
- ✅ SSE transport setup (remote)
- ✅ Configuration examples
- ✅ Troubleshooting

**Start here if:** You want to use the server with Claude Desktop

---

#### [Docker Setup](DOCKER.md)
**Guide for running the server in Docker containers**

- ✅ Dockerfile and docker-compose setup
- ✅ SSE mode (recommended)
- ✅ stdio mode (possible but not recommended)
- ✅ Production considerations

**Start here if:** You want to deploy the server in Docker

---

#### [Authentication Guide](AUTHENTICATION.md)
**How authentication works in the MCP server**

- ✅ API authentication (JWT tokens)
- ✅ SSE transport authentication
- ✅ Configuration options
- ✅ Security considerations

**Start here if:** You need to understand or configure authentication

---

### Reference Documentation

#### [Tools Reference](TOOLS.md)
**Complete documentation for all 37 MCP tools**

- ✅ All tools organized by resource type
- ✅ Parameters and return values
- ✅ Examples for each tool
- ✅ Use cases and error handling

**Start here if:** You want to see what tools are available and how to use them

---

#### [Tool Documentation Guide](TOOL_DOCUMENTATION_GUIDE.md)
**Best practices for writing LLM-friendly tool documentation**

- ✅ Documentation templates
- ✅ Best practices
- ✅ Examples
- ✅ Checklist

**Start here if:** You're developing new tools or improving documentation

---

## 🗺️ Documentation Structure

```
docs/
├── README.md                    ← You are here
├── CLAUDE_DESKTOP_CONFIG.md    ← Claude Desktop setup
├── DOCKER.md                    ← Docker deployment
├── AUTHENTICATION.md            ← Authentication guide
├── TOOLS.md                     ← Tools reference
└── TOOL_DOCUMENTATION_GUIDE.md  ← Developer guide
```

---

## 🎯 Common Tasks

### I want to...

**...use the server with Claude Desktop**
→ [Claude Desktop Configuration](CLAUDE_DESKTOP_CONFIG.md)

**...run the server in Docker**
→ [Docker Setup](DOCKER.md)

**...see what tools are available**
→ [Tools Reference](TOOLS.md)

**...understand authentication**
→ [Authentication Guide](AUTHENTICATION.md)

**...add a new tool**
→ [Tool Documentation Guide](TOOL_DOCUMENTATION_GUIDE.md)

**...configure the server**
→ [Main README](../README.md#configuration)

---

## 🔗 External Resources

- **[Main README](../README.md)** - Project overview and quick start
- **[Classic Models API](https://github.com/jiridj/classic-models-api)** - API documentation
- **[FastMCP](https://github.com/jlowin/fastmcp)** - MCP framework documentation

---

## 💡 Tips

- **New to MCP?** Start with [Claude Desktop Configuration](CLAUDE_DESKTOP_CONFIG.md)
- **Looking for a specific tool?** Use [Tools Reference](TOOLS.md) and search by resource name
- **Having issues?** Check the troubleshooting sections in each guide
- **Developing?** Read [Tool Documentation Guide](TOOL_DOCUMENTATION_GUIDE.md) first

---

## 📝 Contributing

When adding new documentation:

1. Follow the existing structure and style
2. Use clear headings and examples
3. Add to this index if creating a new guide
4. Update related guides if making changes

---

**Need help?** Check the [Main README](../README.md) or open an issue.
