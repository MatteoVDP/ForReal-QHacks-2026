"""AI media detection service using Hive API."""
import requests
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from app.config import settings
from app.models import MediaCheckResponse

# Thread pool for async operations
executor = ThreadPoolExecutor(max_workers=settings.MAX_WORKERS)


class MediaCheckService:
    """Service for detecting AI-generated images and videos."""
    
    @staticmethod
    async def check_media(media_url: str, media_type: str) -> MediaCheckResponse:
        """
        Check if an image or video is AI-generated using Hive API.
        
        Args:
            media_url: URL of the image or video
            media_type: Type of media ("image" or "video")
            
        Returns:
            MediaCheckResponse with ai_generated status, confidence, and message
        """
        if not settings.HIVE_API_KEY:
            raise ValueError("HIVE_API_KEY not configured")
        
        try:
            print(f"Checking {media_type}: {media_url[:100]}...")
            check_start = time.time()
            
            headers = {
                "Authorization": f"Token {settings.HIVE_API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "url": media_url,
                "classes": ["ai_generated"]
            }
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                executor,
                lambda: requests.post(
                    settings.HIVE_API_URL,
                    headers=headers,
                    json=payload,
                    timeout=settings.HIVE_TIMEOUT
                )
            )
            response.raise_for_status()
            data = response.json()
            
            check_time = time.time() - check_start
            print(f"⏱️  Hive AI check took: {check_time:.2f}s")
            
            # Parse Hive response
            ai_generated = False
            confidence = 0.0
            
            if "status" in data and data["status"][0]["response"]["output"]:
                classes = data["status"][0]["response"]["output"][0]["classes"]
                for cls in classes:
                    if cls["class"] == "ai_generated":
                        confidence = cls["score"]
                        ai_generated = confidence > 0.5
                        break
            
            # Determine message based on confidence
            if ai_generated:
                message = "Likely AI-generated" if confidence > 0.8 else "Possibly AI-generated"
            else:
                message = "Likely authentic" if confidence < 0.2 else "Uncertain"
            
            return MediaCheckResponse(
                ai_generated=ai_generated,
                confidence=confidence,
                media_type=media_type,
                message=message
            )
            
        except Exception as e:
            print(f"Error checking media: {str(e)}")
            raise
