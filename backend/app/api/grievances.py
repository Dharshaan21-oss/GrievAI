from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.models.grievance import Grievance, GrievanceStatus, PriorityLevel
from app.models.status_history import GrievanceStatusHistory
from app.models.department import Department
from app.models.user import User
from app.schemas.grievance import GrievanceCreate, GrievanceOut, GrievanceStatusUpdate
from app.api.deps import get_current_user
from app.ml_service import process_new_grievance, add_to_index
from sqlalchemy import func

router = APIRouter(prefix="/api/grievances", tags=["Grievances"])

PRIORITY_MAP = {
    "low": PriorityLevel.low,
    "medium": PriorityLevel.medium,
    "high": PriorityLevel.high,
    "critical": PriorityLevel.critical,
}

@router.post("/", response_model=GrievanceOut)
def create_grievance(
    payload: GrievanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    full_text = f"{payload.title}. {payload.description}"

    # Run the full local AI pipeline
    ai_result = process_new_grievance(full_text)

    # Try to match the predicted category to an existing department
    department = db.query(Department).filter(
        Department.name == ai_result["category"]
    ).first()

    grievance = Grievance(
        title=payload.title,
        description=payload.description,
        citizen_id=current_user.id,
        department_id=department.id if department else None,
        category=ai_result["category"],
        category_confidence=ai_result["category_confidence"],
        priority=PRIORITY_MAP.get(ai_result["priority"], PriorityLevel.medium),
        sentiment_score=None,
        status=GrievanceStatus.filed,
        is_duplicate=ai_result["is_duplicate"],
        duplicate_of_id=ai_result["duplicate_of_id"],
        ai_summary=ai_result["ai_summary"],
        location=payload.location,
    )
    db.add(grievance)
    db.commit()
    db.refresh(grievance)

    # Now that it has a real ID, add it to the duplicate-detection index
    # so future grievances can be compared against it too
    add_to_index(grievance.id, full_text)

    # Log initial status in history
    history = GrievanceStatusHistory(
        grievance_id=grievance.id,
        old_status=None,
        new_status=GrievanceStatus.filed.value,
        changed_by_id=current_user.id,
        remarks="Grievance filed",
    )
    db.add(history)
    db.commit()

    return grievance

@router.get("/stats/summary")
def get_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role.value not in ("official", "admin"):
        raise HTTPException(status_code=403, detail="Only officials or admins can view stats")

    total = db.query(Grievance).count()
    resolved = db.query(Grievance).filter(Grievance.status == GrievanceStatus.resolved).count()
    critical = db.query(Grievance).filter(Grievance.priority == PriorityLevel.critical).count()

    by_category = (
        db.query(Grievance.category, func.count(Grievance.id))
        .filter(Grievance.category.isnot(None))
        .group_by(Grievance.category)
        .all()
    )
    by_status = (
        db.query(Grievance.status, func.count(Grievance.id))
        .group_by(Grievance.status)
        .all()
    )

    return {
        "total": total,
        "resolved": resolved,
        "critical": critical,
        "by_category": [{"category": c, "count": n} for c, n in by_category],
        "by_status": [{"status": s.value, "count": n} for s, n in by_status],
    }


@router.get("/", response_model=List[GrievanceOut])
def list_grievances(
    status: Optional[GrievanceStatus] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Grievance)

    # Citizens only see their own grievances; officials/admins see all
    if current_user.role.value == "citizen":
        query = query.filter(Grievance.citizen_id == current_user.id)

    if status:
        query = query.filter(Grievance.status == status)
    if category:
        query = query.filter(Grievance.category == category)

    return query.order_by(Grievance.created_at.desc()).all()


@router.get("/{grievance_id}", response_model=GrievanceOut)
def get_grievance(
    grievance_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    grievance = db.query(Grievance).filter(Grievance.id == grievance_id).first()
    if not grievance:
        raise HTTPException(status_code=404, detail="Grievance not found")

    if current_user.role.value == "citizen" and grievance.citizen_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this grievance")

    return grievance


@router.patch("/{grievance_id}/status", response_model=GrievanceOut)
def update_status(
    grievance_id: int,
    payload: GrievanceStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role.value not in ("official", "admin"):
        raise HTTPException(status_code=403, detail="Only officials or admins can update status")

    grievance = db.query(Grievance).filter(Grievance.id == grievance_id).first()
    if not grievance:
        raise HTTPException(status_code=404, detail="Grievance not found")

    old_status = grievance.status.value
    grievance.status = payload.status
    if payload.status == GrievanceStatus.resolved:
        from datetime import datetime
        grievance.resolved_at = datetime.utcnow()

    history = GrievanceStatusHistory(
        grievance_id=grievance.id,
        old_status=old_status,
        new_status=payload.status.value,
        changed_by_id=current_user.id,
        remarks=payload.remarks,
    )
    db.add(history)
    db.commit()
    db.refresh(grievance)

    return grievance