"""
Week 5 Part E — Adding a /ask Endpoint to the FastAPI Service (Entry point)
"""
from app import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
