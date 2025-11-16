"""Type definitions for Classic Models API."""
from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    is_active: bool
    date_joined: str


class LoginResponse(BaseModel):
    access: str
    refresh: str
    user: User


class ProductLine(BaseModel):
    productline: str
    textdescription: Optional[str] = None
    htmldescription: Optional[str] = None
    image: Optional[str] = None


class Product(BaseModel):
    productcode: str
    productname: str
    productscale: str
    productvendor: str
    productdescription: str
    quantityinstock: int
    buyprice: str
    msrp: str
    productline: str


class Office(BaseModel):
    officecode: str
    city: str
    phone: str
    addressline1: str
    addressline2: Optional[str] = None
    state: Optional[str] = None
    country: str
    postalcode: str
    territory: str


class Employee(BaseModel):
    employeenumber: int
    lastname: str
    firstname: str
    extension: str
    email: str
    jobtitle: str
    officecode: str
    reportsto: Optional[int] = None


class Customer(BaseModel):
    customernumber: int
    customername: str
    contactlastname: str
    contactfirstname: str
    phone: str
    addressline1: str
    addressline2: Optional[str] = None
    city: str
    state: Optional[str] = None
    postalcode: Optional[str] = None
    country: str
    creditlimit: Optional[str] = None
    salesrepemployeenumber: Optional[int] = None


class Order(BaseModel):
    ordernumber: int
    orderdate: str
    requireddate: str
    shippeddate: Optional[str] = None
    status: str
    comments: Optional[str] = None
    customernumber: int


class Payment(BaseModel):
    id: int
    checknumber: str
    paymentdate: str
    amount: str
    customernumber: int


class OrderDetail(BaseModel):
    id: int
    quantityordered: int
    priceeach: str
    orderlinenumber: int
    ordernumber: int
    productcode: str

