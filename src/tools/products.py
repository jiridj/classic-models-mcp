"""MCP tools for Products resource."""
from typing import Optional
from fastmcp import FastMCP
from ..api.client import APIClient


def register_product_tools(mcp: FastMCP, api_client: APIClient):
    """Register all product tools with the MCP server."""
    
    @mcp.tool()
    async def classic_models_list_products() -> list[dict]:
        """Retrieve a paginated list of all products in the Classic Models catalog.
        
        This tool returns all products available in the system with their complete
        details including pricing, inventory, descriptions, and categorization.
        Use this tool to browse the product catalog or get an overview of available inventory.
        
        **When to use:**
        - Browsing the complete product catalog
        - Getting an overview of all available products
        - Finding products by examining the full list
        - Inventory management and reporting
        
        **Parameters:**
        None - This tool requires no parameters and returns all products.
        
        **Returns:**
        A list of product dictionaries. Each product dictionary contains:
        - `productcode` (str): Unique product identifier (max 15 characters)
        - `productname` (str): Full product name (max 70 characters)
        - `productline` (str): Product category/line (e.g., "Motorcycles", "Classic Cars")
        - `productscale` (str): Model scale (e.g., "1:10", "1:18")
        - `productvendor` (str): Manufacturer name (max 50 characters)
        - `productdescription` (str): Detailed product description
        - `quantityinstock` (int): Current stock quantity (0-32767)
        - `buyprice` (str): Wholesale cost in decimal format (e.g., "48.81")
        - `msrp` (str): Manufacturer's Suggested Retail Price in decimal format (e.g., "95.70")
        
        The list may be large depending on catalog size. Consider using
        `classic_models_get_product` for individual product lookups.
        
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
            }
        ]
        ```
        
        **Errors:**
        - `401 Unauthorized`: Authentication failed (automatically retried with token refresh)
        - `500 Internal Server Error`: Server error occurred
        """
        return await api_client.get("/classic-models/api/v1/products/")
    
    
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
        return await api_client.get(f"/classic-models/api/v1/products/{productcode}/")
    
    
    @mcp.tool()
    async def classic_models_create_product(
        productcode: str,
        productname: str,
        productline: str,
        productscale: str,
        productvendor: str,
        productdescription: str,
        quantityinstock: int,
        buyprice: str,
        msrp: str,
    ) -> dict:
        """Add a new product to the Classic Models catalog with all required information.
        
        This tool creates a new product entry in the catalog. The product line must
        already exist in the system before creating products.
        
        **When to use:**
        - Adding new products to inventory
        - Expanding the product catalog
        - Creating product entries for new inventory items
        
        **Parameters:**
        - `productcode` (str, required): Unique product code identifier.
          Maximum length: 15 characters. Example: "S10_1678"
          Must be unique (not already exist)
        - `productname` (str, required): Full product name.
          Maximum length: 70 characters. Example: "1969 Harley Davidson Ultimate Chopper"
        - `productline` (str, required): Product line category this product belongs to.
          Must be an existing product line. Example: "Motorcycles"
        - `productscale` (str, required): Scale of the product model.
          Maximum length: 10 characters. Example: "1:10"
        - `productvendor` (str, required): Manufacturer or vendor name.
          Maximum length: 50 characters. Example: "Min Lin Diecast"
        - `productdescription` (str, required): Detailed description of the product
          features and specifications
        - `quantityinstock` (int, required): Current inventory quantity available in stock.
          Range: 0-32767
        - `buyprice` (str, required): Wholesale cost price in decimal format.
          Format: Decimal string. Example: "48.81"
        - `msrp` (str, required): Manufacturer's Suggested Retail Price in decimal format.
          Format: Decimal string. Example: "95.70"
        
        **Returns:**
        A dictionary containing the created product object with all fields.
        
        **Example Request:**
        ```python
        result = await classic_models_create_product(
            productcode="S10_9999",
            productname="2024 Classic Model Car",
            productline="Classic Cars",
            productscale="1:18",
            productvendor="Autoart Studio Design",
            productdescription="Detailed diecast model with opening doors and hood",
            quantityinstock=50,
            buyprice="45.99",
            msrp="89.99"
        )
        ```
        
        **Errors:**
        - `400 Bad Request`: Invalid data or missing required fields
        - `401 Unauthorized`: Authentication failed (auto-handled)
        - `409 Conflict`: Product code already exists
        - `404 Not Found`: Product line does not exist
        - `500 Internal Server Error`: Server error occurred
        
        **Related Tools:**
        - Use `classic_models_list_productlines` to see available product lines
        - Use `classic_models_get_product` to retrieve created product
        """
        data = {
            "productcode": productcode,
            "productname": productname,
            "productline": productline,
            "productscale": productscale,
            "productvendor": productvendor,
            "productdescription": productdescription,
            "quantityinstock": quantityinstock,
            "buyprice": buyprice,
            "msrp": msrp,
        }
        return await api_client.post("/classic-models/api/v1/products/", data)
    
    
    @mcp.tool()
    async def classic_models_update_product(
        productcode: str,
        productname: Optional[str] = None,
        productline: Optional[str] = None,
        productscale: Optional[str] = None,
        productvendor: Optional[str] = None,
        productdescription: Optional[str] = None,
        quantityinstock: Optional[int] = None,
        buyprice: Optional[str] = None,
        msrp: Optional[str] = None,
    ) -> dict:
        """Update specific fields of an existing product in the catalog.
        
        This tool allows partial updates to a product. Only provided fields will be updated.
        Use this for making changes to product information without affecting other fields.
        
        **When to use:**
        - Updating product prices
        - Adjusting inventory quantities
        - Modifying product descriptions
        - Changing product categorization
        
        **Parameters:**
        - `productcode` (str, required): The product code to update.
          Must be an existing product code
        - `productname` (str, optional): New product name. Maximum length: 70 characters
        - `productline` (str, optional): New product line. Must be an existing product line
        - `productscale` (str, optional): New product scale. Maximum length: 10 characters
        - `productvendor` (str, optional): New vendor name. Maximum length: 50 characters
        - `productdescription` (str, optional): New product description
        - `quantityinstock` (int, optional): Updated stock quantity. Range: 0-32767
        - `buyprice` (str, optional): Updated buy price in decimal format
        - `msrp` (str, optional): Updated MSRP in decimal format
        
        **Returns:**
        A dictionary containing the updated product object.
        
        **Example Request:**
        ```python
        result = await classic_models_update_product(
            productcode="S10_1678",
            quantityinstock=8000,
            msrp="99.99"
        )
        ```
        
        **Errors:**
        - `404 Not Found`: The product code does not exist
        - `400 Bad Request`: Invalid data
        - `404 Not Found`: Product line does not exist (if updating productline)
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        """
        data = {}
        if productname is not None:
            data["productname"] = productname
        if productline is not None:
            data["productline"] = productline
        if productscale is not None:
            data["productscale"] = productscale
        if productvendor is not None:
            data["productvendor"] = productvendor
        if productdescription is not None:
            data["productdescription"] = productdescription
        if quantityinstock is not None:
            data["quantityinstock"] = quantityinstock
        if buyprice is not None:
            data["buyprice"] = buyprice
        if msrp is not None:
            data["msrp"] = msrp
        
        return await api_client.patch(f"/classic-models/api/v1/products/{productcode}/", data)
    
    
    @mcp.tool()
    async def classic_models_delete_product(productcode: str) -> None:
        """Remove a product from the Classic Models catalog.
        
        This tool permanently deletes a product from the catalog. Use with caution
        as this may affect orders that reference this product.
        
        **When to use:**
        - Removing discontinued products
        - Cleaning up obsolete inventory items
        - Removing products that are no longer available
        
        **Parameters:**
        - `productcode` (str, required): The product code to delete.
          Must be an existing product code
        
        **Returns:**
        None - Success is indicated by no error being raised.
        
        **Example Request:**
        ```python
        await classic_models_delete_product(productcode="S10_1678")
        ```
        
        **Errors:**
        - `404 Not Found`: The product code does not exist
        - `400 Bad Request`: Cannot delete (e.g., orders still reference it)
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        
        **Warning:**
        Deleting a product may fail if order details still reference it.
        Consider updating or deleting those order details first.
        """
        await api_client.delete(f"/classic-models/api/v1/products/{productcode}/")

