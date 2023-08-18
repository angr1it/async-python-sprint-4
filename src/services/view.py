
from sqlalchemy import insert, or_, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from models.view import View as ViewModel
from schemas.view import ViewCreate
from models.auth import User
from services.base import RepositoryDB
from models.url import Url as UrlModel


class RepositoryView(RepositoryDB[ViewModel, ViewCreate]):

    async def add_from_select(self, db: AsyncSession, select_statement):

        statement = insert(self._model).from_select(
            ['url_id'],
            select_statement
        )

        await db.execute(statement=statement)
        await db.commit()

    async def _get_select_views_by_url(self, db: AsyncSession, viewer: User, url_id: int, limit: int, offset: int):

        viewer_id = None if not viewer else viewer.id

        selected_url = (
            select(UrlModel)
            .where(UrlModel.id == url_id)
            .where(UrlModel.deleted == False)  # noqa
            .where(or_(UrlModel.private == False, UrlModel.creator_id == viewer_id))  # noqa
        )

        statement = (
            select(self._model)
            .where(self._model.url_id == selected_url.c.id)
            .limit(limit=limit)
            .offset(offset=offset)
        )

        return statement

    async def get_views_by_url_id(self, db: AsyncSession, viewer: User, url_id: int, limit: int, offset: int):

        statement = await self._get_select_views_by_url(db=db, viewer=viewer, url_id=url_id, limit=limit, offset=offset)
        result = await db.execute(statement=statement)
        return result.scalars().all()

    async def get_view_status_by_url_id(self, db: AsyncSession, viewer: User, url_id: int):

        statement = await self._get_select_views_by_url(db=db, viewer=viewer, url_id=url_id, limit=None, offset=0)

        status = (
            select(func.count()).select_from(
                select(self._model.id)
                .where(self._model.id == statement.c.id)
            )
        )

        result = await db.execute(statement=status)
        return result.scalar_one_or_none()


view_repository = RepositoryView(ViewModel)
