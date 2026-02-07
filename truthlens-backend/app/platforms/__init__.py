"""Platform-specific implementations for different social media platforms."""
from app.platforms.base import BasePlatform
from app.platforms.twitter import TwitterPlatform

__all__ = [
    "BasePlatform",
    "TwitterPlatform"
]
