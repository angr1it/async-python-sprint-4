from datetime import datetime
from typing import Any, Coroutine
import string
import random
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_

from services.base import RepositoryDB
from models.url import Url as URLModel
from schemas.url import URLCreate, URLCreateInput, URLBase, URLRead
from auth.db import User
from services.user import user_repository
from services.view import view_repository

LINK_GEN_LENGTH = 10


class RepositoryDBURL(RepositoryDB[URLModel, URLCreate]):

    async def get_url_by_short_url(self, db: AsyncSession, short_url: str):
        statement = select(self._model).where(self._model.short_url == short_url)
        results = await db.execute(statement=statement)
        return results.scalar_one_or_none()

    def __generate_short_url(self):
        short_url: str = "https://linkl.com/" + "".join(
            random.choices(string.ascii_uppercase + string.digits, k=LINK_GEN_LENGTH)
        )

        return short_url

    async def __create_short_url(self, db: AsyncSession):
        short_url = self.__generate_short_url()
        while await self.get_url_by_short_url(db=db, short_url=short_url) is not None:
            short_url = self.__generate_short_url()
        return short_url

    async def create(
        self, db: AsyncSession, user: User, obj_in: URLCreateInput
    ) -> Coroutine[Any, Any, URLBase]:
        short_url = await self.__create_short_url(db)

        data = await super().create(
            db=db,
            obj_in=URLCreate(
                short_url=short_url,
                original_url=str(obj_in.url),
                private=obj_in.private if user else False,
                created_at=datetime.utcnow(),
                creator_id=user.id if user else None,
            ),
        )

        return data

    async def bulk_create(
        self, db: AsyncSession, user: User, objs_in: list[URLCreateInput]
    ) -> Coroutine[Any, Any, list[URLBase]]:

        objects_to_add = [
            self._model(
                **URLCreate(
                    short_url=await self.__create_short_url(db),
                    original_url=str(obj_in.url),
                    private=obj_in.private if user else False,
                    created_at=datetime.utcnow(),
                    creator_id=user.id if user else None,
                ).model_dump()
            ) for obj_in in objs_in
        ]

        db.add_all(objects_to_add)
        await db.commit()

        for obj in objects_to_add:
            await db.refresh(obj)

        return objects_to_add

    async def get(
        self, db: AsyncSession, user: User, short_url_id: int
    ) -> Coroutine[Any, Any, URLRead]:

        viewer_id = None if not user else user.id
        statement = (
            select(self._model)
            .where(and_(self._model.id == short_url_id, self._model.deleted == False))  # noqa
            .where(or_(self._model.private == False, self._model.creator_id == viewer_id))  # noqa
        )
        to_view_statement = (
            select(self._model.id)
            .where(statement.c.id == self._model.id)
        )

        await view_repository.add_from_select(db=db, select_statement=to_view_statement)
        results = await db.execute(statement=statement)
        return results.scalar_one_or_none()

    async def get_multi(
        self, db: AsyncSession, user: User, short_url_ids: list[int]
    ) -> Coroutine[Any, Any, list[URLBase]]:

        viewer_id = None if not user else user.id

        statement = (
            select(self._model)
            .where(self._model.id.in_(short_url_ids), self._model.deleted == False)  # noqa
            .where(or_(self._model.private == False, self._model.creator_id == viewer_id))  # noqa
        )

        to_view_statement = (
            select(self._model.id)
            .where(statement.c.id == self._model.id)
        )

        await view_repository.add_from_select(db=db, select_statement=to_view_statement)
        results = await db.execute(statement=statement)
        return results.scalars().all()

    async def get_by_username(self, db: AsyncSession, viewer: User, username: str) -> Optional[list[URLBase]]:
        viewer_id = None if not viewer else viewer.id

        creator_select = await user_repository.select_by_username(username=username)

        statement = (
            select(self._model)
            .where(self._model.creator_id == creator_select.c.id, self._model.deleted == False)  # noqa
            .where(or_(self._model.private == False, self._model.creator_id == viewer_id))  # noqa
        )

        to_view_statement = (
            select(self._model.id)
            .where(statement.c.id == self._model.id)
        )

        await view_repository.add_from_select(db=db, select_statement=to_view_statement)
        results = await db.execute(statement=statement)
        return results.scalars().all()

    async def delete(
        self, db: AsyncSession, user: User, id: int
    ) -> Coroutine[Any, Any, URLBase]:
        if not user:
            return None

        obj = await super().get(db=db, id=id)

        if not obj:
            return None

        if not obj.creator_id:
            return None

        if not obj.creator_id == user.id:
            return None

        obj.deleted = True

        await db.commit()
        await db.refresh(obj)
        return obj


url_repository = RepositoryDBURL(URLModel)
