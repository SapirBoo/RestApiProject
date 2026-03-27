from pydantic import BaseModel, Field
from typing import List, Optional

class Tag(BaseModel):
    id: Optional[int] = None
    name: str

class TagCreate(Tag):
    store_id: int
    item_id: Optional[int] = None

class TagResponse(Tag):
    model_config = {
        "from_attributes": True
    }

class TagUpdate(BaseModel):
    name: Optional[str] = None

class TagListResponse(BaseModel):
    tags: List[TagResponse] = Field(default_factory=list)
    total: int = 0
    message: Optional[str] = None

    model_config = {"from_attributes": True}
    