from fastapi import FastAPI
from app.routers import product, category

app = FastAPI(title="Product Service")

@app.get("/")
async def root():
    return {"message": "Products service is alive"}

app.include_router(product.router, prefix="/products", tags=["Products"])
app.include_router(category.router, prefix="/categories", tags=["Categories"])