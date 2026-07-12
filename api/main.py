from fastapi import FastAPI, Depends
from db import deps, models
from sqlalchemy.orm import Session

app = FastAPI()

@app.post("/products")
def add_product(
    payload: models.Product,
    db: Session = Depends(deps.get_db)
):
    print("payload is: ", payload)