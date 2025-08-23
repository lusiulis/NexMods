from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Cart(Base):
    __tablename__ = "carts"
    
    product_variant_id: Mapped[int] = mapped_column(Integer, ForeignKey("product_variants.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    
    user = relationship("User", back_populates="carts")
    product_variant = relationship("ProductVariant", back_populates="carts")