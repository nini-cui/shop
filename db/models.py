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

class ProductList(BaseModel):
    category_id: int | None = None
    min_price: float | None = None
    max_price: float | None = None

class ProductGet(BaseModel):
    product_id: int
