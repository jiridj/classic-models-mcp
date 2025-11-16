"""MCP tools for Offices resource."""
from typing import Optional
from fastmcp import FastMCP
from ..api.client import APIClient


def register_office_tools(mcp: FastMCP, api_client: APIClient):
    """Register all office tools with the MCP server."""
    
    @mcp.tool()
    async def classic_models_list_offices() -> list[dict]:
        """Retrieve a list of all company office locations worldwide.
        
        This tool returns all office locations in the Classic Models company network
        with their complete address and contact information.
        
        **When to use:**
        - Viewing all company office locations
        - Getting office contact information
        - Office management and reporting
        
        **Parameters:**
        None - This tool requires no parameters and returns all offices.
        
        **Returns:**
        A list of office dictionaries. Each dictionary contains:
        - `officecode` (str): Unique office code identifier (max 10 characters)
        - `city` (str): City where the office is located (max 50 characters)
        - `phone` (str): Office phone number (max 50 characters)
        - `addressline1` (str): Primary street address (max 50 characters)
        - `addressline2` (str, optional): Secondary address line (max 50 characters)
        - `state` (str, optional): State or province (max 50 characters)
        - `country` (str): Country name (max 50 characters)
        - `postalcode` (str): Postal/ZIP code (max 15 characters)
        - `territory` (str): Sales territory (max 10 characters)
        
        **Example Response:**
        ```json
        [
            {
                "officecode": "1",
                "city": "San Francisco",
                "phone": "+1 650 219 4782",
                "addressline1": "100 Market Street",
                "addressline2": "Suite 300",
                "state": "CA",
                "country": "USA",
                "postalcode": "94080",
                "territory": "NA"
            }
        ]
        ```
        
        **Errors:**
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        """
        return await api_client.get("/classic-models/api/v1/offices/")
    
    
    @mcp.tool()
    async def classic_models_get_office(officecode: str) -> dict:
        """Retrieve detailed information about a specific office by its code.
        
        This tool fetches complete office information including address, contact details,
        and territory information from the Classic Models system.
        
        **When to use:**
        - Getting details for a specific office location
        - Verifying office information
        - Looking up office contact details
        
        **Parameters:**
        - `officecode` (str, required): The unique office code identifier.
          Example: "1" or "2"
          Maximum length: 10 characters
          Must be an existing office code in the system
        
        **Returns:**
        A dictionary containing the office object with all address and contact fields.
        
        **Example Request:**
        ```python
        office = await classic_models_get_office(officecode="1")
        ```
        
        **Errors:**
        - `404 Not Found`: The office code does not exist
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        """
        return await api_client.get(f"/classic-models/api/v1/offices/{officecode}/")
    
    
    @mcp.tool()
    async def classic_models_create_office(
        officecode: str,
        city: str,
        phone: str,
        addressline1: str,
        country: str,
        postalcode: str,
        territory: str,
        addressline2: Optional[str] = None,
        state: Optional[str] = None,
    ) -> dict:
        """Add a new office location to the company's network.
        
        This tool creates a new office location with complete address and contact information.
        Offices are used to organize employees and manage regional operations.
        
        **When to use:**
        - Adding new office locations
        - Expanding the company network
        - Creating office entries for new locations
        
        **Parameters:**
        - `officecode` (str, required): Unique office code identifier.
          Maximum length: 10 characters. Example: "3"
          Must be unique (not already exist)
        - `city` (str, required): City where the office is located.
          Maximum length: 50 characters. Example: "New York"
        - `phone` (str, required): Office phone number.
          Maximum length: 50 characters. Example: "+1 212 555 1234"
        - `addressline1` (str, required): Primary street address.
          Maximum length: 50 characters. Example: "123 Main Street"
        - `country` (str, required): Country name.
          Maximum length: 50 characters. Example: "USA"
        - `postalcode` (str, required): Postal/ZIP code.
          Maximum length: 15 characters. Example: "10001"
        - `territory` (str, required): Sales territory code.
          Maximum length: 10 characters. Example: "NA" or "EMEA"
        - `addressline2` (str, optional): Secondary address line.
          Maximum length: 50 characters. Example: "Suite 500"
        - `state` (str, optional): State or province.
          Maximum length: 50 characters. Example: "NY"
        
        **Returns:**
        A dictionary containing the created office object with all fields.
        
        **Example Request:**
        ```python
        result = await classic_models_create_office(
            officecode="3",
            city="Chicago",
            phone="+1 312 555 5678",
            addressline1="456 Business Ave",
            addressline2="Floor 10",
            state="IL",
            country="USA",
            postalcode="60601",
            territory="NA"
        )
        ```
        
        **Errors:**
        - `400 Bad Request`: Invalid data or missing required fields
        - `409 Conflict`: Office code already exists
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        """
        data = {
            "officecode": officecode,
            "city": city,
            "phone": phone,
            "addressline1": addressline1,
            "country": country,
            "postalcode": postalcode,
            "territory": territory,
        }
        if addressline2 is not None:
            data["addressline2"] = addressline2
        if state is not None:
            data["state"] = state
        
        return await api_client.post("/classic-models/api/v1/offices/", data)
    
    
    @mcp.tool()
    async def classic_models_update_office(
        officecode: str,
        city: Optional[str] = None,
        phone: Optional[str] = None,
        addressline1: Optional[str] = None,
        addressline2: Optional[str] = None,
        state: Optional[str] = None,
        country: Optional[str] = None,
        postalcode: Optional[str] = None,
        territory: Optional[str] = None,
    ) -> dict:
        """Update specific fields of an existing office location.
        
        This tool allows partial updates to an office. Only provided fields will be updated.
        Use this for making changes to office information without affecting other fields.
        
        **When to use:**
        - Updating office addresses
        - Changing contact information
        - Modifying territory assignments
        - Making partial updates to office details
        
        **Parameters:**
        - `officecode` (str, required): The office code to update.
          Must be an existing office code
        - `city` (str, optional): Updated city name. Maximum length: 50 characters
        - `phone` (str, optional): Updated phone number. Maximum length: 50 characters
        - `addressline1` (str, optional): Updated primary address. Maximum length: 50 characters
        - `addressline2` (str, optional): Updated secondary address. Maximum length: 50 characters
        - `state` (str, optional): Updated state/province. Maximum length: 50 characters
        - `country` (str, optional): Updated country name. Maximum length: 50 characters
        - `postalcode` (str, optional): Updated postal code. Maximum length: 15 characters
        - `territory` (str, optional): Updated territory code. Maximum length: 10 characters
        
        **Returns:**
        A dictionary containing the updated office object.
        
        **Example Request:**
        ```python
        result = await classic_models_update_office(
            officecode="1",
            phone="+1 650 219 4783",
            addressline2="Suite 400"
        )
        ```
        
        **Errors:**
        - `404 Not Found`: The office code does not exist
        - `400 Bad Request`: Invalid data
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        """
        data = {}
        if city is not None:
            data["city"] = city
        if phone is not None:
            data["phone"] = phone
        if addressline1 is not None:
            data["addressline1"] = addressline1
        if addressline2 is not None:
            data["addressline2"] = addressline2
        if state is not None:
            data["state"] = state
        if country is not None:
            data["country"] = country
        if postalcode is not None:
            data["postalcode"] = postalcode
        if territory is not None:
            data["territory"] = territory
        
        return await api_client.patch(f"/classic-models/api/v1/offices/{officecode}/", data)
    
    
    @mcp.tool()
    async def classic_models_delete_office(officecode: str) -> None:
        """Remove an office location from the company network.
        
        This tool permanently deletes an office location. Use with caution as this
        may affect employees assigned to this office.
        
        **When to use:**
        - Removing closed office locations
        - Cleaning up obsolete office entries
        - Reorganizing the company network
        
        **Parameters:**
        - `officecode` (str, required): The office code to delete.
          Must be an existing office code
        
        **Returns:**
        None - Success is indicated by no error being raised.
        
        **Example Request:**
        ```python
        await classic_models_delete_office(officecode="3")
        ```
        
        **Errors:**
        - `404 Not Found`: The office code does not exist
        - `400 Bad Request`: Cannot delete (e.g., employees still assigned)
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        
        **Warning:**
        Deleting an office may fail if employees are still assigned to it.
        Consider reassigning or removing those employees first.
        """
        await api_client.delete(f"/classic-models/api/v1/offices/{officecode}/")

