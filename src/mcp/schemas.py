from pydantic import BaseModel
from typing import List, Optional

class Model(BaseModel):
    id: int
    name: str
    category_id: int
    supplier_id: int
    price: float
    stock: int

class Category(BaseModel):
    id: int
    name: str

class Supplier(BaseModel):
    id: int
    name: str
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None

class ModelListResponse(BaseModel):
    models: List[Model]

class ModelResponse(BaseModel):
    model: Model

class CategoryListResponse(BaseModel):
    categories: List[Category]

class SupplierListResponse(BaseModel):
    suppliers: List[Supplier]