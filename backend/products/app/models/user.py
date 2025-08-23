from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from .cart import Cart
from typing import List

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False)
    profile_img: Mapped[str] = mapped_column(String(2048))
    
    reviews: Mapped[List["Review"]] = relationship("Review", back_populates="user")
    carts: Mapped[List["Cart"]] = relationship("Cart", back_populates="user")