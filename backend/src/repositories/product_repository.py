from typing import Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload


from src.repositories.base_repository import BaseRepository
from src.models.product import Product, ProductVariant


class ProductRepository(BaseRepository[Product]):
    def __init__(self, session: AsyncSession):
        super().__init__(Product, session)
        
        
    async def get_with_variants(self, id: Any) -> Product | None:
        """Получение продукта вместе с его вариантами (размерами и ценами).""" 
        query = (
            select(Product)
            .where(Product.id == id)
            .options(joinedload(Product.variants))
        )
        result = await self.session.execute(query)
        return result.unique().scalar_one_or_none()
    
    
    async def get_multi_with_variants(self, skip: int = 0,
                                      limit: int = 100) -> list[Product]:
        """Получение списка продуктов с подгрузкой вариантов (пагинация)."""
        query = (
            select(Product)
            .options(joinedload(Product.variants))
            .offset(skip)
            .limit(limit)
            .order_by(Product.id) 
        )
        result = await self.session.execute(query)
        return list(result.unique().scalars().all())
        
        
    async def create_product_with_variants(self, product_data: dict,
                                           variants_data: list[dict]) -> Product:
        """Создание продукта и его вариантов в одной транзакции."""
        # Создание объекта продукта
        product = Product(**product_data)
        self.session.add(product)
        await self.session.flush()
        
        # Создание объектов вариантов
        for variant_data in variants_data:
            variant = ProductVariant(**variant_data, product_id=product.id)
            self.session.add(variant)

        await self.session.commit()
        await self.session.refresh(product)
        return product


    