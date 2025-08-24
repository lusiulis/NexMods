from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.schemas import CategoryCreate, CategoryOut, CategoryUpdate, ActionResponse, PaginatedCategorySummaryOut, CategorySummaryOut
from app.models import Category
from app.models import Product, ProductStatus
from typing import Optional
from fastapi import HTTPException

async def create_category(
    db: AsyncSession,
    data: CategoryCreate
) -> CategoryOut:
    result = await db.execute(select(Category).where(Category.name == data.name))
    category_with_name = result.scalar_one_or_none()
    if category_with_name:
        raise HTTPException(status_code=409, detail="Category name already taken.")
    
    new_category = Category(
        name=data.name,
        description=data.description
    )
    
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
        
    return CategoryOut.model_validate(new_category)

async def update_category(
    db: AsyncSession,
    id: int,
    data: CategoryUpdate
) -> ActionResponse:
    result = await db.execute(select(Category).where(Category.id == id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found.")
    
    if data.name:
        name_query_result = await db.execute(select(Category).where(Category.name == data.name))
        category_with_name = name_query_result.scalar_one_or_none()
        if category_with_name and category_with_name.id != id:
            raise HTTPException(status_code=409, detail="Category name already taken.")
        
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(category, field, value)
        
    db.add(category)
    await db.commit()
    await db.refresh(category)
        
    return ActionResponse(
        message = "Category updated successfully",
        status = "successful"
    )
    
async def delete_category(
    db: AsyncSession,
    id: int
) -> ActionResponse:
    result = await db.execute(select(Category).where(Category.id == id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found.")
    
    #Check relations with Product
    
    await db.delete(category)
    await db.commit()
    
    return ActionResponse(
        message = "Category deleted successfully",
        status = "successful"
    )
    
async def get_categories(
    db: AsyncSession,
    page: int = 1,
    limit: int = 10,
    name: Optional[str] = None
) -> PaginatedCategorySummaryOut:
    offset = (page - 1) * limit 
    query = select(Category)
    if name:
        query = query.where(Category.name.ilike(f"%{name}%"))
        
    total_result = await db.execute(
        select(func.count()).select_from(query.subquery())
    )
    total = total_result.scalar() or 0
    pages = (total + limit - 1) // limit
    
    count_expr = func.count(Product.id).filter(Product.status == ProductStatus.ACTIVE)
    stmt = (
        select(
            Category.id,
            Category.name,
            Category.description,
            count_expr.label("product_count")
        )
        .outerjoin(Category.products)
        .group_by(Category.id)
        .order_by(Category.name)
        .offset(offset)
        .limit(limit)
    )
    
    rows = (await db.execute(stmt)).all()
    
    items = [
        CategorySummaryOut(
            id = row[0],
            description = row[1],
            name = row[2],
            product_count= row[3] or 0
        )
        for row in rows
    ]

    return PaginatedCategorySummaryOut(
        total=total,
        pages=pages,
        items=items
    )