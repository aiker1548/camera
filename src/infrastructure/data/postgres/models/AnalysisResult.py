# src/infrastructure/data/postgres/models/video_analysis.py

import sqlalchemy as sa
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column, Mapped
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
