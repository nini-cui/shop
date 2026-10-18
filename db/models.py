from datetime import datetime
from pydantic import BaseModel

class CategoryCreate(BaseModel):
    name: str
    slug: str

class ProductCreate(BaseModel):
    name: str
    slug: str
    description: str | None = None
    price: float
    stock_quantity: int
    category_ids: list[int] = []

class ProductCategory(BaseModel):
    product_id: int
    category_id: int
