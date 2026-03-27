from pydantic import BaseModel, Field
from typing import List, Optional
from .tag import TagResponse

class Item(BaseModel):
    id: Optional[int] = None
    name: str
    price: float

class ItemCreate(Item):
    store_id: int
    tag_id: Optional[int] = None

class ItemResponse(Item):
    model_config = {
        "from_attributes": True
    }

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None

class ItemsListResponse(BaseModel):
    items: List[ItemResponse] = Field(default_factory=list)
    total: int = 0
    message: Optional[str] = None

    model_config = {"from_attributes": True}

class TagsAndItems(BaseModel):
    items: List[ItemResponse] = Field(default_factory=list)
    tags: List[TagResponse] = Field(default_factory=list)
    message: Optional[str] = None

    model_config = {"from_attributes": True}