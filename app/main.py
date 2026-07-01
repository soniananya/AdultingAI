"""
Adulting AI — FastAPI application entry point.

Run locally with:
    uvicorn app.main:app --reload
"""

from fastapi import FastAPI

from app.routers import (
    users,
    documents,
    lifestate,
    workflows,
)

app = FastAPI(title="Adulting AI")


@app.get("/")
def health_check():
    return {"status": "ok", "service": "adulting-ai"}


app.include_router(users.router)
app.include_router(documents.router)
app.include_router(lifestate.router)
app.include_router(workflows.router)
