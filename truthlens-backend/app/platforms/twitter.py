"""Twitter/X platform-specific implementation."""
import re
from typing import Dict, Any
from app.platforms.base import BasePlatform


class TwitterPlatform(BasePlatform):
    """Twitter/X-specific implementation."""
    
    @property
    def name(self) -> str:
        return "twitter"
    
    def extract_text(self, content: Dict[str, Any]) -> str:
        """
        Extract text from Twitter content.
        
        Args:
            content: Dict with 'text' field
            
        Returns:
            Extracted tweet text
        """
        return content.get("text", "").strip()
    
    def extract_media_urls(self, content: Dict[str, Any]) -> list:
        """
        Extract media URLs from Twitter content.
        
        Args:
            content: Dict with optional 'media' field
            
        Returns:
            List of dicts with 'url' and 'type' keys
        """
        media_list = content.get("media", [])
        return [
            {
                "url": item.get("url"),
                "type": item.get("type", "image")
            }
            for item in media_list
            if item.get("url")
        ]
    
    def format_response(self, fact_check_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format fact-check response for Twitter display.
        Currently returns standard format, but can be customized.
        
        Args:
            fact_check_result: Standard fact-check result
            
        Returns:
            Twitter-formatted response
        """
        # For now, return as-is. Can add Twitter-specific formatting here.
        return fact_check_result
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocess Twitter text by removing @mentions and cleaning hashtags.
        
        Args:
            text: Raw tweet text
            
        Returns:
            Preprocessed text
        """
        # Remove @mentions
        text = re.sub(r'@\w+', '', text)
        
        # Remove URLs
        text = re.sub(r'https?://\S+', '', text)
        
        # Clean up extra whitespace
        text = ' '.join(text.split())
        
        return text.strip()
