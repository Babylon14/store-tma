from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base


# Типизация
if TYPE_CHECKING: #
    from .product import Product

class Category(Base):
    """ Категория товара """

    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    icon_url: Mapped[str | None] = mapped_column(String(255))
    
    # Обратная связь: одна категория — много товаров
    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="category",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Category(name={self.name})>"



