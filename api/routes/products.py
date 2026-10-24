from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from schema import schema
from db import deps, models
from sqlalchemy import select
from typing import Annotated

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/")
def add_products(payload: models.ProductCreate, db: Session = Depends(deps.get_db)):

    # step 1: check if all passed category ids are created
    categories = (
        db.query(schema.Category)
        .filter(schema.Category.id.in_(payload.category_ids))
        .all()
    )

    found_category_ids = {category.id for category in categories}
    missing_ids = set(payload.category_ids) - found_category_ids

    if missing_ids:
        raise HTTPException(
            status_code=400,
            detail=f"Categories not found: {sorted(missing_ids)}",
        )

    try:
        # step 2: insert into product table
        product = schema.Product(
            name=payload.name,
            slug=payload.slug,
            description=payload.description,
            price=payload.price,
            stock_quantity=payload.stock_quantity,
        )
        db.add(product)
        db.flush()
        print("product id is: ", product.id)

        for category_id in set(payload.category_ids):
            product_category = schema.ProductCategory(
                product_id=product.id,
                category_id=category_id,
            )
            db.add(product_category)

        # step 3: insert into product image table
        image_keys = dict.fromkeys(payload.images)
        for idx, image_key in enumerate(image_keys):
            product_image = schema.ProductImages(
                product_id=product.id, image_key=image_key, display_order=idx
            )
            db.add(product_image)

        db.commit()
        db.refresh(product)

        return product

    except Exception:
        db.rollback()
        raise


@router.get("/")
def list_products(
    filters: Annotated[models.ProductList, Query()], db: Session = Depends(deps.get_db)
):
    query = select(schema.Product)

    if filters.min_price is not None:
        query = query.where(schema.Product.price >= filters.min_price)

    if filters.max_price is not None:
        query = query.where(schema.Product.price <= filters.max_price)

    if filters.category_id is not None:
        query = query.join(
            schema.ProductCategory,
            schema.Product.id == schema.ProductCategory.product_id,
        ).where(schema.ProductCategory.category_id == filters.category_id)

    products = db.execute(query).scalars().all()

    return products


@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(deps.get_db)):
    product = db.execute(
        select(schema.Product).where(schema.Product.id == product_id)
    ).scalar()
    if product is None:
        raise HTTPException(status_code=404, detail=print("product not found"))

    return product
