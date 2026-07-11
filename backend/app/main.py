from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.grievances import router as grievance_router

app = FastAPI(title="GrievAI API")

app.include_router(auth_router)
app.include_router(grievance_router)

@app.get("/")
def root():
    return {"message": "GrievAI backend is running"}