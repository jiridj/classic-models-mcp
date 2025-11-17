"""Unit tests for MCP server."""
import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock

# Mock fastmcp modules before importing
import sys
from unittest.mock import MagicMock

# Create mock modules
mock_fastmcp = MagicMock()
mock_fastmcp_auth = MagicMock()
sys.modules['fastmcp'] = mock_fastmcp
sys.modules['fastmcp.auth'] = mock_fastmcp_auth

# Now import server components
from src.server import lifespan, register_all_tools


@pytest.mark.asyncio
async def test_lifespan_startup_and_shutdown():
    """lifespan should initialize and close API client."""
    # Mock APIClient
    mock_client = Mock()
    mock_client.initialize = AsyncMock()
    mock_client.close = AsyncMock()
    
    # Mock APIClient class
    with patch('src.server.APIClient', return_value=mock_client):
        # Mock register_all_tools to avoid actual registration
        with patch('src.server.register_all_tools'):
            mock_app = Mock()
            async with lifespan(mock_app):
                # Startup should have been called
                mock_client.initialize.assert_called_once()
    
    # Shutdown should have been called
    mock_client.close.assert_called_once()


def test_register_all_tools_raises_when_no_client():
    """register_all_tools should raise exception when api_client is None."""
    # Temporarily set api_client to None
    import src.server
    original_value = src.server.api_client
    src.server.api_client = None
    
    try:
        with pytest.raises(Exception, match="API client not initialized"):
            register_all_tools()
    finally:
        # Restore original value
        src.server.api_client = original_value


def test_register_all_tools_registers_all_tool_groups():
    """register_all_tools should call all register functions."""
    # Create a mock API client
    mock_client = Mock()
    
    # Mock all register functions
    register_functions = [
        'register_productline_tools',
        'register_product_tools',
        'register_office_tools',
        'register_employee_tools',
        'register_customer_tools',
        'register_order_tools',
        'register_payment_tools',
        'register_orderdetail_tools',
    ]
    
    mock_registers = {}
    for func_name in register_functions:
        mock_registers[func_name] = Mock()
    
    # Set api_client
    import src.server
    original_value = src.server.api_client
    src.server.api_client = mock_client
    
    try:
        # Patch all register functions
        with patch.multiple('src.server', **{name: mock_registers[name] for name in register_functions}):
            register_all_tools()
            
            # Verify all register functions were called with mcp and api_client
            # We need to get mcp from the server module
            from src.server import mcp
            for func_name, mock_func in mock_registers.items():
                mock_func.assert_called_once_with(mcp, mock_client)
    finally:
        # Restore original value
        src.server.api_client = original_value

