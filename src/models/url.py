from datetime import datetime

from sqlalchemy import (
    UUID,
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    ForeignKey
)

from models.settings import MAX_SHORT_URL_LENGTH, MAX_URL_LENGTH
from models import Base


class Url(Base):
    __tablename__ = "url"
    id = Column(Integer, primary_key=True)
    short_url = Column(String(MAX_SHORT_URL_LENGTH), nullable=True)
    original_url = Column(String(MAX_URL_LENGTH), nullable=False)
    private = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    creator_id = Column(UUID, ForeignKey("user.id"), nullable=True)
    deleted = Column("deleted", Boolean, default=False)
