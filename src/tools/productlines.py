"""MCP tools for Product Lines resource."""
from typing import Optional
from fastmcp import FastMCP
from ..api.client import APIClient


def register_productline_tools(mcp: FastMCP, api_client: APIClient):
    """Register all product line tools with the MCP server."""
    
    @mcp.tool()
    async def classic_models_list_productlines() -> list[dict]:
        """Retrieve a list of all product line categories in the Classic Models system.
        
        This tool returns all product line categories available in the system.
        Product lines are used to categorize products (e.g., "Motorcycles", "Classic Cars", "Planes").
        
        **When to use:**
        - Browsing available product categories
        - Getting a list of product lines before creating products
        - Category management and reporting
        
        **Parameters:**
        None - This tool requires no parameters and returns all product lines.
        
        **Returns:**
        A list of product line dictionaries. Each dictionary contains:
        - `productline` (str): Unique product line identifier (max 50 characters)
        - `textdescription` (str, optional): Text description of the product line
        - `htmldescription` (str, optional): HTML description of the product line
        - `image` (str, optional): Base64-encoded image of the product line
        
        **Example Response:**
        ```json
        [
            {
                "productline": "Motorcycles",
                "textdescription": "Motorcycles and bikes",
                "htmldescription": "<p>Motorcycles and bikes</p>",
                "image": null
            }
        ]
        ```
        
        **Errors:**
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        """
        return await api_client.get("/classic-models/api/v1/productlines/")
    
    
    @mcp.tool()
    async def classic_models_get_productline(productline: str) -> dict:
        """Retrieve detailed information about a specific product line by its identifier.
        
        This tool fetches complete product line information including descriptions
        and image data from the Classic Models system.
        
        **When to use:**
        - Getting details for a specific product line
        - Verifying a product line exists before creating products
        - Viewing product line descriptions and images
        
        **Parameters:**
        - `productline` (str, required): The unique product line identifier.
          Example: "Motorcycles" or "Classic Cars"
          Maximum length: 50 characters
          Must be an existing product line in the system
        
        **Returns:**
        A dictionary containing the product line object with:
        - `productline` (str): The product line identifier
        - `textdescription` (str, optional): Text description
        - `htmldescription` (str, optional): HTML description
        - `image` (str, optional): Base64-encoded image
        
        **Example Request:**
        ```python
        result = await classic_models_get_productline(productline="Motorcycles")
        ```
        
        **Errors:**
        - `404 Not Found`: The product line does not exist
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        """
        return await api_client.get(f"/classic-models/api/v1/productlines/{productline}/")
    
    
    @mcp.tool()
    async def classic_models_create_productline(
        productline: str,
        textdescription: Optional[str] = None,
        htmldescription: Optional[str] = None,
    ) -> dict:
        """Add a new product line category to the Classic Models system.
        
        This tool creates a new product line category that can be used to organize products.
        Product lines are required when creating products.
        
        **When to use:**
        - Adding new product categories
        - Creating product lines for new product types
        - Expanding the product categorization system
        
        **Parameters:**
        - `productline` (str, required): Unique product line identifier.
          Example: "Electric Vehicles" or "Vintage Models"
          Maximum length: 50 characters
          Must be unique (not already exist)
        - `textdescription` (str, optional): Plain text description of the product line.
          Maximum length: 4000 characters
        - `htmldescription` (str, optional): HTML-formatted description of the product line.
          Can include HTML tags for formatting
        
        **Returns:**
        A dictionary containing the created product line object with all fields.
        
        **Example Request:**
        ```python
        result = await classic_models_create_productline(
            productline="Electric Vehicles",
            textdescription="Modern electric vehicle models",
            htmldescription="<p>Modern electric vehicle models</p>"
        )
        ```
        
        **Errors:**
        - `400 Bad Request`: Invalid data or missing required fields
        - `409 Conflict`: Product line already exists
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        """
        data = {
            "productline": productline,
        }
        if textdescription is not None:
            data["textdescription"] = textdescription
        if htmldescription is not None:
            data["htmldescription"] = htmldescription
        
        return await api_client.post("/classic-models/api/v1/productlines/", data)
    
    
    @mcp.tool()
    async def classic_models_update_productline(
        productline: str,
        textdescription: Optional[str] = None,
        htmldescription: Optional[str] = None,
    ) -> dict:
        """Update specific fields of an existing product line.
        
        This tool allows partial updates to a product line. Only provided fields will be updated.
        Use this for making changes to descriptions without affecting other fields.
        
        **When to use:**
        - Updating product line descriptions
        - Modifying HTML descriptions
        - Making partial updates to product line information
        
        **Parameters:**
        - `productline` (str, required): The product line identifier to update.
          Must be an existing product line
        - `textdescription` (str, optional): New text description.
          Maximum length: 4000 characters
          If not provided, existing value is preserved
        - `htmldescription` (str, optional): New HTML description.
          If not provided, existing value is preserved
        
        **Returns:**
        A dictionary containing the updated product line object.
        
        **Example Request:**
        ```python
        result = await classic_models_update_productline(
            productline="Motorcycles",
            textdescription="Updated description of motorcycles"
        )
        ```
        
        **Errors:**
        - `404 Not Found`: The product line does not exist
        - `400 Bad Request`: Invalid data
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        """
        data = {}
        if textdescription is not None:
            data["textdescription"] = textdescription
        if htmldescription is not None:
            data["htmldescription"] = htmldescription
        
        return await api_client.patch(f"/classic-models/api/v1/productlines/{productline}/", data)
    
    
    @mcp.tool()
    async def classic_models_delete_productline(productline: str) -> None:
        """Remove a product line from the Classic Models system.
        
        This tool permanently deletes a product line. Use with caution as this
        may affect products that reference this product line.
        
        **When to use:**
        - Removing obsolete product categories
        - Cleaning up unused product lines
        - Reorganizing product categorization
        
        **Parameters:**
        - `productline` (str, required): The product line identifier to delete.
          Must be an existing product line
        
        **Returns:**
        None - Success is indicated by no error being raised.
        
        **Example Request:**
        ```python
        await classic_models_delete_productline(productline="Obsolete Category")
        ```
        
        **Errors:**
        - `404 Not Found`: The product line does not exist
        - `400 Bad Request`: Cannot delete (e.g., products still reference it)
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        
        **Warning:**
        Deleting a product line may fail if products still reference it.
        Consider updating or deleting those products first.
        """
        await api_client.delete(f"/classic-models/api/v1/productlines/{productline}/")

