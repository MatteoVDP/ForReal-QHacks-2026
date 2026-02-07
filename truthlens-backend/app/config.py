"""
Configuration management for TruthLens API.
Loads environment variables and provides configuration objects.
"""
import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""
    
    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    BRAVE_API_KEY: str = os.getenv("BRAVE_API_KEY", "")
    HIVE_API_KEY: Optional[str] = os.getenv("HIVE_API_KEY")
    
    # API Configuration
    GEMINI_MODEL: str = "gemini-2.0-flash-lite"
    BRAVE_SEARCH_URL: str = "https://api.search.brave.com/res/v1/web/search"
    HIVE_API_URL: str = "https://api.thehive.ai/api/v2/task/sync"
    
    # Search Configuration
    SEARCH_RESULT_COUNT: int = 5
    SEARCH_FRESHNESS: str = "pw"  # Past week
    MAX_SOURCES: int = 3
    
    # Trusted Domains for Fact-Checking
    TRUSTED_DOMAINS: list = [
        "reuters.com", "apnews.com", "bbc.com", "bbc.co.uk",
        "snopes.com", "factcheck.org", "politifact.com", 
        "npr.org", "theguardian.com", "nytimes.com",
        "washingtonpost.com", "cnn.com", "nbcnews.com"
    ]
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Thread Pool
    MAX_WORKERS: int = 5
    
    # Timeouts (seconds)
    SEARCH_TIMEOUT: int = 10
    HIVE_TIMEOUT: int = 30
    
    def validate(self):
        """Validate required configuration."""
        errors = []
        
        if not self.GEMINI_API_KEY:
            errors.append("GEMINI_API_KEY is required")
        if not self.BRAVE_API_KEY:
            errors.append("BRAVE_API_KEY is required")
        
        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")
        
        if not self.HIVE_API_KEY:
            print("⚠️  HIVE_API_KEY not set - AI media detection will be unavailable")
        
        return True


# Global settings instance
settings = Settings()

# Validate on import
try:
    settings.validate()
    print("✓ Configuration loaded and validated")
except ValueError as e:
    print(f"❌ Configuration error: {e}")
    raise
