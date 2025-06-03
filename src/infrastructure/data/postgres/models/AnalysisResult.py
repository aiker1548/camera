from sqlalchemy import Column, DateTime, ForeignKey, String, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid 
from datetime import datetime

from src.infrastructure.data.postgres.base import Base


class AnalysisResult(Base):
    __tablename__ = 'analysis_results'

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    video_id = Column(UUID, ForeignKey("videos.id"))
    result_type = Column(Enum("traffic", "speed", name="analysis_type"))
    result_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
