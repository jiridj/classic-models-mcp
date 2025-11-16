"""MCP tools module.

This module contains all MCP tool implementations organized by resource type.
Each resource module exports a registration function that adds tools to the MCP server.
"""
from .productlines import register_productline_tools
from .products import register_product_tools
from .offices import register_office_tools
from .employees import register_employee_tools
from .customers import register_customer_tools
from .orders import register_order_tools
from .payments import register_payment_tools
from .orderdetails import register_orderdetail_tools

__all__ = [
    "register_productline_tools",
    "register_product_tools",
    "register_office_tools",
    "register_employee_tools",
    "register_customer_tools",
    "register_order_tools",
    "register_payment_tools",
    "register_orderdetail_tools",
]

