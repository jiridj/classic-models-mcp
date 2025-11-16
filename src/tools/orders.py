"""MCP tools for Orders resource."""
from typing import Optional
from fastmcp import FastMCP
from ..api.client import APIClient


def register_order_tools(mcp: FastMCP, api_client: APIClient):
    """Register all order tools with the MCP server."""
    
    @mcp.tool()
    async def classic_models_list_orders() -> list[dict]:
        """Retrieve a list of all customer orders with their status and details.
        
        This tool returns all orders in the Classic Models system including
        order dates, status, and customer information.
        
        **When to use:**
        - Viewing all orders in the system
        - Getting order status information
        - Order management and reporting
        - Tracking order fulfillment
        
        **Parameters:**
        None - This tool requires no parameters and returns all orders.
        
        **Returns:**
        A list of order dictionaries. Each dictionary contains:
        - `ordernumber` (int): Unique order number identifier
        - `orderdate` (str): Date when the order was placed (YYYY-MM-DD format)
        - `requireddate` (str): Required delivery date (YYYY-MM-DD format)
        - `shippeddate` (str, optional): Date when the order was shipped (YYYY-MM-DD format)
        - `status` (str): Order status (max 15 characters). Examples: "Shipped", "In Process", "Cancelled"
        - `comments` (str, optional): Order comments or notes
        - `customernumber` (int): Customer number who placed the order
        
        **Example Response:**
        ```json
        [
            {
                "ordernumber": 10100,
                "orderdate": "2003-01-06",
                "requireddate": "2003-01-13",
                "shippeddate": "2003-01-10",
                "status": "Shipped",
                "comments": null,
                "customernumber": 363
            }
        ]
        ```
        
        **Errors:**
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        """
        return await api_client.get("/classic-models/api/v1/orders/")
    
    
    @mcp.tool()
    async def classic_models_get_order(ordernumber: int) -> dict:
        """Retrieve detailed information about a specific order by its order number.
        
        This tool fetches complete order information including dates, status,
        customer, and comments.
        
        **When to use:**
        - Getting details for a specific order
        - Verifying order status
        - Looking up order information for customer service
        - Checking order fulfillment status
        
        **Parameters:**
        - `ordernumber` (int, required): The unique order number identifier.
          Example: 10100 or 10101
          Must be an existing order number in the system
        
        **Returns:**
        A dictionary containing the order object with all fields.
        
        **Example Request:**
        ```python
        order = await classic_models_get_order(ordernumber=10100)
        ```
        
        **Errors:**
        - `404 Not Found`: The order number does not exist
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        
        **Related Tools:**
        - Use `classic_models_list_orderdetails` to get order line items for this order
        """
        return await api_client.get(f"/classic-models/api/v1/orders/{ordernumber}/")
    
    
    @mcp.tool()
    async def classic_models_create_order(
        ordernumber: int,
        orderdate: str,
        requireddate: str,
        status: str,
        customernumber: int,
        shippeddate: Optional[str] = None,
        comments: Optional[str] = None,
    ) -> dict:
        """Create a new customer order with order date, required date, and status information.
        
        This tool creates a new order record. The customer number must already exist.
        After creating an order, use order details tools to add line items.
        
        **When to use:**
        - Creating new customer orders
        - Processing new orders
        - Adding orders to the system
        
        **Parameters:**
        - `ordernumber` (int, required): Unique order number identifier.
          Example: 10500
          Must be unique (not already exist)
        - `orderdate` (str, required): Date when the order was placed.
          Format: YYYY-MM-DD. Example: "2024-01-15"
        - `requireddate` (str, required): Required delivery date.
          Format: YYYY-MM-DD. Example: "2024-01-22"
        - `status` (str, required): Order status.
          Maximum length: 15 characters. Examples: "In Process", "Shipped", "Cancelled"
        - `customernumber` (int, required): Customer number who placed the order.
          Must be an existing customer number
        - `shippeddate` (str, optional): Date when the order was shipped.
          Format: YYYY-MM-DD. Example: "2024-01-20"
        - `comments` (str, optional): Order comments or special instructions
        
        **Returns:**
        A dictionary containing the created order object with all fields.
        
        **Example Request:**
        ```python
        result = await classic_models_create_order(
            ordernumber=10500,
            orderdate="2024-01-15",
            requireddate="2024-01-22",
            status="In Process",
            customernumber=363,
            comments="Rush order"
        )
        ```
        
        **Errors:**
        - `400 Bad Request`: Invalid data or missing required fields
        - `409 Conflict`: Order number already exists
        - `404 Not Found`: Customer number does not exist
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        
        **Related Tools:**
        - Use `classic_models_list_customers` to see available customer numbers
        - Use `classic_models_create_orderdetail` to add line items to the order
        """
        data = {
            "ordernumber": ordernumber,
            "orderdate": orderdate,
            "requireddate": requireddate,
            "status": status,
            "customernumber": customernumber,
        }
        if shippeddate is not None:
            data["shippeddate"] = shippeddate
        if comments is not None:
            data["comments"] = comments
        
        return await api_client.post("/classic-models/api/v1/orders/", data)
    
    
    @mcp.tool()
    async def classic_models_update_order(
        ordernumber: int,
        orderdate: Optional[str] = None,
        requireddate: Optional[str] = None,
        shippeddate: Optional[str] = None,
        status: Optional[str] = None,
        comments: Optional[str] = None,
        customernumber: Optional[int] = None,
    ) -> dict:
        """Update specific fields of an existing order record.
        
        This tool allows partial updates to an order. Only provided fields will be updated.
        Use this for making changes to order information without affecting other fields.
        
        **When to use:**
        - Updating order status (e.g., marking as shipped)
        - Changing order dates
        - Adding shipping dates
        - Updating order comments
        
        **Parameters:**
        - `ordernumber` (int, required): The order number to update.
          Must be an existing order number
        - `orderdate` (str, optional): Updated order date. Format: YYYY-MM-DD
        - `requireddate` (str, optional): Updated required date. Format: YYYY-MM-DD
        - `shippeddate` (str, optional): Updated shipped date. Format: YYYY-MM-DD
        - `status` (str, optional): Updated order status. Maximum length: 15 characters
        - `comments` (str, optional): Updated order comments
        - `customernumber` (int, optional): Updated customer number. Must be an existing customer number
        
        **Returns:**
        A dictionary containing the updated order object.
        
        **Example Request:**
        ```python
        result = await classic_models_update_order(
            ordernumber=10100,
            status="Shipped",
            shippeddate="2024-01-20"
        )
        ```
        
        **Errors:**
        - `404 Not Found`: The order number does not exist
        - `400 Bad Request`: Invalid data
        - `404 Not Found`: Customer number does not exist (if updating customernumber)
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        """
        data = {}
        if orderdate is not None:
            data["orderdate"] = orderdate
        if requireddate is not None:
            data["requireddate"] = requireddate
        if shippeddate is not None:
            data["shippeddate"] = shippeddate
        if status is not None:
            data["status"] = status
        if comments is not None:
            data["comments"] = comments
        if customernumber is not None:
            data["customernumber"] = customernumber
        
        return await api_client.patch(f"/classic-models/api/v1/orders/{ordernumber}/", data)
    
    
    @mcp.tool()
    async def classic_models_delete_order(ordernumber: int) -> None:
        """Remove an order from the system.
        
        This tool permanently deletes an order record. Use with caution as this
        will also affect order details associated with this order.
        
        **When to use:**
        - Removing cancelled orders
        - Cleaning up obsolete order records
        - Removing orders that should not have been created
        
        **Parameters:**
        - `ordernumber` (int, required): The order number to delete.
          Must be an existing order number
        
        **Returns:**
        None - Success is indicated by no error being raised.
        
        **Example Request:**
        ```python
        await classic_models_delete_order(ordernumber=10500)
        ```
        
        **Errors:**
        - `404 Not Found`: The order number does not exist
        - `400 Bad Request`: Cannot delete (e.g., order details still exist)
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        
        **Warning:**
        Deleting an order may fail if order details still exist for this order.
        Consider deleting order details first.
        """
        await api_client.delete(f"/classic-models/api/v1/orders/{ordernumber}/")

