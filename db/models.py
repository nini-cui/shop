from datetime import datetime
from pydantic import BaseModel

class Category(BaseModel):
    id: int
    name: str
    slug: str
    created_at: datetime

class Product(BaseModel):
    id: int
    name: str
    slug: str
    description: str | None = None
    price: float
    stock_quantity: int
    created_at: datetime
    updated_at: datetime

class ProductCreate(BaseModel):
    id: int
    name: str
    slug: str
    description: str | None = None
    price: float
    stock_quantity: int
    created_at: datetime
    updated_at: datetime
