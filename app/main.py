from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.config import Base, engine
from app.routes import api_router

# Create tables if they don't exist (For dev/test only, use Alembic in prod)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CobraGo API",
    description="Backend API for CobraGo collection management application.",
    version="1.0.0"
)

# Configure CORS for frontend access
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
    # Add other origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Welcome to CobraGo API. Go to /docs for Swagger UI."}
