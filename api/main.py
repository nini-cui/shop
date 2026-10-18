from fastapi import FastAPI
from api.routes import categories, products

app = FastAPI()

app.include_router(categories.router)
app.include_router(products.router)
