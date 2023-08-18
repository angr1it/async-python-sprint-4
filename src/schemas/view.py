from datetime import datetime

import orjson
from pydantic import BaseModel


class ViewBase(BaseModel):
    url_id: int
    viewed_at: datetime
    client_info: orjson

    class Config:
        orm_mode = True
        json_loads = orjson.loads
        json_dumps = orjson.dumps

        arbitrary_types_allowed = True


class ViewCreate(ViewBase):
    pass


class ViewInDB(ViewBase):
    id: int


class ViewState(BaseModel):
    url_id: int
    views: int
