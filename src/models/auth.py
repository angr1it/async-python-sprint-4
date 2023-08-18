from uuid import UUID
import uuid
from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, String, DateTime, Boolean, UUID

from models import Base
from models.settings import MAX_EMAIL_LENGTH, MAX_USERNAME_LENGTH


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"
    id: UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: str = Column(String(MAX_USERNAME_LENGTH), nullable=False)
    email: str = Column(String(MAX_EMAIL_LENGTH), nullable=False)
    hashed_password: str = Column(String, nullable=False)
    registred_at: datetime = Column(DateTime, default=datetime.utcnow)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
