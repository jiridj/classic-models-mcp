"""Example of a well-documented tool following LLM-friendly best practices.

This module demonstrates how to document MCP tools to maximize LLM comprehension.
Use this as a reference when creating new tools.
"""
from typing import Optional
from fastmcp import FastMCP
from ..api.client import APIClient

# This would be imported from server.py in actual implementation
# api_client: APIClient | None = None


def create_example_tool(mcp: FastMCP, api_client: APIClient):
    """Register an example tool with comprehensive documentation."""
    
    @mcp.tool()
    async def classic_models_get_product(productcode: str) -> dict:
        """Retrieve detailed information about a specific product by its product code.
        
        This tool fetches complete product information including pricing, inventory,
        description, and categorization details from the Classic Models catalog.
        
        **When to use:**
        - Looking up product details before making a sale
        - Checking product availability and pricing
        - Retrieving product information for order processing
        - Getting product specifications for customer inquiries
        
        **Parameters:**
        - `productcode` (str, required): The unique product code identifier.
          Format: Typically starts with a letter followed by numbers/underscores.
          Example: "S10_1678" or "S12_1098"
          Maximum length: 15 characters
          Must be an existing product code in the system
        
        **Returns:**
        A dictionary containing the complete product object with the following fields:
        - `productcode` (str): The product code identifier
        - `productname` (str): Full name of the product
        - `productline` (str): Category/line the product belongs to
        - `productscale` (str): Scale of the model (e.g., "1:10", "1:18")
        - `productvendor` (str): Manufacturer or vendor name
        - `productdescription` (str): Detailed product description
        - `quantityinstock` (int): Current inventory quantity (0-32767)
        - `buyprice` (str): Wholesale cost in decimal format
        - `msrp` (str): Manufacturer's Suggested Retail Price in decimal format
        
        **Example Request:**
        ```python
        product = await classic_models_get_product(productcode="S10_1678")
        ```
        
        **Example Response:**
        ```json
        {
            "productcode": "S10_1678",
            "productname": "1969 Harley Davidson Ultimate Chopper",
            "productline": "Motorcycles",
            "productscale": "1:10",
            "productvendor": "Min Lin Diecast",
            "productdescription": "This replica features working kickstand...",
            "quantityinstock": 7933,
            "buyprice": "48.81",
            "msrp": "95.70"
        }
        ```
        
        **Errors:**
        - `404 Not Found`: The product code does not exist in the system.
          Error message: "Product with code '{productcode}' not found"
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        
        **Related Tools:**
        - Use `classic_models_list_products` to get all products
        - Use `classic_models_create_product` to add new products
        - Use `classic_models_update_product` to modify product information
        """
        if api_client is None:
            raise Exception("API client not initialized")
        
        return await api_client.get(f"/classic-models/api/v1/products/{productcode}/")
    
    
    @mcp.tool()
    async def classic_models_list_products() -> list[dict]:
        """Retrieve a paginated list of all products in the Classic Models catalog.
        
        This tool returns all products available in the system with their complete
        details. Use this tool to browse the product catalog or get an overview
        of available inventory.
        
        **When to use:**
        - Browsing the complete product catalog
        - Getting an overview of all available products
        - Finding products by examining the full list
        - Inventory management and reporting
        
        **Parameters:**
        None - This tool requires no parameters and returns all products.
        
        **Returns:**
        A list of product dictionaries. Each product dictionary contains:
        - `productcode` (str): Unique product identifier
        - `productname` (str): Product name
        - `productline` (str): Product category/line
        - `productscale` (str): Model scale
        - `productvendor` (str): Manufacturer name
        - `productdescription` (str): Product description
        - `quantityinstock` (int): Current stock quantity
        - `buyprice` (str): Wholesale price
        - `msrp` (str): Retail price
        
        The list may be large depending on catalog size. Consider using
        `classic_models_get_product` for individual product lookups.
        
        **Example Request:**
        ```python
        products = await classic_models_list_products()
        ```
        
        **Example Response:**
        ```json
        [
            {
                "productcode": "S10_1678",
                "productname": "1969 Harley Davidson Ultimate Chopper",
                "productline": "Motorcycles",
                "productscale": "1:10",
                "productvendor": "Min Lin Diecast",
                "productdescription": "This replica features working kickstand...",
                "quantityinstock": 7933,
                "buyprice": "48.81",
                "msrp": "95.70"
            },
            {
                "productcode": "S10_1949",
                "productname": "1950's Chicago Linemaster Streetcar",
                "productline": "Trains",
                "productscale": "1:18",
                "productvendor": "Classic Metal Creations",
                "productdescription": "Highly detailed 1950's Chicago streetcar...",
                "quantityinstock": 8601,
                "buyprice": "56.24",
                "msrp": "111.15"
            }
        ]
        ```
        
        **Errors:**
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        
        **Related Tools:**
        - Use `classic_models_get_product` to get details for a specific product
        - Use `classic_models_create_product` to add new products
        """
        if api_client is None:
            raise Exception("API client not initialized")
        
        return await api_client.get("/classic-models/api/v1/products/")

