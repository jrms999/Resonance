from sqlalchemy import Column, BigInteger, Integer, DateTime, Boolean, ForeignKey, String
from sqlalchemy.sql import func

from app.core.database import Base


class PlayEvent(Base):
    __tablename__ = "play_events"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    track_id = Column(Integer, ForeignKey("tracks.id"), nullable=False, index=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    duration_ms = Column(Integer, nullable=True)
    full_play = Column(Boolean, nullable=False, default=False)
    device_type = Column(String(50), nullable=True)
