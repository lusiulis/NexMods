from fastapi import APIRouter, Depends
from app.schemas.product import ProductOut, ProductCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.product import create_product
from app.database import get_db
router = APIRouter()

@router.post("/", response_model=ProductOut)
async def create(data: ProductCreate, db: AsyncSession = Depends(get_db)):
    return await create_product(db, data)
