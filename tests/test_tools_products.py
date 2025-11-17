"""Unit tests for product tools."""
import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock

from src.tools.products import register_product_tools


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
async def test_register_product_tools_registers_all_tools(mock_mcp, mock_api_client):
    """register_product_tools should register all product tools."""
    register_product_tools(mock_mcp, mock_api_client)
    
    # Verify that mcp.tool() was called 5 times (list, get, create, update, delete)
    assert mock_mcp.tool.call_count == 5


@pytest.mark.asyncio
async def test_list_products_tool(mock_mcp, mock_api_client):
    """classic_models_list_products should call api_client.get."""
    # Store the decorated functions
    decorated_functions = []
    
    def capture_decorator(func):
        decorated_functions.append(func)
        return func
    
    mock_mcp.tool.return_value = capture_decorator
    
    register_product_tools(mock_mcp, mock_api_client)
    
    # Get the registered tool function (first one is list_products)
    tool_func = decorated_functions[0]
    
    # Mock the API response
    expected_response = [
        {
            "productcode": "S10_1678",
            "productname": "Test Product",
            "productline": "Motorcycles",
            "productscale": "1:10",
            "productvendor": "Test Vendor",
            "productdescription": "Test description",
            "quantityinstock": 100,
            "buyprice": "48.81",
            "msrp": "95.70"
        }
    ]
    mock_api_client.get.return_value = expected_response
    
    # Call the tool
    result = await tool_func()
    
    # Verify
    mock_api_client.get.assert_called_once_with("/classic-models/api/v1/products/")
    assert result == expected_response


@pytest.mark.asyncio
async def test_get_product_tool(mock_mcp, mock_api_client):
    """classic_models_get_product should call api_client.get with productcode."""
    # Store the decorated functions
    decorated_functions = []
    
    def capture_decorator(func):
        decorated_functions.append(func)
        return func
    
    mock_mcp.tool.return_value = capture_decorator
    
    register_product_tools(mock_mcp, mock_api_client)
    
    # Get the get_product tool function (second one)
    tool_func = decorated_functions[1]
    
    # Mock the API response
    expected_response = {
        "productcode": "S10_1678",
        "productname": "Test Product",
        "productline": "Motorcycles",
        "productscale": "1:10",
        "productvendor": "Test Vendor",
        "productdescription": "Test description",
        "quantityinstock": 100,
        "buyprice": "48.81",
        "msrp": "95.70"
    }
    mock_api_client.get.return_value = expected_response
    
    # Call the tool
    result = await tool_func(productcode="S10_1678")
    
    # Verify
    mock_api_client.get.assert_called_once_with("/classic-models/api/v1/products/S10_1678/")
    assert result == expected_response


@pytest.mark.asyncio
async def test_create_product_tool(mock_mcp, mock_api_client):
    """classic_models_create_product should call api_client.post with data."""
    # Store the decorated functions
    decorated_functions = []
    
    def capture_decorator(func):
        decorated_functions.append(func)
        return func
    
    mock_mcp.tool.return_value = capture_decorator
    
    register_product_tools(mock_mcp, mock_api_client)
    
    # Get the create_product tool function (third one)
    tool_func = decorated_functions[2]
    
    # Mock the API response
    expected_response = {
        "productcode": "S10_9999",
        "productname": "New Product",
        "productline": "Classic Cars",
        "productscale": "1:18",
        "productvendor": "Test Vendor",
        "productdescription": "New product description",
        "quantityinstock": 50,
        "buyprice": "45.99",
        "msrp": "89.99"
    }
    mock_api_client.post.return_value = expected_response
    
    # Call the tool
    result = await tool_func(
        productcode="S10_9999",
        productname="New Product",
        productline="Classic Cars",
        productscale="1:18",
        productvendor="Test Vendor",
        productdescription="New product description",
        quantityinstock=50,
        buyprice="45.99",
        msrp="89.99"
    )
    
    # Verify
    expected_data = {
        "productcode": "S10_9999",
        "productname": "New Product",
        "productline": "Classic Cars",
        "productscale": "1:18",
        "productvendor": "Test Vendor",
        "productdescription": "New product description",
        "quantityinstock": 50,
        "buyprice": "45.99",
        "msrp": "89.99"
    }
    mock_api_client.post.assert_called_once_with("/classic-models/api/v1/products/", expected_data)
    assert result == expected_response


@pytest.mark.asyncio
async def test_update_product_tool_partial_update(mock_mcp, mock_api_client):
    """classic_models_update_product should call api_client.patch with only provided fields."""
    # Store the decorated functions
    decorated_functions = []
    
    def capture_decorator(func):
        decorated_functions.append(func)
        return func
    
    mock_mcp.tool.return_value = capture_decorator
    
    register_product_tools(mock_mcp, mock_api_client)
    
    # Get the update_product tool function (fourth one)
    tool_func = decorated_functions[3]
    
    # Mock the API response
    expected_response = {
        "productcode": "S10_1678",
        "productname": "Updated Product",
        "quantityinstock": 200,
        "msrp": "99.99"
    }
    mock_api_client.patch.return_value = expected_response
    
    # Call the tool with only some fields
    result = await tool_func(
        productcode="S10_1678",
        productname="Updated Product",
        quantityinstock=200,
        msrp="99.99"
    )
    
    # Verify only provided fields are in the data
    expected_data = {
        "productname": "Updated Product",
        "quantityinstock": 200,
        "msrp": "99.99"
    }
    mock_api_client.patch.assert_called_once_with("/classic-models/api/v1/products/S10_1678/", expected_data)
    assert result == expected_response


@pytest.mark.asyncio
async def test_update_product_tool_no_fields(mock_mcp, mock_api_client):
    """classic_models_update_product should send empty dict when no fields provided."""
    # Store the decorated functions
    decorated_functions = []
    
    def capture_decorator(func):
        decorated_functions.append(func)
        return func
    
    mock_mcp.tool.return_value = capture_decorator
    
    register_product_tools(mock_mcp, mock_api_client)
    
    # Get the update_product tool function (fourth one)
    tool_func = decorated_functions[3]
    
    # Mock the API response
    expected_response = {"productcode": "S10_1678"}
    mock_api_client.patch.return_value = expected_response
    
    # Call the tool with only productcode (no update fields)
    result = await tool_func(productcode="S10_1678")
    
    # Verify empty dict is sent
    mock_api_client.patch.assert_called_once_with("/classic-models/api/v1/products/S10_1678/", {})
    assert result == expected_response


@pytest.mark.asyncio
async def test_delete_product_tool(mock_mcp, mock_api_client):
    """classic_models_delete_product should call api_client.delete."""
    # Store the decorated functions
    decorated_functions = []
    
    def capture_decorator(func):
        decorated_functions.append(func)
        return func
    
    mock_mcp.tool.return_value = capture_decorator
    
    register_product_tools(mock_mcp, mock_api_client)
    
    # Get the delete_product tool function (fifth one)
    tool_func = decorated_functions[4]
    
    # Mock the API response (delete returns None)
    mock_api_client.delete.return_value = None
    
    # Call the tool
    result = await tool_func(productcode="S10_1678")
    
    # Verify
    mock_api_client.delete.assert_called_once_with("/classic-models/api/v1/products/S10_1678/")
    assert result is None

