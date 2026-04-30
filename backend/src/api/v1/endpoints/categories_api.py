from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db
from src.schemas.category_schema import CategoryCreate, CategoryResponse
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









