from fastapi import FastAPI
from app.core.db import Base, engine
from app.projects.router import router as projects_router
from app.places.router import router as places_router

def create_app() -> FastAPI:
    app = FastAPI(title="Travel Projects API", version="1.0.0")
    Base.metadata.create_all(bind=engine)

    app.include_router(projects_router)
    app.include_router(places_router)
    return app

app = create_app()
