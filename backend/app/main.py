"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.api.routes import router
from app.core.config import get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Council of Frontiers",
    description="Multi-Agent Verification Framework using LLM Debate",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    settings = get_settings()
    logger.info("Starting Council of Frontiers...")
    
    groq_keys = settings.get_groq_api_keys()
    if not groq_keys:
        logger.warning("GROQ_API_KEY not configured")
    else:
        logger.info(f"Groq API configured with {len(groq_keys)} key(s)")
    
    open_router_keys = settings.get_open_router_api_keys()
    if not open_router_keys:
        logger.warning("OPEN_ROUTER_API_KEY not configured")
    else:
        logger.info(f"OpenRouter API configured with {len(open_router_keys)} key(s)")
    
    nvidia_keys = settings.get_nvidia_api_keys()
    if not nvidia_keys:
        logger.warning("NVIDIA_API_KEY not configured")
    else:
        logger.info(f"NVIDIA NIM API configured with {len(nvidia_keys)} key(s)")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info("Shutting down Council of Frontiers...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
