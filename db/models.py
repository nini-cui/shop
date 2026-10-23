from pydantic import BaseModel, Field
from decimal import Decimal

class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    slug: str = Field(min_length=1, max_length=255)
    
class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    slug: str = Field(min_length=1, max_length=255)
    description: str | None = None
    price: Decimal = Field(gt=0)
    stock_quantity: int = Field(ge=0)
    category_ids: list[int] = Field(default_factory=list)
    images: list[str] = Field(default_factory=list)

class ProductCategory(BaseModel):
    product_id: int = Field(gt=0)
    category_id: int = Field(gt=0)

class ProductList(BaseModel):
    category_id: int | None = Field(default=None, gt=0)
    min_price: Decimal | None = Field(default=None, ge=0)
    max_price: Decimal | None = Field(default=None, ge=0)

class ProductGet(BaseModel):
    product_id: int = Field(gt=0)

class BucketCreate(BaseModel):
    bucket_name: str | None = Field(default=None, min_length=3, max_length=63)