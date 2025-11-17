"""Main MCP server for Classic Models API."""
import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastmcp import FastMCP
from .config import config
from .api.client import APIClient

# Global API client instance
api_client: APIClient | None = None


@asynccontextmanager
async def lifespan(app: FastMCP) -> AsyncGenerator[None, None]:
    """Lifespan context manager for startup and shutdown."""
    global api_client
    # Startup
    api_client = APIClient()
    await api_client.initialize()
    # Register all tools after API client is ready
    register_all_tools()
    yield
    # Shutdown
    if api_client:
        await api_client.close()


# Initialize FastMCP server with lifespan
# Configure authentication for HTTP transport if needed
auth = None
if config.transport == "http":
    from fastmcp.server.auth import StaticTokenVerifier
    # Create a static token verifier for bearer token authentication
    auth = StaticTokenVerifier(
        tokens={config.http_bearer_token: {"client_id": "mcp-client", "scopes": []}}
    )

mcp = FastMCP(
    name="Classic Models API Server",
    instructions="MCP server for interacting with the Classic Models API. Provides tools for managing products, customers, orders, and more.",
    lifespan=lifespan,
    auth=auth,
)


# Import and register all tools
from .tools.productlines import register_productline_tools
from .tools.products import register_product_tools
from .tools.offices import register_office_tools
from .tools.employees import register_employee_tools
from .tools.customers import register_customer_tools
from .tools.orders import register_order_tools
from .tools.payments import register_payment_tools
from .tools.orderdetails import register_orderdetail_tools


def register_all_tools():
    """Register all MCP tools with the server."""
    if api_client is None:
        raise Exception("API client not initialized. Tools must be registered after server startup.")
    
    # Register all tool groups
    register_productline_tools(mcp, api_client)
    register_product_tools(mcp, api_client)
    register_office_tools(mcp, api_client)
    register_employee_tools(mcp, api_client)
    register_customer_tools(mcp, api_client)
    register_order_tools(mcp, api_client)
    register_payment_tools(mcp, api_client)
    register_orderdetail_tools(mcp, api_client)


# Register tools after API client is initialized
# This will be called in the lifespan startup


if __name__ == "__main__":
    # Run the MCP server
    if config.transport == "http":
        mcp.run(
            transport="http",
            host="0.0.0.0",
            port=config.http_port,
        )
    else:
        # Default to stdio transport
        mcp.run()

