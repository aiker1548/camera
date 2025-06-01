from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Interval, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from src.application.video.tdo.enums import TimeOfDay, TracingStatus
from src.infrastructure.data.postgres.base import Base


class Video(Base):
    __tablename__ = 'videos'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)  # должно содержать id
    duration = Column(Interval, nullable=False)
    resolution_width = Column(Integer)
    resolution_height = Column(Integer)
    fps = Column(Integer)
    time_of_day = Column(Enum(TimeOfDay, name="time_of_day"))
    tracing = Column(Enum(TracingStatus, name="tracing_status"))
    counter = Column(Integer, default=0)

    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    author = relationship("User")

    camera_id = Column(UUID(as_uuid=True), ForeignKey("d_camera.id"), nullable=False)
    camera = relationship("Camera", back_populates="videos")

    upload_time = Column(DateTime, default=datetime.utcnow)
    preview_url = Column(String)
