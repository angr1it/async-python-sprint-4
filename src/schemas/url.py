from datetime import datetime
import uuid
from typing import Optional

from pydantic import AnyUrl, BaseModel, ConfigDict


class URLCreateInput(BaseModel):
    url: AnyUrl
    private: bool


class URLBase(BaseModel):
    short_url: str
    original_url: str
    private: bool
    created_at: datetime


class URLCreate(BaseModel):
    short_url: str
    original_url: str
    private: bool
    created_at: datetime
    creator_id: Optional[uuid.UUID]


class URLUpdate(URLBase):
    pass


class URLRead(URLBase):
    id: int


class URLInDBBase(URLRead):
    model_config = ConfigDict(from_attributes=True)

    deleted: bool


class URLInDB(URLInDBBase):
    pass


class URL(URLInDBBase):
    pass
