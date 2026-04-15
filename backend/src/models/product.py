from typing import TYPE_CHECKING
from decimal import Decimal as PyDecimal
from sqlalchemy import String, Text, ForeignKey, Numeric, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base


# Типизация
if TYPE_CHECKING:
    from .category import Category

class Product(Base):
    """ Товар """
    
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text)
    image_url: Mapped[str | None] = mapped_column(String(255))

    # Связь с категорией
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id", ondelete="CASCADE"))
    category: Mapped["Category"] = relationship("Category", back_populates="products")
    
    # # Связь с вариантами (размеры, цены)
    variants: Mapped[list["ProductVariant"]] = relationship(
        "ProductVariant", 
        back_populates="product", 
        cascade="all, delete-orphan",
        lazy="selectin" 
    )

    def __repr__(self):
        return f"<Product(title={self.title})>"
    

class ProductVariant(Base):
    """ Вариант товара """
    
    size: Mapped[str | None] = mapped_column(String(50))
    price: Mapped[PyDecimal] = mapped_column(Numeric(10, 2))
    stock: Mapped[int] = mapped_column(Integer, default=0)
    
    # Связь с товаром
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id", ondelete="CASCADE"))
    product: Mapped["Product"] = relationship("Product", back_populates="variants")

    def __repr__(self):
        return f"<ProductVariant(size={self.size}, price={self.price})>"

