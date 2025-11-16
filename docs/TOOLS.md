# Tools Reference

> 📖 **Navigation:** [Documentation Index](README.md) | [Main README](../README.md)

Complete documentation for all 37 MCP tools available in the Classic Models MCP server.

---

## 📋 Quick Overview

| Resource | Tools | Operations Available |
|----------|-------|---------------------|
| **Products** | 5 | List, Get, Create, Update, Delete |
| **Product Lines** | 5 | List, Get, Create, Update, Delete |
| **Customers** | 5 | List, Get, Create, Update, Delete |
| **Orders** | 5 | List, Get, Create, Update, Delete |
| **Order Details** | 5 | List, Get, Create, Update, Delete |
| **Employees** | 5 | List, Get, Create, Update, Delete |
| **Offices** | 5 | List, Get, Create, Update, Delete |
| **Payments** | 2 | Get, Update |

**Total: 37 tools**

---

## 🔍 Tool Naming Pattern

All tools follow this pattern: `classic_models_{operation}_{resource}`

**Operations:**
- `list_` - Get all items
- `get_` - Get one item
- `create_` - Add new item
- `update_` - Modify existing item
- `delete_` - Remove item

**Example:** `classic_models_list_products` = List all products

---

## 📚 Table of Contents

- [Product Lines Tools](#product-lines-tools) (5 tools)
- [Products Tools](#products-tools) (5 tools)
- [Offices Tools](#offices-tools) (5 tools)
- [Employees Tools](#employees-tools) (5 tools)
- [Customers Tools](#customers-tools) (5 tools)
- [Orders Tools](#orders-tools) (5 tools)
- [Payments Tools](#payments-tools) (2 tools)
- [Order Details Tools](#order-details-tools) (5 tools)

---

## Product Lines Tools

### `classic_models_list_productlines`

Retrieve a list of all product line categories in the Classic Models system.

**Parameters:** None

**Returns:** List of product line dictionaries

**Example:**
```python
productlines = await classic_models_list_productlines()
```

**Use Cases:**
- Browsing available product categories
- Getting a list of product lines before creating products
- Category management and reporting

---

### `classic_models_get_productline`

Retrieve detailed information about a specific product line by its identifier.

**Parameters:**
- `productline` (str, required): The unique product line identifier (max 50 characters)
  - Example: "Motorcycles" or "Classic Cars"

**Returns:** Product line dictionary with productline, textdescription, htmldescription, and image fields

**Example:**
```python
productline = await classic_models_get_productline(productline="Motorcycles")
```

**Use Cases:**
- Getting details for a specific product line
- Verifying a product line exists before creating products
- Viewing product line descriptions and images

---

### `classic_models_create_productline`

Add a new product line category to the Classic Models system.

**Parameters:**
- `productline` (str, required): Unique product line identifier (max 50 characters)
- `textdescription` (str, optional): Plain text description (max 4000 characters)
- `htmldescription` (str, optional): HTML-formatted description

**Returns:** Created product line dictionary

**Example:**
```python
result = await classic_models_create_productline(
    productline="Electric Vehicles",
    textdescription="Modern electric vehicle models",
    htmldescription="<p>Modern electric vehicle models</p>"
)
```

**Use Cases:**
- Adding new product categories
- Creating product lines for new product types
- Expanding the product categorization system

---

### `classic_models_update_productline`

Update specific fields of an existing product line.

**Parameters:**
- `productline` (str, required): The product line identifier to update
- `textdescription` (str, optional): New text description (max 4000 characters)
- `htmldescription` (str, optional): New HTML description

**Returns:** Updated product line dictionary

**Example:**
```python
result = await classic_models_update_productline(
    productline="Motorcycles",
    textdescription="Updated description of motorcycles"
)
```

**Use Cases:**
- Updating product line descriptions
- Modifying HTML descriptions
- Making partial updates to product line information

---

### `classic_models_delete_productline`

Remove a product line from the Classic Models system.

**Parameters:**
- `productline` (str, required): The product line identifier to delete

**Returns:** None (success indicated by no error)

**Example:**
```python
await classic_models_delete_productline(productline="Obsolete Category")
```

**Use Cases:**
- Removing obsolete product categories
- Cleaning up unused product lines
- Reorganizing product categorization

**Warning:** Deleting a product line may fail if products still reference it.

---

## Products Tools

### `classic_models_list_products`

Retrieve a paginated list of all products in the Classic Models catalog.

**Parameters:** None

**Returns:** List of product dictionaries

**Example:**
```python
products = await classic_models_list_products()
```

**Use Cases:**
- Browsing the complete product catalog
- Getting an overview of all available products
- Finding products by examining the full list
- Inventory management and reporting

---

### `classic_models_get_product`

Retrieve detailed information about a specific product by its product code.

**Parameters:**
- `productcode` (str, required): The unique product code identifier (max 15 characters)
  - Example: "S10_1678" or "S12_1098"

**Returns:** Product dictionary with complete product information

**Example:**
```python
product = await classic_models_get_product(productcode="S10_1678")
```

**Use Cases:**
- Looking up product details before making a sale
- Checking product availability and pricing
- Retrieving product information for order processing
- Getting product specifications for customer inquiries

---

### `classic_models_create_product`

Add a new product to the Classic Models catalog with all required information.

**Parameters:**
- `productcode` (str, required): Unique product code identifier (max 15 characters)
- `productname` (str, required): Full product name (max 70 characters)
- `productline` (str, required): Product line category (must exist)
- `productscale` (str, required): Scale of the product model (max 10 characters)
- `productvendor` (str, required): Manufacturer or vendor name (max 50 characters)
- `productdescription` (str, required): Detailed product description
- `quantityinstock` (int, required): Current inventory quantity (0-32767)
- `buyprice` (str, required): Wholesale cost in decimal format
- `msrp` (str, required): Manufacturer's Suggested Retail Price in decimal format

**Returns:** Created product dictionary

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

**Use Cases:**
- Adding new products to inventory
- Expanding the product catalog
- Creating product entries for new inventory items

---

### `classic_models_update_product`

Update specific fields of an existing product in the catalog.

**Parameters:**
- `productcode` (str, required): The product code to update
- `productname` (str, optional): New product name
- `productline` (str, optional): New product line
- `productscale` (str, optional): New product scale
- `productvendor` (str, optional): New vendor name
- `productdescription` (str, optional): New product description
- `quantityinstock` (int, optional): Updated stock quantity
- `buyprice` (str, optional): Updated buy price
- `msrp` (str, optional): Updated MSRP

**Returns:** Updated product dictionary

**Example:**
```python
result = await classic_models_update_product(
    productcode="S10_1678",
    quantityinstock=8000,
    msrp="99.99"
)
```

**Use Cases:**
- Updating product prices
- Adjusting inventory quantities
- Modifying product descriptions
- Changing product categorization

---

### `classic_models_delete_product`

Remove a product from the Classic Models catalog.

**Parameters:**
- `productcode` (str, required): The product code to delete

**Returns:** None (success indicated by no error)

**Example:**
```python
await classic_models_delete_product(productcode="S10_1678")
```

**Use Cases:**
- Removing discontinued products
- Cleaning up obsolete inventory items
- Removing products that are no longer available

**Warning:** Deleting a product may fail if orders still reference it.

---

## Offices Tools

### `classic_models_list_offices`

Retrieve a list of all company office locations worldwide.

**Parameters:** None

**Returns:** List of office dictionaries

**Example:**
```python
offices = await classic_models_list_offices()
```

**Use Cases:**
- Viewing all company office locations
- Getting office contact information
- Office management and reporting

---

### `classic_models_get_office`

Retrieve detailed information about a specific office by its code.

**Parameters:**
- `officecode` (str, required): The unique office code identifier (max 10 characters)
  - Example: "1" or "2"

**Returns:** Office dictionary with complete address and contact information

**Example:**
```python
office = await classic_models_get_office(officecode="1")
```

**Use Cases:**
- Getting details for a specific office location
- Verifying office information
- Looking up office contact details

---

### `classic_models_create_office`

Add a new office location to the company's network.

**Parameters:**
- `officecode` (str, required): Unique office code identifier (max 10 characters)
- `city` (str, required): City where the office is located (max 50 characters)
- `phone` (str, required): Office phone number (max 50 characters)
- `addressline1` (str, required): Primary street address (max 50 characters)
- `country` (str, required): Country name (max 50 characters)
- `postalcode` (str, required): Postal/ZIP code (max 15 characters)
- `territory` (str, required): Sales territory code (max 10 characters)
- `addressline2` (str, optional): Secondary address line
- `state` (str, optional): State or province

**Returns:** Created office dictionary

**Example:**
```python
result = await classic_models_create_office(
    officecode="3",
    city="Chicago",
    phone="+1 312 555 5678",
    addressline1="456 Business Ave",
    country="USA",
    postalcode="60601",
    territory="NA"
)
```

**Use Cases:**
- Adding new office locations
- Expanding the company network
- Creating office entries for new locations

---

### `classic_models_update_office`

Update specific fields of an existing office location.

**Parameters:**
- `officecode` (str, required): The office code to update
- `city` (str, optional): Updated city name
- `phone` (str, optional): Updated phone number
- `addressline1` (str, optional): Updated primary address
- `addressline2` (str, optional): Updated secondary address
- `state` (str, optional): Updated state/province
- `country` (str, optional): Updated country name
- `postalcode` (str, optional): Updated postal code
- `territory` (str, optional): Updated territory code

**Returns:** Updated office dictionary

**Example:**
```python
result = await classic_models_update_office(
    officecode="1",
    phone="+1 650 219 4783",
    addressline2="Suite 400"
)
```

**Use Cases:**
- Updating office addresses
- Changing contact information
- Modifying territory assignments
- Making partial updates to office details

---

### `classic_models_delete_office`

Remove an office location from the company network.

**Parameters:**
- `officecode` (str, required): The office code to delete

**Returns:** None (success indicated by no error)

**Example:**
```python
await classic_models_delete_office(officecode="3")
```

**Use Cases:**
- Removing closed office locations
- Cleaning up obsolete office entries
- Reorganizing the company network

**Warning:** Deleting an office may fail if employees are still assigned to it.

---

## Employees Tools

### `classic_models_list_employees`

Retrieve a list of all employees in the organization with their details.

**Parameters:** None

**Returns:** List of employee dictionaries

**Example:**
```python
employees = await classic_models_list_employees()
```

**Use Cases:**
- Viewing all employees in the organization
- Getting employee contact information
- Employee management and reporting
- Organizational chart analysis

---

### `classic_models_get_employee`

Retrieve detailed information about a specific employee by their employee number.

**Parameters:**
- `employeenumber` (int, required): The unique employee number identifier
  - Example: 1002 or 1056

**Returns:** Employee dictionary with complete employee information

**Example:**
```python
employee = await classic_models_get_employee(employeenumber=1002)
```

**Use Cases:**
- Getting details for a specific employee
- Verifying employee information
- Looking up employee contact details
- Checking reporting relationships

---

### `classic_models_create_employee`

Add a new employee to the organization with their job details and office assignment.

**Parameters:**
- `employeenumber` (int, required): Unique employee number identifier
- `lastname` (str, required): Employee's last name (max 50 characters)
- `firstname` (str, required): Employee's first name (max 50 characters)
- `extension` (str, required): Office extension (max 10 characters)
- `email` (str, required): Employee email address (max 100 characters)
- `jobtitle` (str, required): Job title/position (max 50 characters)
- `officecode` (str, required): Office code where employee is assigned (must exist)
- `reportsto` (int, optional): Employee number of the manager (must exist if provided)

**Returns:** Created employee dictionary

**Example:**
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

**Use Cases:**
- Adding new employees to the organization
- Onboarding new hires
- Creating employee records for new staff

---

### `classic_models_update_employee`

Update specific fields of an existing employee record.

**Parameters:**
- `employeenumber` (int, required): The employee number to update
- `lastname` (str, optional): Updated last name
- `firstname` (str, optional): Updated first name
- `extension` (str, optional): Updated extension
- `email` (str, optional): Updated email address
- `jobtitle` (str, optional): Updated job title
- `officecode` (str, optional): Updated office code
- `reportsto` (int, optional): Updated manager employee number

**Returns:** Updated employee dictionary

**Example:**
```python
result = await classic_models_update_employee(
    employeenumber=1002,
    jobtitle="CEO",
    email="diane.murphy@classicmodelcars.com"
)
```

**Use Cases:**
- Updating employee contact information
- Changing job titles or positions
- Reassigning employees to different offices
- Updating reporting relationships

---

### `classic_models_delete_employee`

Remove an employee from the organization.

**Parameters:**
- `employeenumber` (int, required): The employee number to delete

**Returns:** None (success indicated by no error)

**Example:**
```python
await classic_models_delete_employee(employeenumber=2000)
```

**Use Cases:**
- Removing terminated employees
- Cleaning up obsolete employee records
- Removing employees who have left the organization

**Warning:** Deleting an employee may fail if customers are still assigned to them as sales rep.

---

## Customers Tools

### `classic_models_list_customers`

Retrieve a list of all customers with their contact and credit information.

**Parameters:** None

**Returns:** List of customer dictionaries

**Example:**
```python
customers = await classic_models_list_customers()
```

**Use Cases:**
- Viewing all customers in the system
- Getting customer contact information
- Customer management and reporting
- Credit limit analysis

---

### `classic_models_get_customer`

Retrieve detailed information about a specific customer by their customer number.

**Parameters:**
- `customernumber` (int, required): The unique customer number identifier
  - Example: 103 or 112

**Returns:** Customer dictionary with complete customer information

**Example:**
```python
customer = await classic_models_get_customer(customernumber=103)
```

**Use Cases:**
- Getting details for a specific customer
- Verifying customer information
- Looking up customer contact details
- Checking credit limits before processing orders

---

### `classic_models_create_customer`

Add a new customer to the system with their contact details and credit limit.

**Parameters:**
- `customernumber` (int, required): Unique customer number identifier
- `customername` (str, required): Customer company name (max 50 characters)
- `contactlastname` (str, required): Contact person's last name (max 50 characters)
- `contactfirstname` (str, required): Contact person's first name (max 50 characters)
- `phone` (str, required): Contact phone number (max 50 characters)
- `addressline1` (str, required): Primary street address (max 50 characters)
- `city` (str, required): City name (max 50 characters)
- `country` (str, required): Country name (max 50 characters)
- `addressline2` (str, optional): Secondary address line
- `state` (str, optional): State or province
- `postalcode` (str, optional): Postal/ZIP code
- `creditlimit` (str, optional): Credit limit in decimal format
- `salesrepemployeenumber` (int, optional): Employee number of assigned sales rep

**Returns:** Created customer dictionary

**Example:**
```python
result = await classic_models_create_customer(
    customernumber=500,
    customername="New Customer Inc",
    contactlastname="Doe",
    contactfirstname="Jane",
    phone="+1 555 987 6543",
    addressline1="456 Business Ave",
    city="Chicago",
    country="USA",
    creditlimit="25000.00",
    salesrepemployeenumber=1370
)
```

**Use Cases:**
- Adding new customers to the system
- Onboarding new clients
- Creating customer records for new accounts

---

### `classic_models_update_customer`

Update specific fields of an existing customer record.

**Parameters:**
- `customernumber` (int, required): The customer number to update
- `customername` (str, optional): Updated company name
- `contactlastname` (str, optional): Updated contact last name
- `contactfirstname` (str, optional): Updated contact first name
- `phone` (str, optional): Updated phone number
- `addressline1` (str, optional): Updated primary address
- `addressline2` (str, optional): Updated secondary address
- `city` (str, optional): Updated city name
- `state` (str, optional): Updated state/province
- `postalcode` (str, optional): Updated postal code
- `country` (str, optional): Updated country name
- `creditlimit` (str, optional): Updated credit limit
- `salesrepemployeenumber` (int, optional): Updated sales rep employee number

**Returns:** Updated customer dictionary

**Example:**
```python
result = await classic_models_update_customer(
    customernumber=103,
    phone="40.32.2556",
    creditlimit="25000.00"
)
```

**Use Cases:**
- Updating customer contact information
- Changing customer addresses
- Adjusting credit limits
- Reassigning sales representatives

---

### `classic_models_delete_customer`

Remove a customer from the system.

**Parameters:**
- `customernumber` (int, required): The customer number to delete

**Returns:** None (success indicated by no error)

**Example:**
```python
await classic_models_delete_customer(customernumber=500)
```

**Use Cases:**
- Removing inactive customers
- Cleaning up obsolete customer records
- Removing customers who are no longer active

**Warning:** Deleting a customer may fail if orders or payments still exist for this customer.

---

## Orders Tools

### `classic_models_list_orders`

Retrieve a list of all customer orders with their status and details.

**Parameters:** None

**Returns:** List of order dictionaries

**Example:**
```python
orders = await classic_models_list_orders()
```

**Use Cases:**
- Viewing all orders in the system
- Getting order status information
- Order management and reporting
- Tracking order fulfillment

---

### `classic_models_get_order`

Retrieve detailed information about a specific order by its order number.

**Parameters:**
- `ordernumber` (int, required): The unique order number identifier
  - Example: 10100 or 10101

**Returns:** Order dictionary with complete order information

**Example:**
```python
order = await classic_models_get_order(ordernumber=10100)
```

**Use Cases:**
- Getting details for a specific order
- Verifying order status
- Looking up order information for customer service
- Checking order fulfillment status

---

### `classic_models_create_order`

Create a new customer order with order date, required date, and status information.

**Parameters:**
- `ordernumber` (int, required): Unique order number identifier
- `orderdate` (str, required): Date when the order was placed (YYYY-MM-DD format)
- `requireddate` (str, required): Required delivery date (YYYY-MM-DD format)
- `status` (str, required): Order status (max 15 characters)
- `customernumber` (int, required): Customer number who placed the order (must exist)
- `shippeddate` (str, optional): Date when the order was shipped (YYYY-MM-DD format)
- `comments` (str, optional): Order comments or special instructions

**Returns:** Created order dictionary

**Example:**
```python
result = await classic_models_create_order(
    ordernumber=10500,
    orderdate="2024-01-15",
    requireddate="2024-01-22",
    status="In Process",
    customernumber=363,
    comments="Rush order"
)
```

**Use Cases:**
- Creating new customer orders
- Processing new orders
- Adding orders to the system

**Note:** After creating an order, use order details tools to add line items.

---

### `classic_models_update_order`

Update specific fields of an existing order record.

**Parameters:**
- `ordernumber` (int, required): The order number to update
- `orderdate` (str, optional): Updated order date (YYYY-MM-DD format)
- `requireddate` (str, optional): Updated required date (YYYY-MM-DD format)
- `shippeddate` (str, optional): Updated shipped date (YYYY-MM-DD format)
- `status` (str, optional): Updated order status
- `comments` (str, optional): Updated order comments
- `customernumber` (int, optional): Updated customer number

**Returns:** Updated order dictionary

**Example:**
```python
result = await classic_models_update_order(
    ordernumber=10100,
    status="Shipped",
    shippeddate="2024-01-20"
)
```

**Use Cases:**
- Updating order status (e.g., marking as shipped)
- Changing order dates
- Adding shipping dates
- Updating order comments

---

### `classic_models_delete_order`

Remove an order from the system.

**Parameters:**
- `ordernumber` (int, required): The order number to delete

**Returns:** None (success indicated by no error)

**Example:**
```python
await classic_models_delete_order(ordernumber=10500)
```

**Use Cases:**
- Removing cancelled orders
- Cleaning up obsolete order records
- Removing orders that should not have been created

**Warning:** Deleting an order may fail if order details still exist for this order.

---

## Payments Tools

### `classic_models_get_payment`

Retrieve detailed information about a specific payment by customer number and check number.

**Parameters:**
- `customernumber` (int, required): The customer number who made the payment
- `checknumber` (str, required): The check number or payment identifier (max 50 characters)
  - Example: "HQ336336" or "JM555205"

**Returns:** Payment dictionary with payment details

**Example:**
```python
payment = await classic_models_get_payment(
    customernumber=103,
    checknumber="HQ336336"
)
```

**Use Cases:**
- Getting details for a specific payment
- Verifying payment information
- Looking up payment records for accounting
- Checking payment history for a customer

---

### `classic_models_update_payment`

Update specific fields of an existing payment record.

**Parameters:**
- `customernumber` (int, required): The customer number of the payment to update
- `checknumber` (str, required): The check number of the payment to update
- `paymentdate` (str, optional): Updated payment date (YYYY-MM-DD format)
- `amount` (str, optional): Updated payment amount in decimal format

**Returns:** Updated payment dictionary

**Example:**
```python
result = await classic_models_update_payment(
    customernumber=103,
    checknumber="HQ336336",
    amount="6100.00"
)
```

**Use Cases:**
- Correcting payment dates
- Adjusting payment amounts
- Making corrections to payment records

**Note:** Payments are typically created through the payment processing system. This tool is primarily for corrections and adjustments.

---

## Order Details Tools

### `classic_models_list_orderdetails`

Retrieve a list of all order line items with product details.

**Parameters:** None

**Returns:** List of order detail dictionaries

**Example:**
```python
orderdetails = await classic_models_list_orderdetails()
```

**Use Cases:**
- Viewing all order line items
- Getting order detail information
- Order detail management and reporting
- Analyzing order line items

---

### `classic_models_get_orderdetail`

Retrieve detailed information about a specific order detail by its ID.

**Parameters:**
- `orderdetail_id` (int, required): The unique order detail ID identifier
  - Example: 1 or 100

**Returns:** Order detail dictionary with complete line item information

**Example:**
```python
orderdetail = await classic_models_get_orderdetail(orderdetail_id=1)
```

**Use Cases:**
- Getting details for a specific order line item
- Verifying order detail information
- Looking up order line item details

---

### `classic_models_create_orderdetail`

Create a new order line item with product details.

**Parameters:**
- `ordernumber` (int, required): Order number this line item belongs to (must exist)
- `productcode` (str, required): Product code for this line item (must exist)
- `quantityordered` (int, required): Quantity ordered (positive integer)
- `priceeach` (str, required): Price per unit in decimal format
- `orderlinenumber` (int, required): Line number within the order (typically 1, 2, 3, etc.)

**Returns:** Created order detail dictionary with generated ID

**Example:**
```python
result = await classic_models_create_orderdetail(
    ordernumber=10100,
    productcode="S18_1749",
    quantityordered=30,
    priceeach="136.00",
    orderlinenumber=3
)
```

**Use Cases:**
- Adding products to an order
- Creating order line items
- Adding items to existing orders

---

### `classic_models_update_orderdetail`

Update specific fields of an existing order detail record.

**Parameters:**
- `orderdetail_id` (int, required): The order detail ID to update
- `ordernumber` (int, optional): Updated order number
- `productcode` (str, optional): Updated product code
- `quantityordered` (int, optional): Updated quantity ordered
- `priceeach` (str, optional): Updated price per unit
- `orderlinenumber` (int, optional): Updated line number

**Returns:** Updated order detail dictionary

**Example:**
```python
result = await classic_models_update_orderdetail(
    orderdetail_id=1,
    quantityordered=35,
    priceeach="140.00"
)
```

**Use Cases:**
- Updating quantities ordered
- Adjusting prices
- Changing products in an order line item
- Modifying order line numbers

---

### `classic_models_delete_orderdetail`

Remove an order detail (line item) from the system.

**Parameters:**
- `orderdetail_id` (int, required): The order detail ID to delete

**Returns:** None (success indicated by no error)

**Example:**
```python
await classic_models_delete_orderdetail(orderdetail_id=1)
```

**Use Cases:**
- Removing items from orders
- Cleaning up incorrect order line items
- Removing cancelled line items

---

## Tool Summary

**Total Tools:** 37

- **Product Lines:** 5 tools (list, get, create, update, delete)
- **Products:** 5 tools (list, get, create, update, delete)
- **Offices:** 5 tools (list, get, create, update, delete)
- **Employees:** 5 tools (list, get, create, update, delete)
- **Customers:** 5 tools (list, get, create, update, delete)
- **Orders:** 5 tools (list, get, create, update, delete)
- **Payments:** 2 tools (get, update)
- **Order Details:** 5 tools (list, get, create, update, delete)

All tools support comprehensive error handling, automatic authentication retry, and detailed documentation for LLM comprehension.

