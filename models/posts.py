from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    status: str  # Consider using Enum for ["draft", "published"]
    content: str
    category: str
    author_name: str


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None


class PostInDB(PostBase):
    id: str
    created_at: datetime
    updated_at: datetime


class PostResponse(PostInDB):
    pass
