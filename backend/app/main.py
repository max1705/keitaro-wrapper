from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app import models  # noqa: F401
from app.routers import campaigns, streams

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Keitaro Wrapper")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(campaigns.router)
app.include_router(streams.router)

@app.get("/health")
def health():
    return {"ok": True}