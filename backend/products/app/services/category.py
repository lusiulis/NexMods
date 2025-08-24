from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas import CategoryCreate, CategoryOut, CategoryUpdate, ActionResponse
from app.models import Category
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