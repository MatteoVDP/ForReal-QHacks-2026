"""
TruthLens API - Main application entry point.
Refactored modular architecture for scalability.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import fact_check_router, media_router

print("=" * 50)
print("🚀 Initializing TruthLens API")
print("=" * 50)

# Initialize FastAPI app
app = FastAPI(
    title="TruthLens API",
    version="1.0.0",
    description="AI-powered fact-checking and media verification API"
)
print("✓ FastAPI app initialized")

# Configure CORS for Chrome Extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your extension ID
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
print("✓ CORS middleware configured")

# Include routers
app.include_router(fact_check_router)
app.include_router(media_router)
print("✓ API routers registered")

print("=" * 50)
print(f"✅ TruthLens API Ready")
print(f"📍 Model: {settings.GEMINI_MODEL}")
print(f"🔍 Search: Brave Search API")
print(f"🤖 Media Detection: {'Enabled' if settings.HIVE_API_KEY else 'Disabled'}")
print("=" * 50)


@app.get("/")
async def root():
    """Root endpoint - API status."""
    return {
        "message": "TruthLens API is running",
        "version": "1.0.0",
        "features": {
            "fact_check": True,
            "media_check": bool(settings.HIVE_API_KEY)
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "model": settings.GEMINI_MODEL,
        "search": "brave",
        "media_detection": bool(settings.HIVE_API_KEY)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT
    )
