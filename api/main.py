from fastapi import FastAPI, Depends
from db import deps, models
from sqlalchemy.orm import Session
from sqlalchemy import select
from schema import schema

app = FastAPI()

@app.post("/categories")
def add_category(
    payload: models.CategoryCreate,
    db: Session = Depends(deps.get_db)
):
    category = schema.Category(name=payload.name, slug=payload.slug)
    db.add(category)
    db.commit()

def fetch_categories(db: Session):
    categories = db.execute(select(schema.Category)).scalars().all()
    print("Categories", categories)
    return categories

@app.get("/categories")
def get_categories(db: Session = Depends(deps.get_db)):
    return fetch_categories(db)   

@app.post("/products")
def add_product(
    payload: models.Product,
    db: Session = Depends(deps.get_db)
):  
    product_name = payload.name
    # first check if product already exist

        # if not create product

    # then check if the product in the category already
        # if not create category
    
    # create product category record
