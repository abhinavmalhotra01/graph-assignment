from fastapi import FastAPI
import os
from motor.motor_asyncio import AsyncIOMotorClient
from app.routers import graph_router
from app.routers import run_router

app = FastAPI()


@app.get("/test")
def test_app():
    return "App is up"

app.include_router(graph_router.router)
app.include_router(run_router.router)