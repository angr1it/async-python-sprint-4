from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session
from auth.db import User
from api.auth import current_user
from services.url import url_repository
from services.view import view_repository
from schemas.url import URLCreateInput, URLRead
from schemas.ids_list import IdsList


url_router = APIRouter()


@url_router.post("/", response_model=URLRead)
async def create_url(
    *,
    user: User = Depends(current_user),
    obj_in: URLCreateInput,
    db: AsyncSession = Depends(get_async_session)
):
    response = await url_repository.create(db=db, obj_in=obj_in, user=user)

    return response


@url_router.get("/{short_url_id}", response_model=URLRead)
async def get_url_by_id(
    *,
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_async_session),
    short_url_id: int
):
    result = await url_repository.get(db=db, user=user, short_url_id=short_url_id)
    return result


@url_router.post("/items/", response_model=list[URLRead])
async def batch_upload(
    *,
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_async_session),
    ids_list: IdsList
):
    short_url_ids = ids_list.ids
    response = await url_repository.get_multi(
        db=db, user=user, short_url_ids=short_url_ids
    )

    return response


@url_router.get("/delete/{short_url_id}", response_model=URLRead)
async def delete_url(
    *,
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_async_session),
    short_url_id: int
):
    data = await url_repository.delete(db=db, id=short_url_id, user=user)

    return data


@url_router.get("/user/{username}", response_model=list[URLRead])
async def get_by_username(
    *,
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_async_session),
    username: str
) -> list[URLRead]:
    data = await url_repository.get_by_username(db=db, viewer=user, username=username)

    return data


@url_router.get("/{short_url_id}/status")
async def get_url_status(
    *,
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_async_session),
    short_url_id: int,
    full_info: bool,
    limit: Optional[int] = None,
    offset: Optional[int] = 0
):
    if full_info:
        data = await view_repository.get_views_by_url_id(
            db=db, url_id=short_url_id, viewer=user, limit=limit, offset=offset
        )
        return data
    else:
        views = await view_repository.get_view_status_by_url_id(
            db=db, url_id=short_url_id, viewer=user
        )
        result = await url_repository.get(db=db, user=user, short_url_id=short_url_id)

        return {
            "url": result,
            "views": views
        }
