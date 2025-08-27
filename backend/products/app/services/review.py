from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from app.schemas import ReviewCreate, ReviewOut, PaginatedReviewItem, ReviewItem, ReviewUserInfo, ActionResponse, ReviewUpdate
from app.models import Review, User, Product
from fastapi import HTTPException
from typing import List

async def create_review(db: AsyncSession, data: ReviewCreate) -> ReviewOut:
    #ADD TOKEN USER ID - REMOVE FROM SCHEME
    user = await db.get(User, data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    product = await db.get(Product, data.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    review = Review(
        rating = data.rating,
        product_id = data.product_id,
        user_id = data.user_id,
        comment = data.comment
    )
    #product = product, user = user
    
    db.add(review)
    await db.commit()
    await db.refresh(review)

    return ReviewOut.model_validate(review)

async def get_reviews(
    db: AsyncSession, 
    product_id: int,
    page: int = 1,
    limit: int = 10,
) -> PaginatedReviewItem:
    #VALIDATE USER TOKEN
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    offset = (page - 1) * limit
    query = select(Review).where(Review.product_id == product_id).options(
        selectinload(Review.user)
    )
    
    total_result = await db.execute(
        select(func.count()).select_from(query.subquery())
    )
    total = total_result.scalar() or 0
    pages = (total + limit - 1) // limit
    
    result = await db.execute(query.offset(offset).limit(limit))
    reviews: List[Review] = list(result.scalars().all())
    
    items = [
        ReviewItem(
            id = r.id,
            comment = r.comment,
            rating = r.rating,
            user = ReviewUserInfo(
                id = r.user_id,
                username = r.user.username,
                profile_img = r.user.profileImg
            )
        )
        for r in reviews
    ]
    return PaginatedReviewItem(
        total = total,
        pages = pages,
        items = items
    )
    
async def update_review(
    db: AsyncSession,
    review_id: int,
    data: ReviewUpdate
) -> ActionResponse:
    review = await db.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found.")
    
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(review, field, value)
    
    db.add(review)
    await db.commit()
    await db.refresh(review)
    
    return ActionResponse(
        message = "Review updated successfully",
        status = "successful"
    )

async def delete_review(
    db: AsyncSession,
    review_id: int
) -> ActionResponse:
    #VALIDATE TOKEN
    review = await db.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found.")
    
    await db.delete(review)
    await db.commit()
    
    return ActionResponse(
        message = "Review deleted successfully",
        status = "successful"
    )