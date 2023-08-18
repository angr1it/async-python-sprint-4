from pydantic import BaseModel


class IdsList(BaseModel):
    ids: list[int]
