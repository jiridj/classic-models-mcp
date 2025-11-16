# Tool Documentation Guide

> 📖 **Navigation:** [Documentation Index](README.md) | [Main README](../README.md)

Best practices for writing clear, LLM-friendly documentation for MCP tools.

---

## 🎯 Why Good Documentation Matters

Good documentation helps LLMs:
- ✅ Understand what each tool does
- ✅ Know when to use each tool
- ✅ Provide correct parameters
- ✅ Handle errors properly
- ✅ Suggest related tools

---

## 📋 Key Principles

### 1. **Comprehensive Docstrings**
- Start with a clear, one-sentence summary
- Follow with detailed description of what the tool does
- Explain when and why to use the tool
- Include example use cases

### 2. **Detailed Parameter Documentation**
- Use type hints (Python types or Pydantic models)
- Provide clear parameter descriptions
- Include examples of valid values
- Specify required vs optional parameters
- Explain constraints (min/max values, formats, etc.)

### 3. **Return Value Documentation**
- Clearly describe what the tool returns
- Specify the structure/format of the response
- Include example return values
- Document possible error responses

### 4. **Use Pydantic Models**
- Define request/response models with field descriptions
- Use field validators and constraints
- Provide default values where appropriate
- Use enums for constrained values

### 5. **Clear, Unambiguous Language**
- Avoid pronouns ("it", "this") - use specific nouns
- Use consistent terminology throughout
- Define acronyms on first use
- Avoid jargon or explain technical terms

### 6. **Examples in Documentation**
- Include realistic examples in docstrings
- Show both simple and complex use cases
- Demonstrate edge cases when relevant

## Example: Well-Documented Tool

Here's an example of a well-documented tool following these principles:

```python
from pydantic import BaseModel, Field
from typing import Optional
from fastmcp import FastMCP

class ProductCreateRequest(BaseModel):
    """Request model for creating a new product.
    
    All fields except optional ones are required to create a product in the catalog.
    """
    productcode: str = Field(
        ...,
        description="Unique product code identifier (max 15 characters). Example: 'S10_1678'",
        max_length=15,
        min_length=1
    )
    productname: str = Field(
        ...,
        description="Full name of the product. Example: '1969 Harley Davidson Ultimate Chopper'",
        max_length=70,
        min_length=1
    )
    productline: str = Field(
        ...,
        description="Product line category this product belongs to. Must be an existing product line. Example: 'Motorcycles'"
    )
    productscale: str = Field(
        ...,
        description="Scale of the product model. Example: '1:10'",
        max_length=10
    )
    productvendor: str = Field(
        ...,
        description="Manufacturer or vendor name. Example: 'Min Lin Diecast'",
        max_length=50
    )
    productdescription: str = Field(
        ...,
        description="Detailed description of the product features and specifications"
    )
    quantityinstock: int = Field(
        ...,
        description="Current inventory quantity available in stock",
        ge=0,
        le=32767
    )
    buyprice: str = Field(
        ...,
        description="Wholesale cost price in decimal format. Example: '48.81'",
        pattern=r'^-?\d{0,8}(?:\.\d{0,2})?$'
    )
    msrp: str = Field(
        ...,
        description="Manufacturer's Suggested Retail Price in decimal format. Example: '95.70'",
        pattern=r'^-?\d{0,8}(?:\.\d{0,2})?$'
    )


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
    """Create a new product in the Classic Models catalog.
    
    This tool adds a new product to the product catalog with all required information.
    The product code must be unique and the product line must already exist in the system.
    
    **When to use:**
    - Adding new products to inventory
    - Expanding the product catalog
    - Creating product entries for new inventory items
    
    **Parameters:**
    - `productcode`: Unique identifier for the product (required, max 15 chars)
    - `productname`: Full product name (required, max 70 chars)
    - `productline`: Category/line the product belongs to (required, must exist)
    - `productscale`: Scale of the model (required, e.g., "1:10")
    - `productvendor`: Manufacturer name (required, max 50 chars)
    - `productdescription`: Detailed product description (required)
    - `quantityinstock`: Current inventory count (required, 0-32767)
    - `buyprice`: Wholesale cost in decimal format (required, e.g., "48.81")
    - `msrp`: Retail price in decimal format (required, e.g., "95.70")
    
    **Returns:**
    A dictionary containing the created product object with all fields including:
    - `productcode`: The product code
    - `productname`: The product name
    - All other product fields as provided
    
    **Example:**
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
    """
    if api_client is None:
        raise Exception("API client not initialized")
    
    product_data = {
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
    
    return await api_client.post("/classic-models/api/v1/products/", product_data)
```

