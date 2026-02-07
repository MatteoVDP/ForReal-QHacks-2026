"""AI media detection service using AI or Not API."""
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
        Check if an image or video is AI-generated using AI or Not API.
        
        Args:
            media_url: URL of the image or video
            media_type: Type of media ("image" or "video")
            
        Returns:
            MediaCheckResponse with ai_generated status, confidence, and message
        """
        if not settings.AIORNOT_API_KEY:
            raise ValueError("AIORNOT_API_KEY not configured")
        
        try:
            print(f"Checking {media_type}: {media_url[:100]}...")
            check_start = time.time()
            
            # AI or Not API uses simple Bearer token authentication
            headers = {
                "Authorization": f"Bearer {settings.AIORNOT_API_KEY.strip()}",
                "Content-Type": "application/json"
            }
            
            # AI or Not payload format
            payload = {
                "object": media_url
            }
            
            print(f"🔑 Using AI or Not API")
            print(f"📤 Request payload: {payload}")
            print(f"🌐 Endpoint: {settings.AIORNOT_API_URL}")
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                executor,
                lambda: requests.post(
                    settings.AIORNOT_API_URL,
                    headers=headers,
                    json=payload,
                    timeout=settings.AIORNOT_TIMEOUT
                )
            )
            
            print(f"📥 Response status: {response.status_code}")
            
            if response.status_code == 403:
                print("❌ 403 Forbidden - API key might be invalid")
                print(f"Response body: {response.text[:500]}")
                raise ValueError(f"AI or Not API authentication failed. Please check your API key.")
            
            if response.status_code == 400:
                print("❌ 400 Bad Request - Invalid payload")
                print(f"Response body: {response.text}")
                raise ValueError(f"AI or Not API bad request. Response: {response.text}")
            
            response.raise_for_status()
            data = response.json()
            print(f"✓ Response data received: {data}")
            
            check_time = time.time() - check_start
            print(f"⏱️  AI or Not check took: {check_time:.2f}s")
            
            # Parse AI or Not response
            # Response format: {"report": {"verdict": "ai" or "human", "confidence": 0.0-1.0}}
            verdict = data.get("report", {}).get("verdict", "unknown")
            confidence = data.get("report", {}).get("confidence", 0.5)
            
            ai_generated = verdict == "ai"
            
            # Determine message based on confidence
            if ai_generated:
                message = "Likely AI-generated" if confidence > 0.8 else "Possibly AI-generated"
            else:
                message = "Likely authentic" if confidence > 0.8 else "Uncertain"
            
            return MediaCheckResponse(
                ai_generated=ai_generated,
                confidence=confidence,
                media_type=media_type,
                message=message
            )
            
        except Exception as e:
            print(f"Error checking media: {str(e)}")
            raise
