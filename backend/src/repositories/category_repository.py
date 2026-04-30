from sqlalchemy import select

from src.repositories.base_repository import BaseRepository
from src.models.category import Category


class CategoryRepository(BaseRepository[Category]):
    def __init__(self, session):
        super().__init__(Category, session)
        
        
    async def get_by_name(self, name: str) -> Category | None:
        """ Получить категорию по названию """
        
        query = select(self.model).where(self.model.name == name)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    