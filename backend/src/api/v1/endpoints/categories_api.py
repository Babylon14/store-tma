from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db
from src.schemas.category_schema import CategoryCreate, CategoryResponse, CategoryUpdate
from src.repositories.category_repository import CategoryRepository


router = APIRouter()

@router.post(path="/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate,
    db: AsyncSession = Depends(get_db)
):
    """ Создать категорию """
    
    repo = CategoryRepository(db)
    # Проверка на дубликат
    existing = await repo.get_by_name(category_data.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Категория с таким названием уже существует"
        )
    return await repo.create(category_data.model_dump())
        

@router.get(path="/", response_model=list[CategoryResponse])
async def list_categories(db: AsyncSession = Depends(get_db)):
    """ Список категорий """
    
    repo = CategoryRepository(db)
    return await repo.get_all()


@router.patch(path="/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: AsyncSession = Depends(get_db)
):
    """ Обновить категорию """
    
    repo = CategoryRepository(db)
    
    # 1. Получаем объект из базы
    category = await repo.get(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена"
        )
    # 2. Проверка на уникальность имени, если оно изменилось
    if category_data.name and category_data.name != category.name:
        existing_name = await repo.get_by_name(category_data.name)
        if existing_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Категория с таким названием уже существует"
            )
    # 3. Применяем метод обновления  
    await repo.update(db_obj=category, obj_in=category_data)
    return category


@router.delete(path="/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    """ Удалить категорию """
    
    repo = CategoryRepository(db)
    deleted = await repo.delete(category_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена"
        )
    return None



