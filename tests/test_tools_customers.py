"""Unit tests for customer tools."""
import pytest
from unittest.mock import Mock, AsyncMock, MagicMock

from src.tools.customers import register_customer_tools


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
async def test_register_customer_tools_registers_all_tools(mock_mcp, mock_api_client):
    """register_customer_tools should register all customer tools."""
    register_customer_tools(mock_mcp, mock_api_client)
    
    # Verify that mcp.tool() was called 5 times (list, get, create, update, delete)
    assert mock_mcp.tool.call_count == 5


@pytest.mark.asyncio
async def test_list_customers_tool(mock_mcp, mock_api_client):
    """classic_models_list_customers should call api_client.get."""
    decorated_functions = []
    
    def capture_decorator(func):
        decorated_functions.append(func)
        return func
    
    mock_mcp.tool.return_value = capture_decorator
    
    register_customer_tools(mock_mcp, mock_api_client)
    
    # Get the registered tool function
    tool_func = decorated_functions[0]
    
    # Mock the API response
    expected_response = [
        {
            "customernumber": 103,
            "customername": "Test Customer",
            "contactlastname": "Doe",
            "contactfirstname": "John",
            "phone": "123-456-7890",
            "addressline1": "123 Main St",
            "city": "New York",
            "country": "USA",
            "creditlimit": "10000.00"
        }
    ]
    mock_api_client.get.return_value = expected_response
    
    # Call the tool
    result = await tool_func()
    
    # Verify
    mock_api_client.get.assert_called_once_with("/classic-models/api/v1/customers/")
    assert result == expected_response


@pytest.mark.asyncio
async def test_get_customer_tool(mock_mcp, mock_api_client):
    """classic_models_get_customer should call api_client.get with customernumber."""
    decorated_functions = []
    
    def capture_decorator(func):
        decorated_functions.append(func)
        return func
    
    mock_mcp.tool.return_value = capture_decorator
    
    register_customer_tools(mock_mcp, mock_api_client)
    
    # Get the get_customer tool function (second one)
    tool_func = decorated_functions[1]
    
    # Mock the API response
    expected_response = {
        "customernumber": 103,
        "customername": "Test Customer",
        "contactlastname": "Doe",
        "contactfirstname": "John"
    }
    mock_api_client.get.return_value = expected_response
    
    # Call the tool
    result = await tool_func(customernumber=103)
    
    # Verify
    mock_api_client.get.assert_called_once_with("/classic-models/api/v1/customers/103/")
    assert result == expected_response


@pytest.mark.asyncio
async def test_create_customer_tool(mock_mcp, mock_api_client):
    """classic_models_create_customer should call api_client.post with data."""
    decorated_functions = []
    
    def capture_decorator(func):
        decorated_functions.append(func)
        return func
    
    mock_mcp.tool.return_value = capture_decorator
    
    register_customer_tools(mock_mcp, mock_api_client)
    
    # Get the create_customer tool function (third one)
    tool_func = decorated_functions[2]
    
    # Mock the API response
    expected_response = {
        "customernumber": 999,
        "customername": "New Customer",
        "contactlastname": "Smith",
        "contactfirstname": "Jane"
    }
    mock_api_client.post.return_value = expected_response
    
    # Call the tool
    result = await tool_func(
        customernumber=999,
        customername="New Customer",
        contactlastname="Smith",
        contactfirstname="Jane",
        phone="555-1234",
        addressline1="456 Oak Ave",
        city="Boston",
        country="USA"
    )
    
    # Verify
    call_args = mock_api_client.post.call_args
    assert call_args[0][0] == "/classic-models/api/v1/customers/"
    assert call_args[0][1]["customername"] == "New Customer"
    assert call_args[0][1]["contactlastname"] == "Smith"
    assert result == expected_response


@pytest.mark.asyncio
async def test_update_customer_tool(mock_mcp, mock_api_client):
    """classic_models_update_customer should call api_client.patch with only provided fields."""
    decorated_functions = []
    
    def capture_decorator(func):
        decorated_functions.append(func)
        return func
    
    mock_mcp.tool.return_value = capture_decorator
    
    register_customer_tools(mock_mcp, mock_api_client)
    
    # Get the update_customer tool function (fourth one)
    tool_func = decorated_functions[3]
    
    # Mock the API response
    expected_response = {
        "customernumber": 103,
        "customername": "Updated Customer"
    }
    mock_api_client.patch.return_value = expected_response
    
    # Call the tool with only some fields
    result = await tool_func(
        customernumber=103,
        customername="Updated Customer"
    )
    
    # Verify
    expected_data = {"customername": "Updated Customer"}
    mock_api_client.patch.assert_called_once_with("/classic-models/api/v1/customers/103/", expected_data)
    assert result == expected_response


@pytest.mark.asyncio
async def test_delete_customer_tool(mock_mcp, mock_api_client):
    """classic_models_delete_customer should call api_client.delete."""
    decorated_functions = []
    
    def capture_decorator(func):
        decorated_functions.append(func)
        return func
    
    mock_mcp.tool.return_value = capture_decorator
    
    register_customer_tools(mock_mcp, mock_api_client)
    
    # Get the delete_customer tool function (fifth one)
    tool_func = decorated_functions[4]
    
    # Mock the API response (delete returns None)
    mock_api_client.delete.return_value = None
    
    # Call the tool
    result = await tool_func(customernumber=103)
    
    # Verify
    mock_api_client.delete.assert_called_once_with("/classic-models/api/v1/customers/103/")
    assert result is None

