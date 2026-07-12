from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    DateTime, 
    Text, Float, 
    ForeignKey, 
    Identity, 
    PrimaryKeyConstraint, 
    func
)
    
class Base(DeclarativeBase):
    pass

class Category(Base):
    __tablename__ = "category"
    
    id = Column(Integer, Identity(), primary_key=True, nullable=False)
    name = Column(String(255), unique=True, nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    create_at = Column(DateTime, server_default=func.now())

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255), unique=True, nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class ProductCategory(Base):
    __tablename__ = "product_category"
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    __table_args__ = (
        PrimaryKeyConstraint("product_id", "category_id"),
    )
