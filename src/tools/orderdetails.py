"""MCP tools for Order Details resource."""
from typing import Optional
from fastmcp import FastMCP
from ..api.client import APIClient


def register_orderdetail_tools(mcp: FastMCP, api_client: APIClient):
    """Register all order detail tools with the MCP server."""
    
    @mcp.tool()
    async def classic_models_list_orderdetails() -> list[dict]:
        """Retrieve a list of all order line items with product details.
        
        This tool returns all order details (line items) in the Classic Models system
        including product information, quantities, and pricing.
        
        **When to use:**
        - Viewing all order line items
        - Getting order detail information
        - Order detail management and reporting
        - Analyzing order line items
        
        **Parameters:**
        None - This tool requires no parameters and returns all order details.
        
        **Returns:**
        A list of order detail dictionaries. Each dictionary contains:
        - `id` (int): Internal order detail identifier
        - `ordernumber` (int): Order number this line item belongs to
        - `productcode` (str): Product code for this line item
        - `quantityordered` (int): Quantity ordered
        - `priceeach` (str): Price per unit in decimal format
        - `orderlinenumber` (int): Line number within the order (typically 1, 2, 3, etc.)
        
        **Example Response:**
        ```json
        [
            {
                "id": 1,
                "ordernumber": 10100,
                "productcode": "S18_1749",
                "quantityordered": 30,
                "priceeach": "136.00",
                "orderlinenumber": 3
            }
        ]
        ```
        
        **Errors:**
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        """
        return await api_client.get("/classic-models/api/v1/orderdetails/")
    
    
    @mcp.tool()
    async def classic_models_get_orderdetail(orderdetail_id: int) -> dict:
        """Retrieve detailed information about a specific order detail by its ID.
        
        This tool fetches complete order detail information including product,
        quantity, pricing, and order information.
        
        **When to use:**
        - Getting details for a specific order line item when you know the ID
        - Verifying order detail information
        - Looking up order line item details by ID
        
        **Parameters:**
        - `orderdetail_id` (int, required): The unique order detail ID identifier.
          Example: 1 or 100
          Must be an existing order detail ID in the system
        
        **Returns:**
        A dictionary containing the order detail object with all fields:
        - `id` (int): Internal order detail identifier (auto-generated)
        - `ordernumber` (int): Order number this line item belongs to
        - `productcode` (str): Product code for this line item
        - `quantityordered` (int): Quantity ordered
        - `priceeach` (str): Price per unit in decimal format
        - `orderlinenumber` (int): Line number within the order
        
        **Example Request:**
        ```python
        orderdetail = await classic_models_get_orderdetail(orderdetail_id=1)
        ```
        
        **Example Response:**
        ```json
        {
            "id": 1,
            "ordernumber": 10100,
            "productcode": "S10_1678",
            "quantityordered": 30,
            "priceeach": "136.00",
            "orderlinenumber": 1
        }
        ```
        
        **Errors:**
        - `404 Not Found`: The order detail ID does not exist
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        
        **Related Tools:**
        - Use `classic_models_get_orderdetail_by_key` to lookup by order number and product code
        - Use `classic_models_get_order` to get the order this detail belongs to
        - Use `classic_models_get_product` to get product details
        """
        return await api_client.get(f"/classic-models/api/v1/orderdetails/{orderdetail_id}/")
    
    
    @mcp.tool()
    async def classic_models_get_orderdetail_by_key(ordernumber: int, productcode: str) -> dict:
        """Retrieve detailed information about a specific order detail by order number and product code.
        
        This tool fetches complete order detail information using the composite key
        (order number and product code). This is the traditional lookup method and
        maintains backward compatibility.
        
        **When to use:**
        - Getting details for a specific order line item when you know the order number and product code
        - Looking up order details using the composite key
        - Maintaining compatibility with existing workflows
        
        **Parameters:**
        - `ordernumber` (int, required): The order number this line item belongs to.
          Must be an existing order number in the system
        - `productcode` (str, required): The product code for this line item.
          Example: "S10_1678" or "S18_1749"
          Must be an existing product code
        
        **Returns:**
        A dictionary containing the order detail object with all fields:
        - `id` (int): Internal order detail identifier (auto-generated)
        - `ordernumber` (int): Order number this line item belongs to
        - `productcode` (str): Product code for this line item
        - `quantityordered` (int): Quantity ordered
        - `priceeach` (str): Price per unit in decimal format
        - `orderlinenumber` (int): Line number within the order
        
        **Example Request:**
        ```python
        orderdetail = await classic_models_get_orderdetail_by_key(
            ordernumber=10100,
            productcode="S10_1678"
        )
        ```
        
        **Example Response:**
        ```json
        {
            "id": 1,
            "ordernumber": 10100,
            "productcode": "S10_1678",
            "quantityordered": 30,
            "priceeach": "136.00",
            "orderlinenumber": 1
        }
        ```
        
        **Errors:**
        - `404 Not Found`: The order detail does not exist for this order number/product code combination
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        
        **Related Tools:**
        - Use `classic_models_get_orderdetail` to lookup by ID
        - Use `classic_models_get_order` to get the order this detail belongs to
        - Use `classic_models_get_product` to get product details
        """
        return await api_client.get(f"/classic-models/api/v1/orderdetails/{ordernumber}/{productcode}/")
    
    
    @mcp.tool()
    async def classic_models_create_orderdetail(
        ordernumber: int,
        productcode: str,
        quantityordered: int,
        priceeach: str,
        orderlinenumber: int,
    ) -> dict:
        """Create a new order line item with product details.
        
        This tool creates a new order detail (line item) for an order.
        The order number and product code must already exist.
        
        **When to use:**
        - Adding products to an order
        - Creating order line items
        - Adding items to existing orders
        
        **Parameters:**
        - `ordernumber` (int, required): Order number this line item belongs to.
          Must be an existing order number
        - `productcode` (str, required): Product code for this line item.
          Must be an existing product code. Example: "S18_1749"
        - `quantityordered` (int, required): Quantity ordered.
          Must be a positive integer
        - `priceeach` (str, required): Price per unit in decimal format.
          Example: "136.00"
        - `orderlinenumber` (int, required): Line number within the order.
          Typically sequential (1, 2, 3, etc.). Range: -32768 to 32767
        
        **Returns:**
        A dictionary containing the created order detail object with all fields:
        - `id` (int): Internal order detail identifier (auto-generated, included in response)
        - `ordernumber` (int): Order number this line item belongs to
        - `productcode` (str): Product code for this line item
        - `quantityordered` (int): Quantity ordered
        - `priceeach` (str): Price per unit in decimal format
        - `orderlinenumber` (int): Line number within the order
        
        **Example Request:**
        ```python
        result = await classic_models_create_orderdetail(
            ordernumber=10100,
            productcode="S18_1749",
            quantityordered=30,
            priceeach="136.00",
            orderlinenumber=3
        )
        ```
        
        **Errors:**
        - `400 Bad Request`: Invalid data or missing required fields
        - `404 Not Found`: Order number does not exist
        - `404 Not Found`: Product code does not exist
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        
        **Related Tools:**
        - Use `classic_models_list_orders` to see available order numbers
        - Use `classic_models_list_products` to see available product codes
        """
        data = {
            "ordernumber": ordernumber,
            "productcode": productcode,
            "quantityordered": quantityordered,
            "priceeach": priceeach,
            "orderlinenumber": orderlinenumber,
        }
        return await api_client.post("/classic-models/api/v1/orderdetails/", data)
    
    
    @mcp.tool()
    async def classic_models_update_orderdetail(
        orderdetail_id: int,
        ordernumber: Optional[int] = None,
        productcode: Optional[str] = None,
        quantityordered: Optional[int] = None,
        priceeach: Optional[str] = None,
        orderlinenumber: Optional[int] = None,
    ) -> dict:
        """Update specific fields of an existing order detail record by ID.
        
        This tool allows partial updates to an order detail. Only provided fields will be updated.
        Use this for making changes to order line items without affecting other fields.
        
        **When to use:**
        - Updating quantities ordered
        - Adjusting prices
        - Changing products in an order line item
        - Modifying order line numbers
        
        **Parameters:**
        - `orderdetail_id` (int, required): The order detail ID to update.
          Must be an existing order detail ID
        - `ordernumber` (int, optional): Updated order number. Must be an existing order number
        - `productcode` (str, optional): Updated product code. Must be an existing product code
        - `quantityordered` (int, optional): Updated quantity ordered. Must be a positive integer
        - `priceeach` (str, optional): Updated price per unit in decimal format
        - `orderlinenumber` (int, optional): Updated line number. Range: -32768 to 32767
        
        **Returns:**
        A dictionary containing the updated order detail object with all fields:
        - `id` (int): Internal order detail identifier (auto-generated)
        - `ordernumber` (int): Order number this line item belongs to
        - `productcode` (str): Product code for this line item
        - `quantityordered` (int): Quantity ordered
        - `priceeach` (str): Price per unit in decimal format
        - `orderlinenumber` (int): Line number within the order
        
        **Example Request:**
        ```python
        result = await classic_models_update_orderdetail(
            orderdetail_id=1,
            quantityordered=35,
            priceeach="140.00"
        )
        ```
        
        **Errors:**
        - `404 Not Found`: The order detail ID does not exist
        - `400 Bad Request`: Invalid data
        - `404 Not Found`: Order number does not exist (if updating ordernumber)
        - `404 Not Found`: Product code does not exist (if updating productcode)
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        
        **Related Tools:**
        - Use `classic_models_update_orderdetail_by_key` to update using composite key
        """
        data = {}
        if ordernumber is not None:
            data["ordernumber"] = ordernumber
        if productcode is not None:
            data["productcode"] = productcode
        if quantityordered is not None:
            data["quantityordered"] = quantityordered
        if priceeach is not None:
            data["priceeach"] = priceeach
        if orderlinenumber is not None:
            data["orderlinenumber"] = orderlinenumber
        
        return await api_client.patch(f"/classic-models/api/v1/orderdetails/{orderdetail_id}/", data)
    
    
    @mcp.tool()
    async def classic_models_update_orderdetail_by_key(
        ordernumber: int,
        productcode: str,
        quantityordered: Optional[int] = None,
        priceeach: Optional[str] = None,
        orderlinenumber: Optional[int] = None,
    ) -> dict:
        """Update specific fields of an existing order detail record by composite key.
        
        This tool allows partial updates to an order detail using the composite key
        (order number and product code). Only provided fields will be updated.
        This maintains backward compatibility with existing workflows.
        
        **When to use:**
        - Updating quantities ordered when you know the order number and product code
        - Adjusting prices using composite key lookup
        - Modifying order line numbers using composite key
        
        **Parameters:**
        - `ordernumber` (int, required): The order number of the order detail to update.
          Must be an existing order number
        - `productcode` (str, required): The product code of the order detail to update.
          Must be an existing product code
        - `quantityordered` (int, optional): Updated quantity ordered. Must be a positive integer
        - `priceeach` (str, optional): Updated price per unit in decimal format
        - `orderlinenumber` (int, optional): Updated line number. Range: -32768 to 32767
        
        **Returns:**
        A dictionary containing the updated order detail object with all fields:
        - `id` (int): Internal order detail identifier (auto-generated)
        - `ordernumber` (int): Order number this line item belongs to
        - `productcode` (str): Product code for this line item
        - `quantityordered` (int): Quantity ordered
        - `priceeach` (str): Price per unit in decimal format
        - `orderlinenumber` (int): Line number within the order
        
        **Example Request:**
        ```python
        result = await classic_models_update_orderdetail_by_key(
            ordernumber=10100,
            productcode="S10_1678",
            quantityordered=35,
            priceeach="140.00"
        )
        ```
        
        **Errors:**
        - `404 Not Found`: The order detail does not exist for this order number/product code combination
        - `400 Bad Request`: Invalid data
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        
        **Related Tools:**
        - Use `classic_models_update_orderdetail` to update using ID
        """
        data = {}
        if quantityordered is not None:
            data["quantityordered"] = quantityordered
        if priceeach is not None:
            data["priceeach"] = priceeach
        if orderlinenumber is not None:
            data["orderlinenumber"] = orderlinenumber
        
        return await api_client.patch(
            f"/classic-models/api/v1/orderdetails/{ordernumber}/{productcode}/",
            data
        )
    
    
    @mcp.tool()
    async def classic_models_delete_orderdetail(orderdetail_id: int) -> None:
        """Remove an order detail (line item) from the system by ID.
        
        This tool permanently deletes an order detail record. Use with caution as this
        affects the order total and product quantities.
        
        **When to use:**
        - Removing items from orders when you know the ID
        - Cleaning up incorrect order line items
        - Removing cancelled line items
        
        **Parameters:**
        - `orderdetail_id` (int, required): The order detail ID to delete.
          Must be an existing order detail ID
        
        **Returns:**
        None - Success is indicated by no error being raised.
        
        **Example Request:**
        ```python
        await classic_models_delete_orderdetail(orderdetail_id=1)
        ```
        
        **Errors:**
        - `404 Not Found`: The order detail ID does not exist
        - `400 Bad Request`: Cannot delete
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        
        **Related Tools:**
        - Use `classic_models_delete_orderdetail_by_key` to delete using composite key
        """
        await api_client.delete(f"/classic-models/api/v1/orderdetails/{orderdetail_id}/")
    
    
    @mcp.tool()
    async def classic_models_delete_orderdetail_by_key(ordernumber: int, productcode: str) -> None:
        """Remove an order detail (line item) from the system by composite key.
        
        This tool permanently deletes an order detail record using the composite key
        (order number and product code). Use with caution as this affects the order
        total and product quantities. This maintains backward compatibility.
        
        **When to use:**
        - Removing items from orders when you know the order number and product code
        - Cleaning up incorrect order line items using composite key
        - Removing cancelled line items using composite key
        
        **Parameters:**
        - `ordernumber` (int, required): The order number of the order detail to delete.
          Must be an existing order number
        - `productcode` (str, required): The product code of the order detail to delete.
          Must be an existing product code
        
        **Returns:**
        None - Success is indicated by no error being raised.
        
        **Example Request:**
        ```python
        await classic_models_delete_orderdetail_by_key(
            ordernumber=10100,
            productcode="S10_1678"
        )
        ```
        
        **Errors:**
        - `404 Not Found`: The order detail does not exist for this order number/product code combination
        - `400 Bad Request`: Cannot delete
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        
        **Related Tools:**
        - Use `classic_models_delete_orderdetail` to delete using ID
        """
        await api_client.delete(f"/classic-models/api/v1/orderdetails/{ordernumber}/{productcode}/")

