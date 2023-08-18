from sqlalchemy import select

from models.auth import User as UserModel
from schemas.auth import UserCreate
from services.base import RepositoryDB


class RepositoryUser(RepositoryDB[UserModel, UserCreate]):

    async def select_by_username(self, username: str):
        return select(self._model).where(self._model.username == username)


user_repository = RepositoryUser(UserModel)
