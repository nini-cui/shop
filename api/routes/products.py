from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, selectinload
from schema import schema
from db import deps, models
from sqlalchemy import select
from slugify import slugify
from typing import Annotated
import boto3, os

router = APIRouter(prefix="/products", tags=["Products"])
BUCKET_NAME = os.environ["BUCKET_NAME"]


def generate_presigned_url(image_key: str):
    s3_client = boto3.client("s3")

    return s3_client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": BUCKET_NAME,
            "Key": image_key,
        },
        ExpiresIn=900,
    )


@router.post("/")
def add_product(payload: models.ProductCreate, db: Session = Depends(deps.get_db)):

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

    slug = slugify(payload.name)

    try:
        # step 2: insert into product table
        product = schema.Product(
            name=payload.name,
            slug=slug,
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
        image_keys = dict.fromkeys(payload.image_keys)
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


@router.get("/", response_model=models.ProductListResponse)
def list_products(
    filters: Annotated[models.ProductList, Query()], db: Session = Depends(deps.get_db)
):
    query = select(schema.Product).options(selectinload(schema.Product.images))

    if filters.min_price is not None:
        query = query.where(schema.Product.price >= filters.min_price)

    if filters.max_price is not None:
        query = query.where(schema.Product.price <= filters.max_price)

    if filters.category_id is not None:
        query = query.join(
            schema.ProductCategory,
            schema.Product.id == schema.ProductCategory.product_id,
        ).where(schema.ProductCategory.category_id == filters.category_id)

    page_size = filters.page_size
    offset = (filters.page - 1) * page_size

    query = query.offset(offset).limit(page_size + 1)

    products = db.execute(query).scalars().all()

    has_next = len(products) > page_size
    products = products[:page_size]

    for product in products:
        for image in product.images:
            image.image_url = generate_presigned_url(image.image_key)

    return models.ProductListResponse(
        products=products,
        next=has_next,
        previous=filters.page > 1,
    )


@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(deps.get_db)):
    product = db.execute(
        select(schema.Product).where(schema.Product.id == product_id)
    ).scalar()
    if product is None:
        raise HTTPException(status_code=404, detail=print("product not found"))

    return product
