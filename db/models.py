from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal


class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    slug: str = Field(min_length=1, max_length=255)


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    price: Decimal = Field(gt=0)
    stock_quantity: int = Field(ge=0)
    category_ids: list[int] = Field(default_factory=list)
    image_keys: list[str] = Field(default_factory=list)


class ProductCategory(BaseModel):
    product_id: int = Field(gt=0)
    category_id: int = Field(gt=0)


class ProductList(BaseModel):
    category_id: int | None = Field(default=None, gt=0)
    min_price: Decimal | None = Field(default=None, ge=0)
    max_price: Decimal | None = Field(default=None, ge=0)
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=50, ge=1, le=100)


class ProductGet(BaseModel):
    product_id: int = Field(gt=0)


class BucketCreate(BaseModel):
    bucket_name: str | None = Field(default=None, min_length=3, max_length=63)


class ProductImageResponse(BaseResponse):
    image_key: str
    display_order: int
    image_url: str


class ProductResponse(BaseResponse):
    id: int
    name: str
    slug: str
    description: str | None = None
    price: Decimal
    stock_quantity: int
    images: list[ProductImageResponse] = Field(default_factory=list)


class ProductListResponse(BaseModel):
    products: list[ProductResponse]
    next: bool
    previous: bool
