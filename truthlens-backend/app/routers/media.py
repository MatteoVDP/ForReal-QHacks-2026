"""AI media detection API routes."""
from fastapi import APIRouter, HTTPException
from app.models import MediaCheckRequest, MediaCheckResponse
from app.services import MediaCheckService

router = APIRouter(prefix="/api", tags=["media"])


@router.post("/check-media", response_model=MediaCheckResponse)
async def check_media(request: MediaCheckRequest):
    """
    Check if an image or video is AI-generated using Hive API.
    
    Args:
        request: MediaCheckRequest with media_url and media_type
        
    Returns:
        MediaCheckResponse with AI detection results
    """
    try:
        result = await MediaCheckService.check_media(
            request.media_url,
            request.media_type
        )
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        print(f"Error in check_media: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Media check error: {str(e)}")
