# TruthLens Backend - Architecture Documentation

## 📁 Project Structure

```
truthlens-backend/
├── app/
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # FastAPI app entry point
│   ├── config.py                # Configuration & environment variables
│   │
│   ├── models/                  # Pydantic request/response models
│   │   ├── __init__.py
│   │   ├── fact_check.py       # Fact-checking models
│   │   └── media_check.py      # Media detection models
│   │
│   ├── services/                # Business logic layer
│   │   ├── __init__.py
│   │   ├── fact_check_service.py   # Fact-checking with Gemini
│   │   ├── media_check_service.py  # AI media detection with Hive
│   │   └── search_service.py       # Brave Search integration
│   │
│   ├── routers/                 # API endpoints
│   │   ├── __init__.py
│   │   ├── fact_check.py       # /api/fact-check endpoint
│   │   └── media.py            # /api/check-media endpoint
│   │
│   └── platforms/               # Platform-specific implementations
│       ├── __init__.py
│       ├── base.py             # Abstract base class
│       └── twitter.py          # Twitter/X implementation
│
├── main.py                      # Legacy entry point (redirects to app/main.py)
├── requirements.txt
├── .env
└── README.md
```

## 🏗️ Architecture Overview

### **1. Layered Architecture**

```
┌─────────────────────────────────────┐
│         API Routes Layer            │  ← FastAPI endpoints
│        (routers/*)                  │
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│      Business Logic Layer           │  ← Services
│        (services/*)                 │
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│      External APIs Layer            │  ← Gemini, Brave, Hive
│   (Gemini, Brave Search, Hive)     │
└─────────────────────────────────────┘
```

### **2. Separation of Concerns**

| Layer | Purpose | Files |
|-------|---------|-------|
| **Routes** | Handle HTTP requests/responses | `routers/*.py` |
| **Services** | Business logic & external API calls | `services/*.py` |
| **Models** | Data validation & serialization | `models/*.py` |
| **Config** | Environment & settings | `config.py` |
| **Platforms** | Platform-specific logic | `platforms/*.py` |

## 🚀 Running the Application

### **Option 1: Using new structure (recommended)**
```bash
cd truthlens-backend
python -m app.main
```

### **Option 2: Using legacy entry point**
```bash
cd truthlens-backend
python main.py
```

### **Option 3: Using uvicorn directly**
```bash
cd truthlens-backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📦 Adding New Features

### **Adding a New Platform (e.g., Facebook)**

1. Create `app/platforms/facebook.py`:
```python
from app.platforms.base import BasePlatform

class FacebookPlatform(BasePlatform):
    @property
    def name(self) -> str:
        return "facebook"
    
    def extract_text(self, content):
        # Facebook-specific text extraction
        pass
    
    def extract_media_urls(self, content):
        # Facebook-specific media extraction
        pass
```

2. Register in `app/platforms/__init__.py`:
```python
from app.platforms.facebook import FacebookPlatform
__all__ = ["BasePlatform", "TwitterPlatform", "FacebookPlatform"]
```

3. Use in routes:
```python
from app.platforms import FacebookPlatform

platform = FacebookPlatform()
text = platform.extract_text(content)
```

### **Adding a New API Endpoint**

1. Create a new router in `app/routers/`:
```python
# app/routers/sentiment.py
from fastapi import APIRouter
from app.models import SentimentRequest, SentimentResponse

router = APIRouter(prefix="/api", tags=["sentiment"])

@router.post("/analyze-sentiment")
async def analyze_sentiment(request: SentimentRequest):
    # Your logic here
    pass
```

2. Create models in `app/models/`:
```python
# app/models/sentiment.py
from pydantic import BaseModel

class SentimentRequest(BaseModel):
    text: str

class SentimentResponse(BaseModel):
    sentiment: str
    score: float
```

3. Create service in `app/services/`:
```python
# app/services/sentiment_service.py
class SentimentService:
    @staticmethod
    async def analyze(text: str):
        # AI analysis logic
        pass
```

4. Register router in `app/main.py`:
```python
from app.routers import sentiment_router
app.include_router(sentiment_router)
```

### **Adding a New External API Integration**

1. Add API configuration to `app/config.py`:
```python
class Settings:
    NEW_API_KEY: str = os.getenv("NEW_API_KEY", "")
    NEW_API_URL: str = "https://api.example.com"
```

2. Create service in `app/services/`:
```python
# app/services/new_api_service.py
import requests
from app.config import settings

class NewAPIService:
    @staticmethod
    async def call_api(data):
        response = requests.post(
            settings.NEW_API_URL,
            headers={"Authorization": f"Bearer {settings.NEW_API_KEY}"},
            json=data
        )
        return response.json()
```

## 🎯 Benefits of This Architecture

### **1. Modularity**
- Each feature is isolated in its own module
- Easy to add/remove features without affecting others
- Clear boundaries between components

### **2. Scalability**
- Add new platforms without touching existing code
- New features are self-contained
- Easy to split into microservices later

### **3. Testability**
- Each service can be tested independently
- Mock external APIs easily
- Unit test business logic separately from routes

### **4. Maintainability**
- Changes are localized to specific files
- Easy to find and fix bugs
- Clear code organization

### **5. Reusability**
- Services can be used across multiple routes
- Platform adapters can be shared
- Configuration is centralized

## 📚 Code Examples

### **Using Services in Routes**
```python
from app.services import FactCheckService, SearchService

@router.post("/fact-check")
async def fact_check(request: FactCheckRequest):
    # Search for sources
    results = await SearchService.search_claim(request.text)
    
    # Analyze with AI
    fact_check = await FactCheckService.synthesize_fact_check(
        request.text, request.text, results
    )
    
    return fact_check
```

### **Using Platform Adapters**
```python
from app.platforms import TwitterPlatform

platform = TwitterPlatform()
text = platform.preprocess_text(raw_tweet)  # Clean @mentions, URLs
media = platform.extract_media_urls(tweet_data)
```

### **Accessing Configuration**
```python
from app.config import settings

print(f"Using model: {settings.GEMINI_MODEL}")
print(f"Search timeout: {settings.SEARCH_TIMEOUT}s")
```

## 🔄 Migration from Legacy Code

The old monolithic `main.py` (450+ lines) has been refactored into:

| Old Code | New Location | Lines |
|----------|--------------|-------|
| Request/Response models | `app/models/*.py` | ~50 |
| Fact-checking logic | `app/services/fact_check_service.py` | ~120 |
| Media detection logic | `app/services/media_check_service.py` | ~80 |
| Search logic | `app/services/search_service.py` | ~90 |
| API routes | `app/routers/*.py` | ~60 |
| Configuration | `app/config.py` | ~80 |
| Platform logic | `app/platforms/*.py` | ~100 |

**Result:** 
- Old: 1 file, 450 lines
- New: 16 files, ~580 lines total (more code for better organization)
- Each file is < 150 lines (easier to understand and maintain)

## 🚦 Next Steps

1. **Test the new structure**: Run the server and verify all endpoints work
2. **Add new platforms**: Create `app/platforms/facebook.py`, `app/platforms/instagram.py`
3. **Add new features**: Create sentiment analysis, credibility scoring, etc.
4. **Write tests**: Add unit tests for each service
5. **Add documentation**: Generate API docs with FastAPI's built-in Swagger

## 🤝 Contributing

When adding new features:
1. Follow the established structure
2. Use services for business logic
3. Keep routes thin (just request/response handling)
4. Add models for all requests/responses
5. Update this README with new features
