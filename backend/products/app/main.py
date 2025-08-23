from fastapi import FastAPI
from app.routers import product, category
from contextlib import asynccontextmanager
from app.database import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Product Service", lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Products service is alive"}

app.include_router(product.router, prefix="/products", tags=["Products"])
app.include_router(category.router, prefix="/categories", tags=["Categories"])