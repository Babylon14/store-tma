from typing import Generic, Type, TypeVar, List, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from src.db.base import Base


ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session


    async def get(self, id: Any) -> Optional[ModelType]:
        """ Получить одну запись по ID """
        
        query = select(self.model).where(self.model.id == id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()


    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """ Получить список ВСЕХ записей с пагинацией """
        
        query = select(self.model).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    
    async def create(self, obj_in: dict) -> ModelType:
        """ Создать новую запись """
        
        db_obj = self.model(**obj_in)       # Создаем объект
        self.session.add(db_obj)            # Добавляем объект в сессию
        await self.session.commit()         # Сохраняем изменения в БД
        await self.session.refresh(db_obj)  # Обновляем объект
        return db_obj


    async def update(self, db_obj: ModelType, obj_in: dict | Any) -> None:
        """
        Обновить запись в базе.
        db_obj: объект из базы, который мы уже получили через get()
        obj_in: либо словарь с новыми данными, либо Pydantic-схема
        """
        
        # Если пришла Pydantic-схема, превращаем её в словарь, исключая неустановленные поля
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
            
        # Обновляем атрибуты объекта
        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])

        # Сохраняем изменения в БД
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj


    async def delete(self, id: Any) -> None:
        """ Удалить запись по ID """
        
        query = delete(self.model).where(self.model.id == id)
        result = await self.session.execute(query)
        await self.session.commit()
        return result.rowcount > 0