## Documentation Template

Use this template for consistent tool documentation:

```python
@mcp.tool()
async def tool_name(
    param1: type,
    param2: Optional[type] = None,
) -> dict:
    """One-sentence summary of what the tool does.
    
    Detailed description explaining:
    - What the tool does
    - When to use it
    - What problem it solves
    
    **When to use:**
    - Specific scenario 1
    - Specific scenario 2
    - Specific scenario 3
    
    **Parameters:**
    - `param1`: Description of param1 (required/optional). Example: "example_value"
    - `param2`: Description of param2 (required/optional). Example: "example_value"
    
    **Returns:**
    Description of return value structure and format.
    
    **Example:**
    ```python
    result = await tool_name(
        param1="value1",
        param2="value2"
    )
    ```
    
    **Errors:**
    - `400`: Description of when this error occurs
    - `404`: Description of when this error occurs
    - `500`: Description of when this error occurs
    """
    # Implementation
```

## FastMCP-Specific Features

### Using Tool Annotations

FastMCP supports additional metadata through annotations:

```python
@mcp.tool(
    name="custom_tool_name",  # Override function name
    description="Custom description",  # Override docstring description
    tags={"category": "products", "operation": "create"},
)
async def my_tool():
    """Tool implementation"""
    pass
```

### Type Hints with Pydantic

FastMCP automatically uses Pydantic models for validation:

```python
from pydantic import BaseModel, Field

class ProductUpdate(BaseModel):
    productname: Optional[str] = Field(None, description="New product name")
    quantityinstock: Optional[int] = Field(None, ge=0, description="Updated stock quantity")

@mcp.tool()
async def update_product(
    productcode: str,
    updates: ProductUpdate
) -> dict:
    """Update product fields."""
    pass
```

## Checklist for Tool Documentation

- [ ] Clear, concise one-sentence summary
- [ ] Detailed description of functionality
- [ ] "When to use" section
- [ ] All parameters documented with types
- [ ] Parameter examples provided
- [ ] Return value structure documented
- [ ] Example usage included
- [ ] Error cases documented
- [ ] Type hints on all parameters
- [ ] Pydantic models for complex types
- [ ] Field descriptions in Pydantic models
- [ ] No ambiguous pronouns
- [ ] Consistent terminology
- [ ] Acronyms defined

## Additional Tips

1. **Use Enum Types**: For constrained values, use Python enums:
   ```python
   from enum import Enum
   
   class OrderStatus(str, Enum):
       """Order status values."""
       PENDING = "Pending"
       SHIPPED = "Shipped"
       CANCELLED = "Cancelled"
   ```

2. **Document Relationships**: Explain how tools relate to each other:
   ```python
   """Create a new order.
   
   Note: Before creating an order, ensure the customer exists using
   `classic_models_get_customer`. Products must exist before adding
   them to order details.
   """
   ```

3. **Include Validation Rules**: Document constraints clearly:
   ```python
   customernumber: int = Field(
       ...,
       description="Unique customer identifier (positive integer)",
       gt=0
   )
   ```

4. **Provide Context**: Explain business logic when relevant:
   ```python
   """Update product inventory.
   
   This tool updates the quantity in stock. Use negative values to
   reduce inventory (e.g., when items are sold) and positive values
   to increase inventory (e.g., when restocking).
   """
   ```

