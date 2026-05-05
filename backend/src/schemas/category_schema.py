from pydantic import BaseModel, ConfigDict, Field


class CategoryBase(BaseModel):
    name: str
    icon_url: str | None = None
    
    
class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass
    

class CategoryResponse(CategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


