from fastapi import FastAPI

app = FastAPI(title="GrievAI API")

@app.get("/")
def root():
    return {"message": "GrievAI backend is running"}