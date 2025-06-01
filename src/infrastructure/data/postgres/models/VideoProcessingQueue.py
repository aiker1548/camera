import sqlalchemy as sa
from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column, Mapped
import uuid
from datetime import datetime

from src.infrastructure.data.postgres.base import Base


class VideoProcessingQueue(Base):
    __tablename__ = 'video_processing_queue'

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    video_id = Column(UUID, ForeignKey("videos.id"), nullable=False)
    status = Column(Enum("Pending", "Processing", "Done", "Error", name="processing_status"))
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)