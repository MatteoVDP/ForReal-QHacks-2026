"""Base platform interface for social media platforms."""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class BasePlatform(ABC):
    """
    Abstract base class for platform-specific implementations.
    Each social media platform should implement this interface.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Platform name (e.g., 'twitter', 'facebook')."""
        pass
    
    @abstractmethod
    def extract_text(self, content: Dict[str, Any]) -> str:
        """
        Extract text content from platform-specific data structure.
        
        Args:
            content: Platform-specific content data
            
        Returns:
            Extracted text string
        """
        pass
    
    @abstractmethod
    def extract_media_urls(self, content: Dict[str, Any]) -> list:
        """
        Extract media URLs (images/videos) from platform-specific data.
        
        Args:
            content: Platform-specific content data
            
        Returns:
            List of media URLs with types
        """
        pass
    
    @abstractmethod
    def format_response(self, fact_check_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format fact-check response for platform-specific display.
        
        Args:
            fact_check_result: Standard fact-check result
            
        Returns:
            Platform-specific formatted response
        """
        pass
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocess text before fact-checking (e.g., remove hashtags, mentions).
        Can be overridden by platform implementations.
        
        Args:
            text: Raw text
            
        Returns:
            Preprocessed text
        """
        return text.strip()
