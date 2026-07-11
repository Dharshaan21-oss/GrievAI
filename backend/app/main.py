from fastapi import FastAPI
from app.api.auth import router as auth_router

app = FastAPI(title="GrievAI API")

app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "GrievAI backend is running"}