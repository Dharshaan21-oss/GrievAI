from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.grievance import GrievanceStatus, PriorityLevel

class GrievanceCreate(BaseModel):
    title: str
    description: str
    location: Optional[str] = None

class GrievanceOut(BaseModel):
    id: int
    title: str
    description: str
    citizen_id: int
    department_id: Optional[int] = None
    category: Optional[str] = None
    category_confidence: Optional[float] = None
    priority: PriorityLevel
    status: GrievanceStatus
    is_duplicate: bool
    duplicate_of_id: Optional[int] = None
    ai_summary: Optional[str] = None
    location: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class GrievanceStatusUpdate(BaseModel):
    status: GrievanceStatus
    remarks: Optional[str] = None