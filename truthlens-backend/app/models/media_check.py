"""Models for AI media detection."""
from pydantic import BaseModel


class MediaCheckRequest(BaseModel):
    """Request model for AI media detection."""
    media_url: str
    media_type: str  # "image" or "video"


class MediaCheckResponse(BaseModel):
    """Response model for AI media detection."""
    ai_generated: bool
    confidence: float
    media_type: str
    message: str
