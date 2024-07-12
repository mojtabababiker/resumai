#!/usr/bin/env python3
"""The main application module for the API.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.v1.views import auth

app = FastAPI(title="Resumai API", version="0.1.0", root_path="/api/v1")
app.include_router(auth.router)
# Add CORS middleware to allow cross-origin requests
origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# test route
@app.get("/status", tags=["status"])
def status() -> dict:
    return {"status": "ok"}
