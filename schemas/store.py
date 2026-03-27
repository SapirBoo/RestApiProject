from pydantic import BaseModel, Field
from typing import List, Optional
from .item import ItemResponse
from .tag import TagResponse

class Store(BaseModel):
    id: Optional[int] = None
    name: str

class StoreCreate(Store):
    pass

class StoresResponse(Store):
    items: List[ItemResponse] = Field(default_factory=list)
    tags: List[TagResponse] = Field(default_factory=list)

    model_config = {"from_attributes": True}

class StoresListResponse(BaseModel):
    stores: List[StoresResponse] = Field(default_factory=list)
    total: int = 0
    message: Optional[str] = None