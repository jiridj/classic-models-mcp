"""MCP tools for Employees resource."""
from typing import Optional
from fastmcp import FastMCP
from ..api.client import APIClient


def register_employee_tools(mcp: FastMCP, api_client: APIClient):
    """Register all employee tools with the MCP server."""
    
    @mcp.tool()
    async def classic_models_list_employees() -> list[dict]:
        """Retrieve a list of all employees in the organization with their details.
        
        This tool returns all employees in the Classic Models organization including
        their job titles, office assignments, and reporting relationships.
        
        **When to use:**
        - Viewing all employees in the organization
        - Getting employee contact information
        - Employee management and reporting
        - Organizational chart analysis
        
        **Parameters:**
        None - This tool requires no parameters and returns all employees.
        
        **Returns:**
        A list of employee dictionaries. Each dictionary contains:
        - `employeenumber` (int): Unique employee number identifier
        - `lastname` (str): Employee's last name (max 50 characters)
        - `firstname` (str): Employee's first name (max 50 characters)
        - `extension` (str): Office extension/phone extension (max 10 characters)
        - `email` (str): Employee email address (max 100 characters)
        - `jobtitle` (str): Job title/position (max 50 characters)
        - `officecode` (str): Office code where employee is assigned
        - `reportsto` (int, optional): Employee number of the manager this employee reports to
        
        **Example Response:**
        ```json
        [
            {
                "employeenumber": 1002,
                "lastname": "Murphy",
                "firstname": "Diane",
                "extension": "x5800",
                "email": "dmurphy@classicmodelcars.com",
                "jobtitle": "President",
                "officecode": "1",
                "reportsto": null
            }
        ]
        ```
        
        **Errors:**
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        """
        return await api_client.get("/classic-models/api/v1/employees/")
    
    
    @mcp.tool()
    async def classic_models_get_employee(employeenumber: int) -> dict:
        """Retrieve detailed information about a specific employee by their employee number.
        
        This tool fetches complete employee information including job details,
        office assignment, and reporting relationships.
        
        **When to use:**
        - Getting details for a specific employee
        - Verifying employee information
        - Looking up employee contact details
        - Checking reporting relationships
        
        **Parameters:**
        - `employeenumber` (int, required): The unique employee number identifier.
          Example: 1002 or 1056
          Must be an existing employee number in the system
        
        **Returns:**
        A dictionary containing the employee object with all fields.
        
        **Example Request:**
        ```python
        employee = await classic_models_get_employee(employeenumber=1002)
        ```
        
        **Errors:**
        - `404 Not Found`: The employee number does not exist
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        """
        return await api_client.get(f"/classic-models/api/v1/employees/{employeenumber}/")
    
    
    @mcp.tool()
    async def classic_models_create_employee(
        employeenumber: int,
        lastname: str,
        firstname: str,
        extension: str,
        email: str,
        jobtitle: str,
        officecode: str,
        reportsto: Optional[int] = None,
    ) -> dict:
        """Add a new employee to the organization with their job details and office assignment.
        
        This tool creates a new employee record with complete job and contact information.
        The office code must already exist in the system.
        
        **When to use:**
        - Adding new employees to the organization
        - Onboarding new hires
        - Creating employee records for new staff
        
        **Parameters:**
        - `employeenumber` (int, required): Unique employee number identifier.
          Example: 2000
          Must be unique (not already exist)
        - `lastname` (str, required): Employee's last name.
          Maximum length: 50 characters. Example: "Smith"
        - `firstname` (str, required): Employee's first name.
          Maximum length: 50 characters. Example: "John"
        - `extension` (str, required): Office extension/phone extension.
          Maximum length: 10 characters. Example: "x5800"
        - `email` (str, required): Employee email address.
          Maximum length: 100 characters. Example: "jsmith@classicmodelcars.com"
        - `jobtitle` (str, required): Job title/position.
          Maximum length: 50 characters. Example: "Sales Rep"
        - `officecode` (str, required): Office code where employee is assigned.
          Must be an existing office code. Example: "1"
        - `reportsto` (int, optional): Employee number of the manager this employee reports to.
          Must be an existing employee number if provided
        
        **Returns:**
        A dictionary containing the created employee object with all fields.
        
        **Example Request:**
        ```python
        result = await classic_models_create_employee(
            employeenumber=2000,
            lastname="Johnson",
            firstname="Jane",
            extension="x5801",
            email="jjohnson@classicmodelcars.com",
            jobtitle="Sales Manager",
            officecode="1",
            reportsto=1002
        )
        ```
        
        **Errors:**
        - `400 Bad Request`: Invalid data or missing required fields
        - `409 Conflict`: Employee number already exists
        - `404 Not Found`: Office code does not exist
        - `404 Not Found`: Manager employee number does not exist (if reportsto provided)
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        
        **Related Tools:**
        - Use `classic_models_list_offices` to see available office codes
        - Use `classic_models_list_employees` to see existing employee numbers for reportsto
        """
        data = {
            "employeenumber": employeenumber,
            "lastname": lastname,
            "firstname": firstname,
            "extension": extension,
            "email": email,
            "jobtitle": jobtitle,
            "officecode": officecode,
        }
        if reportsto is not None:
            data["reportsto"] = reportsto
        
        return await api_client.post("/classic-models/api/v1/employees/", data)
    
    
    @mcp.tool()
    async def classic_models_update_employee(
        employeenumber: int,
        lastname: Optional[str] = None,
        firstname: Optional[str] = None,
        extension: Optional[str] = None,
        email: Optional[str] = None,
        jobtitle: Optional[str] = None,
        officecode: Optional[str] = None,
        reportsto: Optional[int] = None,
    ) -> dict:
        """Update specific fields of an existing employee record.
        
        This tool allows partial updates to an employee. Only provided fields will be updated.
        Use this for making changes to employee information without affecting other fields.
        
        **When to use:**
        - Updating employee contact information
        - Changing job titles or positions
        - Reassigning employees to different offices
        - Updating reporting relationships
        
        **Parameters:**
        - `employeenumber` (int, required): The employee number to update.
          Must be an existing employee number
        - `lastname` (str, optional): Updated last name. Maximum length: 50 characters
        - `firstname` (str, optional): Updated first name. Maximum length: 50 characters
        - `extension` (str, optional): Updated extension. Maximum length: 10 characters
        - `email` (str, optional): Updated email address. Maximum length: 100 characters
        - `jobtitle` (str, optional): Updated job title. Maximum length: 50 characters
        - `officecode` (str, optional): Updated office code. Must be an existing office code
        - `reportsto` (int, optional): Updated manager employee number. Must be an existing employee number
        
        **Returns:**
        A dictionary containing the updated employee object.
        
        **Example Request:**
        ```python
        result = await classic_models_update_employee(
            employeenumber=1002,
            jobtitle="CEO",
            email="diane.murphy@classicmodelcars.com"
        )
        ```
        
        **Errors:**
        - `404 Not Found`: The employee number does not exist
        - `400 Bad Request`: Invalid data
        - `404 Not Found`: Office code does not exist (if updating officecode)
        - `404 Not Found`: Manager employee number does not exist (if updating reportsto)
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        """
        data = {}
        if lastname is not None:
            data["lastname"] = lastname
        if firstname is not None:
            data["firstname"] = firstname
        if extension is not None:
            data["extension"] = extension
        if email is not None:
            data["email"] = email
        if jobtitle is not None:
            data["jobtitle"] = jobtitle
        if officecode is not None:
            data["officecode"] = officecode
        if reportsto is not None:
            data["reportsto"] = reportsto
        
        return await api_client.patch(f"/classic-models/api/v1/employees/{employeenumber}/", data)
    
    
    @mcp.tool()
    async def classic_models_delete_employee(employeenumber: int) -> None:
        """Remove an employee from the organization.
        
        This tool permanently deletes an employee record. Use with caution as this
        may affect customers assigned to this employee as sales rep.
        
        **When to use:**
        - Removing terminated employees
        - Cleaning up obsolete employee records
        - Removing employees who have left the organization
        
        **Parameters:**
        - `employeenumber` (int, required): The employee number to delete.
          Must be an existing employee number
        
        **Returns:**
        None - Success is indicated by no error being raised.
        
        **Example Request:**
        ```python
        await classic_models_delete_employee(employeenumber=2000)
        ```
        
        **Errors:**
        - `404 Not Found`: The employee number does not exist
        - `400 Bad Request`: Cannot delete (e.g., customers still assigned as sales rep)
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        
        **Warning:**
        Deleting an employee may fail if customers are still assigned to them as sales rep.
        Consider reassigning those customers first.
        """
        await api_client.delete(f"/classic-models/api/v1/employees/{employeenumber}/")

