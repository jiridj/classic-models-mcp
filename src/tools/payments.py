"""MCP tools for Payments resource."""
from typing import Optional
from fastmcp import FastMCP
from ..api.client import APIClient


def register_payment_tools(mcp: FastMCP, api_client: APIClient):
    """Register all payment tools with the MCP server."""
    
    @mcp.tool()
    async def classic_models_get_payment(customernumber: int, checknumber: str) -> dict:
        """Retrieve detailed information about a specific payment by customer number and check number.
        
        This tool fetches complete payment information including payment date,
        amount, and customer details.
        
        **When to use:**
        - Getting details for a specific payment
        - Verifying payment information
        - Looking up payment records for accounting
        - Checking payment history for a customer
        
        **Parameters:**
        - `customernumber` (int, required): The customer number who made the payment.
          Must be an existing customer number in the system
        - `checknumber` (str, required): The check number or payment identifier.
          Example: "HQ336336" or "JM555205"
          Maximum length: 50 characters
          Must be an existing check number for this customer
        
        **Returns:**
        A dictionary containing the payment object with:
        - `id` (int): Internal payment identifier
        - `checknumber` (str): The check number
        - `paymentdate` (str): Date when payment was made (YYYY-MM-DD format)
        - `amount` (str): Payment amount in decimal format
        - `customernumber` (int): Customer number who made the payment
        
        **Example Request:**
        ```python
        payment = await classic_models_get_payment(
            customernumber=103,
            checknumber="HQ336336"
        )
        ```
        
        **Example Response:**
        ```json
        {
            "id": 1,
            "checknumber": "HQ336336",
            "paymentdate": "2004-10-19",
            "amount": "6066.78",
            "customernumber": 103
        }
        ```
        
        **Errors:**
        - `404 Not Found`: The payment does not exist for this customer/check number combination
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        
        **Related Tools:**
        - Use `classic_models_list_customers` to see available customer numbers
        """
        return await api_client.get(f"/classic-models/api/v1/payments/{customernumber}/{checknumber}/")
    
    
    @mcp.tool()
    async def classic_models_update_payment(
        customernumber: int,
        checknumber: str,
        paymentdate: Optional[str] = None,
        amount: Optional[str] = None,
    ) -> dict:
        """Update specific fields of an existing payment record.
        
        This tool allows partial updates to a payment. Only provided fields will be updated.
        Use this for making corrections to payment information.
        
        **When to use:**
        - Correcting payment dates
        - Adjusting payment amounts
        - Making corrections to payment records
        
        **Parameters:**
        - `customernumber` (int, required): The customer number of the payment to update.
          Must be an existing customer number
        - `checknumber` (str, required): The check number of the payment to update.
          Must be an existing check number for this customer
        - `paymentdate` (str, optional): Updated payment date.
          Format: YYYY-MM-DD. Example: "2024-01-15"
        - `amount` (str, optional): Updated payment amount in decimal format.
          Example: "1000.00"
        
        **Returns:**
        A dictionary containing the updated payment object.
        
        **Example Request:**
        ```python
        result = await classic_models_update_payment(
            customernumber=103,
            checknumber="HQ336336",
            amount="6100.00"
        )
        ```
        
        **Errors:**
        - `404 Not Found`: The payment does not exist for this customer/check number combination
        - `400 Bad Request`: Invalid data
        - `401 Unauthorized`: Authentication failed (automatically retried)
        - `500 Internal Server Error`: Server error occurred
        
        **Note:**
        Payments are typically created through the payment processing system.
        This tool is primarily for corrections and adjustments.
        """
        data = {}
        if paymentdate is not None:
            data["paymentdate"] = paymentdate
        if amount is not None:
            data["amount"] = amount
        
        return await api_client.patch(
            f"/classic-models/api/v1/payments/{customernumber}/{checknumber}/",
            data
        )

