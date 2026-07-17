from app.db.session import SessionLocal
from app.models.department import Department

TEST_EMAIL = "youractualemail@gmail.com"  # replace with your real email

CATEGORIES = [
    "Water Supply", "Electricity", "Roads & Infrastructure",
    "Sanitation & Waste Management", "Public Safety", "Corruption",
    "Health Services", "Education"
]

def seed():
    db = SessionLocal()
    for name in CATEGORIES:
        existing = db.query(Department).filter(Department.name == name).first()
        if existing:
            existing.email = TEST_EMAIL
        else:
            db.add(Department(name=name, description=f"{name} department", email=TEST_EMAIL))
    db.commit()
    db.close()
    print("Departments seeded/updated with contact email.")

if __name__ == "__main__":
    seed()