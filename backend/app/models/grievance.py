from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.session import Base

class GrievanceStatus(str, enum.Enum):
    filed = "filed"
    in_review = "in_review"
    assigned = "assigned"
    in_progress = "in_progress"
    resolved = "resolved"
    rejected = "rejected"

class PriorityLevel(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class Grievance(Base):
    __tablename__ = "grievances"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)

    citizen_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    citizen = relationship("User", back_populates="grievances", foreign_keys=[citizen_id])

    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    department = relationship("Department", back_populates="grievances")

    category = Column(String, nullable=True)          # AI-predicted category
    category_confidence = Column(Float, nullable=True)  # model confidence score

    priority = Column(Enum(PriorityLevel), default=PriorityLevel.medium)
    sentiment_score = Column(Float, nullable=True)

    status = Column(Enum(GrievanceStatus), default=GrievanceStatus.filed)

    is_duplicate = Column(Boolean, default=False)
    duplicate_of_id = Column(Integer, ForeignKey("grievances.id"), nullable=True)

    ai_summary = Column(Text, nullable=True)
    location = Column(String, nullable=True)
    photo_path = Column(String, nullable=True)

    assigned_official_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    status_history = relationship("GrievanceStatusHistory", back_populates="grievance")