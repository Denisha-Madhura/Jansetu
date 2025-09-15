from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.database import create_db_and_tables
from src.routes.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables...")
    await create_db_and_tables()
    yield
    print("Application shutting down...")


# FastAPI app instance
app = FastAPI(
    title="Jansetu Backend",
    description="Backend for Jansetu Application",
    version="0.0.1",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    lifespan=lifespan,
)


# Health check
@app.get("/ping")
async def ping():
    return {"response": "pong"}


# Include auth routes
app.include_router(auth_router)
