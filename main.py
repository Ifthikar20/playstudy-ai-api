from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from database import Base, engine
from routers import users, scores, notes

app = FastAPI()

# Create all DB tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(users.router)
app.include_router(scores.router)
app.include_router(notes.router)

@app.get("/")
async def root():
    return {"message": "PlayStudy.AI Backend"}

# Swagger Bearer token config
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="PlayStudy.AI API",
        version="1.0.0",
        description="API for PlayStudy.AI with JWT Bearer Authentication",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", []).append({"BearerAuth": []})
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
