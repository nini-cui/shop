from fastapi import FastAPI
from api.routes import categories, products, storage

app = FastAPI()

app.include_router(categories.router)
app.include_router(products.router)
app.include_router(storage.router)