from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import deps, models
from schema import product
from sqlalchemy import select

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/")
def add_category(payload: models.CategoryCreate, db: Session = Depends(deps.get_db)):
    category = product.Category(name=payload.name, slug=payload.slug)
    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def fetch_categories(db: Session):
    categories = db.execute(select(product.Category)).scalars().all()
    print("Categories", categories)
    return categories


@router.get("/")
def list_categories(db: Session = Depends(deps.get_db)):
    return fetch_categories(db)
