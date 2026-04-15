from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


class Base(DeclarativeBase):
    """Базовый класс для всех моделей"""
    
    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Автоматически делает имя таблицы из имени класса в нижнем регистре"""
        return cls.__name__.lower()
    
    # Добавление id для всех таблиц
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    