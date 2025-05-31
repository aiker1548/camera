from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from src.infrastructure.data.postgres.base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=False), primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    fio = Column(String(255), nullable=False)
    org = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=False)
