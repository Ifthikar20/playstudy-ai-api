from fastapi import FastAPI
from database import Base, engine
from routers import users, scores, notes

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(users.router)
app.include_router(scores.router)
app.include_router(notes.router)

@app.get("/")
async def root():
    return {"message": "PlayStudy.AI Backend"}