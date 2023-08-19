from typing import Generic, TypeVar
from abc import ABC

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from models import Base


class Repository(ABC):
    def get(self, *args, **kwargs):
        raise NotImplementedError

    def get_multi(self, *args, **kwargs):
        raise NotImplementedError

    def create(self, *args, **kwargs):
        raise NotImplementedError

    def update(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class RepositoryDB(Repository, Generic[ModelType, CreateSchemaType]):

    def __init__(self, model: type[ModelType]) -> None:
        self._model = model

    async def create(self, db: AsyncSession, obj_in: CreateSchemaType):
        obj = self._model(**obj_in.model_dump())

        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj
