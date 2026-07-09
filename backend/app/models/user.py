from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.session import Base

class UserRole(str, enum.Enum):
    citizen = "citizen"
    official = "official"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.citizen, nullable=False)
    department_id = Column(Integer, nullable=True)  # for officials
    created_at = Column(DateTime, default=datetime.utcnow)

    grievances = relationship("Grievance", back_populates="citizen", foreign_keys="Grievance.citizen_id")