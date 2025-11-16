"""MCP tools for Customers resource."""
from typing import Optional
from fastmcp import FastMCP
from ..api.client import APIClient


def register_customer_tools(mcp: FastMCP, api_client: APIClient):
    """Register all customer tools with the MCP server."""
    
    @mcp.tool()
    async def classic_models_list_customers() -> list[dict]:
        """Retrieve a list of all customers with their contact and credit information.
        
        This tool returns all customers in the Classic Models system including
        their contact details, addresses, and credit limits.
        
        **When to use:**
        - Viewing all customers in the system
        - Getting customer contact information
        - Customer management and reporting
        - Credit limit analysis
        
        **Parameters:**
        None - This tool requires no parameters and returns all customers.
        
        **Returns:**
        A list of customer dictionaries. Each dictionary contains:
        - `customernumber` (int): Unique customer number identifier
        - `customername` (str): Customer company name (max 50 characters)
        - `contactlastname` (str): Contact person's last name (max 50 characters)
        - `contactfirstname` (str): Contact person's first name (max 50 characters)
        - `phone` (str): Contact phone number (max 50 characters)
        - `addressline1` (str): Primary street address (max 50 characters)
        - `addressline2` (str, optional): Secondary address line (max 50 characters)
        - `city` (str): City name (max 50 characters)
        - `state` (str, optional): State or province (max 50 characters)
        - `postalcode` (str, optional): Postal/ZIP code (max 15 characters)
        - `country` (str): Country name (max 50 characters)
        - `creditlimit` (str, optional): Credit limit in decimal format
        - `salesrepemployeenumber` (int, optional): Employee number of assigned sales rep
        
        **Example Response:**
        ```json
        [
            {
                "customernumber": 103,
                "customername": "Atelier graphique",
                "contactlastname": "Schmitt",
                "contactfirstname": "Carine",
                "phone": "40.32.2555",
                "addressline1": "54, rue Royale",
                "addressline2": null,
                "city": "Nantes",
                "state": null,
                "postalcode": "44000",
                "country": "France",
                "creditlimit": "21000.00",
                "salesrepemployeenumber": 1370
            }
        ]
        ```
        
        **Errors:**
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        """
        return await api_client.get("/classic-models/api/v1/customers/")
    
    
    @mcp.tool()
    async def classic_models_get_customer(customernumber: int) -> dict:
        """Retrieve detailed information about a specific customer by their customer number.
        
        This tool fetches complete customer information including contact details,
        address, credit limit, and assigned sales representative.
        
        **When to use:**
        - Getting details for a specific customer
        - Verifying customer information
        - Looking up customer contact details
        - Checking credit limits before processing orders
        
        **Parameters:**
        - `customernumber` (int, required): The unique customer number identifier.
          Example: 103 or 112
          Must be an existing customer number in the system
        
        **Returns:**
        A dictionary containing the customer object with all fields.
        
        **Example Request:**
        ```python
        customer = await classic_models_get_customer(customernumber=103)
        ```
        
        **Errors:**
        - `404 Not Found`: The customer number does not exist
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        """
        return await api_client.get(f"/classic-models/api/v1/customers/{customernumber}/")
    
    
    @mcp.tool()
    async def classic_models_create_customer(
        customernumber: int,
        customername: str,
        contactlastname: str,
        contactfirstname: str,
        phone: str,
        addressline1: str,
        city: str,
        country: str,
        addressline2: Optional[str] = None,
        state: Optional[str] = None,
        postalcode: Optional[str] = None,
        creditlimit: Optional[str] = None,
        salesrepemployeenumber: Optional[int] = None,
    ) -> dict:
        """Add a new customer to the system with their contact details and credit limit.
        
        This tool creates a new customer record with complete contact and address information.
        The sales rep employee number must be an existing employee if provided.
        
        **When to use:**
        - Adding new customers to the system
        - Onboarding new clients
        - Creating customer records for new accounts
        
        **Parameters:**
        - `customernumber` (int, required): Unique customer number identifier.
          Example: 500
          Must be unique (not already exist)
        - `customername` (str, required): Customer company name.
          Maximum length: 50 characters. Example: "ABC Corporation"
        - `contactlastname` (str, required): Contact person's last name.
          Maximum length: 50 characters. Example: "Smith"
        - `contactfirstname` (str, required): Contact person's first name.
          Maximum length: 50 characters. Example: "John"
        - `phone` (str, required): Contact phone number.
          Maximum length: 50 characters. Example: "+1 555 123 4567"
        - `addressline1` (str, required): Primary street address.
          Maximum length: 50 characters. Example: "123 Main Street"
        - `city` (str, required): City name.
          Maximum length: 50 characters. Example: "New York"
        - `country` (str, required): Country name.
          Maximum length: 50 characters. Example: "USA"
        - `addressline2` (str, optional): Secondary address line.
          Maximum length: 50 characters. Example: "Suite 100"
        - `state` (str, optional): State or province.
          Maximum length: 50 characters. Example: "NY"
        - `postalcode` (str, optional): Postal/ZIP code.
          Maximum length: 15 characters. Example: "10001"
        - `creditlimit` (str, optional): Credit limit in decimal format.
          Example: "50000.00"
        - `salesrepemployeenumber` (int, optional): Employee number of assigned sales rep.
          Must be an existing employee number if provided
        
        **Returns:**
        A dictionary containing the created customer object with all fields.
        
        **Example Request:**
        ```python
        result = await classic_models_create_customer(
            customernumber=500,
            customername="New Customer Inc",
            contactlastname="Doe",
            contactfirstname="Jane",
            phone="+1 555 987 6543",
            addressline1="456 Business Ave",
            city="Chicago",
            state="IL",
            country="USA",
            postalcode="60601",
            creditlimit="25000.00",
            salesrepemployeenumber=1370
        )
        ```
        
        **Errors:**
        - `400 Bad Request`: Invalid data or missing required fields
        - `409 Conflict`: Customer number already exists
        - `404 Not Found`: Sales rep employee number does not exist (if provided)
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        
        **Related Tools:**
        - Use `classic_models_list_employees` to see available sales rep employee numbers
        """
        data = {
            "customernumber": customernumber,
            "customername": customername,
            "contactlastname": contactlastname,
            "contactfirstname": contactfirstname,
            "phone": phone,
            "addressline1": addressline1,
            "city": city,
            "country": country,
        }
        if addressline2 is not None:
            data["addressline2"] = addressline2
        if state is not None:
            data["state"] = state
        if postalcode is not None:
            data["postalcode"] = postalcode
        if creditlimit is not None:
            data["creditlimit"] = creditlimit
        if salesrepemployeenumber is not None:
            data["salesrepemployeenumber"] = salesrepemployeenumber
        
        return await api_client.post("/classic-models/api/v1/customers/", data)
    
    
    @mcp.tool()
    async def classic_models_update_customer(
        customernumber: int,
        customername: Optional[str] = None,
        contactlastname: Optional[str] = None,
        contactfirstname: Optional[str] = None,
        phone: Optional[str] = None,
        addressline1: Optional[str] = None,
        addressline2: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        postalcode: Optional[str] = None,
        country: Optional[str] = None,
        creditlimit: Optional[str] = None,
        salesrepemployeenumber: Optional[int] = None,
    ) -> dict:
        """Update specific fields of an existing customer record.
        
        This tool allows partial updates to a customer. Only provided fields will be updated.
        Use this for making changes to customer information without affecting other fields.
        
        **When to use:**
        - Updating customer contact information
        - Changing customer addresses
        - Adjusting credit limits
        - Reassigning sales representatives
        
        **Parameters:**
        - `customernumber` (int, required): The customer number to update.
          Must be an existing customer number
        - `customername` (str, optional): Updated company name. Maximum length: 50 characters
        - `contactlastname` (str, optional): Updated contact last name. Maximum length: 50 characters
        - `contactfirstname` (str, optional): Updated contact first name. Maximum length: 50 characters
        - `phone` (str, optional): Updated phone number. Maximum length: 50 characters
        - `addressline1` (str, optional): Updated primary address. Maximum length: 50 characters
        - `addressline2` (str, optional): Updated secondary address. Maximum length: 50 characters
        - `city` (str, optional): Updated city name. Maximum length: 50 characters
        - `state` (str, optional): Updated state/province. Maximum length: 50 characters
        - `postalcode` (str, optional): Updated postal code. Maximum length: 15 characters
        - `country` (str, optional): Updated country name. Maximum length: 50 characters
        - `creditlimit` (str, optional): Updated credit limit in decimal format
        - `salesrepemployeenumber` (int, optional): Updated sales rep employee number. Must be an existing employee number
        
        **Returns:**
        A dictionary containing the updated customer object.
        
        **Example Request:**
        ```python
        result = await classic_models_update_customer(
            customernumber=103,
            phone="40.32.2556",
            creditlimit="25000.00"
        )
        ```
        
        **Errors:**
        - `404 Not Found`: The customer number does not exist
        - `400 Bad Request`: Invalid data
        - `404 Not Found`: Sales rep employee number does not exist (if updating salesrepemployeenumber)
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        """
        data = {}
        if customername is not None:
            data["customername"] = customername
        if contactlastname is not None:
            data["contactlastname"] = contactlastname
        if contactfirstname is not None:
            data["contactfirstname"] = contactfirstname
        if phone is not None:
            data["phone"] = phone
        if addressline1 is not None:
            data["addressline1"] = addressline1
        if addressline2 is not None:
            data["addressline2"] = addressline2
        if city is not None:
            data["city"] = city
        if state is not None:
            data["state"] = state
        if postalcode is not None:
            data["postalcode"] = postalcode
        if country is not None:
            data["country"] = country
        if creditlimit is not None:
            data["creditlimit"] = creditlimit
        if salesrepemployeenumber is not None:
            data["salesrepemployeenumber"] = salesrepemployeenumber
        
        return await api_client.patch(f"/classic-models/api/v1/customers/{customernumber}/", data)
    
    
    @mcp.tool()
    async def classic_models_delete_customer(customernumber: int) -> None:
        """Remove a customer from the system.
        
        This tool permanently deletes a customer record. Use with caution as this
        may affect orders and payments associated with this customer.
        
        **When to use:**
        - Removing inactive customers
        - Cleaning up obsolete customer records
        - Removing customers who are no longer active
        
        **Parameters:**
        - `customernumber` (int, required): The customer number to delete.
          Must be an existing customer number
        
        **Returns:**
        None - Success is indicated by no error being raised.
        
        **Example Request:**
        ```python
        await classic_models_delete_customer(customernumber=500)
        ```
        
        **Errors:**
        - `404 Not Found`: The customer number does not exist
        - `400 Bad Request`: Cannot delete (e.g., orders still exist for this customer)
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        
        **Warning:**
        Deleting a customer may fail if orders or payments still exist for this customer.
        Consider handling those records first.
        """
        await api_client.delete(f"/classic-models/api/v1/customers/{customernumber}/")

