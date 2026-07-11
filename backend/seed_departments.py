from app.db.session import SessionLocal
from app.models.department import Department

CATEGORIES = [
    "Water Supply", "Electricity", "Roads & Infrastructure",
    "Sanitation & Waste Management", "Public Safety", "Corruption",
    "Health Services", "Education"
]

def seed():
    db = SessionLocal()
    for name in CATEGORIES:
        existing = db.query(Department).filter(Department.name == name).first()
        if not existing:
            db.add(Department(name=name, description=f"{name} department"))
    db.commit()
    db.close()
    print("Departments seeded.")

if __name__ == "__main__":
    seed()