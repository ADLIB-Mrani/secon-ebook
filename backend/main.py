"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import Base, engine
from app.api.routes import ebook, templates, resources
from app.api.routes.templates import init_default_templates
from app.core.database import SessionLocal
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Automatic E-book Generation System"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ebook.router, prefix="/api/v1")
app.include_router(templates.router, prefix="/api/v1")
app.include_router(resources.router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    logger.info("Starting Secon E-book Generator...")
    
    # Initialize default templates
    db = SessionLocal()
    try:
        init_default_templates(db)
        logger.info("Default templates initialized")
    finally:
        db.close()


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/api/v1/info")
def api_info():
    """API information."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "endpoints": {
            "ebook": "/api/v1/ebook",
            "templates": "/api/v1/templates",
            "resources": "/api/v1/resources"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
