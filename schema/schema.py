from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    ForeignKey,
    Identity,
    PrimaryKeyConstraint,
    func,
    Numeric,
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

    id = Column(Integer, Identity(), primary_key=True, nullable=False)
    name = Column(String(255), unique=True, nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    stock_quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class ProductCategory(Base):
    __tablename__ = "product_category"
    product_id = Column(
        Integer, ForeignKey("product.id", ondelete="CASCADE"), nullable=False
    )
    category_id = Column(
        Integer, ForeignKey("category.id", ondelete="CASCADE"), nullable=False
    )
    __table_args__ = (PrimaryKeyConstraint("product_id", "category_id"),)


class ProductImages(Base):
    __tablename__ = "product_images"
    id = Column(Integer, Identity(), primary_key=True, nullable=False)
    product_id = Column(
        Integer, ForeignKey("product.id", ondelete="CASCADE"), nullable=False
    )
    image_key = Column(Text, nullable=False, unique=True)
    display_order = Column(Integer, nullable=False, default=0)
