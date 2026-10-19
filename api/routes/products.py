from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schema import schema
from db import deps, models

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/")
def add_products(
    payload: models.ProductCreate,
    db: Session = Depends(deps.get_db)):

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

    # step 2: insert into product table
    product = schema.Product(name=payload.name, slug=payload.slug, description=payload.description, price=payload.price, stock_quantity=payload.stock_quantity)
    db.add(product)
    db.flush()
    print("product id is: ", product.id)

    for category_id in set(payload.category_ids):
        product_category = schema.ProductCategory(
            product_id=product.id,
            category_id=category_id,
        )
        db.add(product_category)

    db.commit()
    db.refresh(product)

    return product
