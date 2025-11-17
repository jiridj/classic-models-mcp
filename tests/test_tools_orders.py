"""Unit tests for order tools."""
import pytest
from unittest.mock import Mock, AsyncMock, MagicMock

from src.tools.orders import register_order_tools


@pytest.fixture
def mock_mcp():
    """Create a mock FastMCP instance."""
    mcp = MagicMock()
    return mcp


@pytest.fixture
def mock_api_client():
    """Create a mock APIClient."""
    client = Mock()
    client.get = AsyncMock()
    client.post = AsyncMock()
    client.patch = AsyncMock()
    client.delete = AsyncMock()
    return client


@pytest.mark.asyncio
async def test_register_order_tools_registers_all_tools(mock_mcp, mock_api_client):
    """register_order_tools should register all order tools."""
    register_order_tools(mock_mcp, mock_api_client)
    
    # Verify that mcp.tool() was called 5 times (list, get, create, update, delete)
    assert mock_mcp.tool.call_count == 5


@pytest.mark.asyncio
async def test_list_orders_tool(mock_mcp, mock_api_client):
    """classic_models_list_orders should call api_client.get."""
    decorated_functions = []
    
    def capture_decorator(func):
        decorated_functions.append(func)
        return func
    
    mock_mcp.tool.return_value = capture_decorator
    
    register_order_tools(mock_mcp, mock_api_client)
    
    # Get the registered tool function
    tool_func = decorated_functions[0]
    
    # Mock the API response
    expected_response = [
        {
            "ordernumber": 10100,
            "orderdate": "2003-01-06",
            "requireddate": "2003-01-13",
            "shippeddate": "2003-01-10",
            "status": "Shipped",
            "comments": "Check on availability.",
            "customernumber": 363
        }
    ]
    mock_api_client.get.return_value = expected_response
    
    # Call the tool
    result = await tool_func()
    
    # Verify
    mock_api_client.get.assert_called_once_with("/classic-models/api/v1/orders/")
    assert result == expected_response


@pytest.mark.asyncio
async def test_get_order_tool(mock_mcp, mock_api_client):
    """classic_models_get_order should call api_client.get with ordernumber."""
    decorated_functions = []
    
    def capture_decorator(func):
        decorated_functions.append(func)
        return func
    
    mock_mcp.tool.return_value = capture_decorator
    
    register_order_tools(mock_mcp, mock_api_client)
    
    # Get the get_order tool function (second one)
    tool_func = decorated_functions[1]
    
    # Mock the API response
    expected_response = {
        "ordernumber": 10100,
        "orderdate": "2003-01-06",
        "status": "Shipped",
        "customernumber": 363
    }
    mock_api_client.get.return_value = expected_response
    
    # Call the tool
    result = await tool_func(ordernumber=10100)
    
    # Verify
    mock_api_client.get.assert_called_once_with("/classic-models/api/v1/orders/10100/")
    assert result == expected_response


@pytest.mark.asyncio
async def test_create_order_tool(mock_mcp, mock_api_client):
    """classic_models_create_order should call api_client.post with data."""
    decorated_functions = []
    
    def capture_decorator(func):
        decorated_functions.append(func)
        return func
    
    mock_mcp.tool.return_value = capture_decorator
    
    register_order_tools(mock_mcp, mock_api_client)
    
    # Get the create_order tool function (third one)
    tool_func = decorated_functions[2]
    
    # Mock the API response
    expected_response = {
        "ordernumber": 99999,
        "orderdate": "2024-01-01",
        "requireddate": "2024-01-15",
        "status": "In Process",
        "customernumber": 103
    }
    mock_api_client.post.return_value = expected_response
    
    # Call the tool
    result = await tool_func(
        ordernumber=99999,
        orderdate="2024-01-01",
        requireddate="2024-01-15",
        status="In Process",
        customernumber=103
    )
    
    # Verify
    call_args = mock_api_client.post.call_args
    assert call_args[0][0] == "/classic-models/api/v1/orders/"
    assert call_args[0][1]["orderdate"] == "2024-01-01"
    assert call_args[0][1]["customernumber"] == 103
    assert result == expected_response


@pytest.mark.asyncio
async def test_update_order_tool(mock_mcp, mock_api_client):
    """classic_models_update_order should call api_client.patch with only provided fields."""
    decorated_functions = []
    
    def capture_decorator(func):
        decorated_functions.append(func)
        return func
    
    mock_mcp.tool.return_value = capture_decorator
    
    register_order_tools(mock_mcp, mock_api_client)
    
    # Get the update_order tool function (fourth one)
    tool_func = decorated_functions[3]
    
    # Mock the API response
    expected_response = {
        "ordernumber": 10100,
        "status": "Shipped"
    }
    mock_api_client.patch.return_value = expected_response
    
    # Call the tool with only some fields
    result = await tool_func(
        ordernumber=10100,
        status="Shipped"
    )
    
    # Verify
    expected_data = {"status": "Shipped"}
    mock_api_client.patch.assert_called_once_with("/classic-models/api/v1/orders/10100/", expected_data)
    assert result == expected_response


@pytest.mark.asyncio
async def test_delete_order_tool(mock_mcp, mock_api_client):
    """classic_models_delete_order should call api_client.delete."""
    decorated_functions = []
    
    def capture_decorator(func):
        decorated_functions.append(func)
        return func
    
    mock_mcp.tool.return_value = capture_decorator
    
    register_order_tools(mock_mcp, mock_api_client)
    
    # Get the delete_order tool function (fifth one)
    tool_func = decorated_functions[4]
    
    # Mock the API response (delete returns None)
    mock_api_client.delete.return_value = None
    
    # Call the tool
    result = await tool_func(ordernumber=10100)
    
    # Verify
    mock_api_client.delete.assert_called_once_with("/classic-models/api/v1/orders/10100/")
    assert result is None

