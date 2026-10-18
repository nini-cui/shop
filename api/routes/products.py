from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import deps

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/")
def get_products(db: Session = Depends(deps.get_db)):
    # Query products from your database here
    return []