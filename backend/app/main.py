# Main application entry point (e.g., Flask/FastAPI app instance)
# API swagger docs: http://127.0.0.1:8000/docs
# To run: uvicorn main:app --reload

from fastapi import FastAPI
from database import get_db_status

app=FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/check-db-connection/")
async def check_db_connection():
    db_conn_status= get_db_status()
    return db_conn_status
