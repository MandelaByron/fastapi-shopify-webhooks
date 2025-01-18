# Entry point of the FastAPI application
from app.api.main import api_router
from fastapi import FastAPI

app = FastAPI()
app.include_router(api_router)
