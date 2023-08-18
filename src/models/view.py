from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    JSON
)

from models import Base


class View(Base):
    __tablename__ = "view"
    id = Column(Integer, primary_key=True)
    url_id = Column(Integer, ForeignKey("url.id"), nullable=False)
    viewed_at = Column(DateTime, default=datetime.utcnow)
    client_info = Column(JSON)
