from fastapi import FastAPI
from app.core.db import Base, engine
def create_app() -> FastAPI:
    app = FastAPI(title="Travel Projects API", version="1.0.0")
    Base.metadata.create_all(bind=engine)

    return app

app = create_app()
