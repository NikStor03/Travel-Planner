from fastapi import FastAPI

def create_app() -> FastAPI:
    app = FastAPI(title="Travel Projects API", version="1.0.0")
    return app

app = create_app()
