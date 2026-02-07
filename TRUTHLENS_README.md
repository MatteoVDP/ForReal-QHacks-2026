# TruthLens 🔍

**Real-time fact-checking for X (Twitter) powered by AI**

TruthLens is a Chrome extension that adds a magnifying glass icon next to tweets, allowing users to instantly fact-check claims with AI-powered analysis and real-time web search.

---

## 🎯 Features

- **One-click fact-checking** directly on X.com
- **AI-powered claim extraction** using Google Gemini
- **Real-time web search** via Tavily API
- **Clear verdicts**: True, False, Misleading, or Unverifiable
- **Source citations** with clickable links
- **Confidence scoring** for transparency

---

## 🏗️ Architecture

### Frontend (Chrome Extension)
- Manifest V3 extension
- MutationObserver for dynamic tweet detection
- Vanilla JavaScript for lightweight performance
- Twitter-matching UI design

### Backend (FastAPI)
- `/api/fact-check` endpoint
- Google Gemini for claim extraction and synthesis
- Tavily API for authoritative source search
- Async processing for 3-5 second response times

---

## 🚀 Setup Instructions

### Prerequisites
- Python 3.9+
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- Tavily API key ([Get one here](https://tavily.com))
- Chrome or Firefox browser

### Backend Setup

1. **Navigate to backend directory:**
   ```powershell
   cd truthlens-backend
   ```

2. **Create virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure API keys:**
   ```powershell
   cp .env.example .env
   # Edit .env and add your API keys
   ```

5. **Run the server:**
   ```powershell
   python main.py
   ```
   
   Server will start at `http://localhost:8000`

### Extension Setup

1. **Navigate to extension directory:**
   ```powershell
   cd truthlens-extension
   ```

2. **Create placeholder icons** (or add your own 16x16, 48x48, 128x128 PNG files):
   ```powershell
   mkdir icons
   # Add icon16.png, icon48.png, icon128.png to the icons folder
   ```

3. **Load extension in Chrome:**
   - Open Chrome and go to `chrome://extensions/`
   - Enable "Developer mode" (top right)
   - Click "Load unpacked"
   - Select the `truthlens-extension` folder

4. **Test the extension:**
   - Navigate to [X.com](https://x.com)
   - Look for magnifying glass icons next to tweets
   - Click to fact-check!

---

## 🧪 Testing

### Backend Test
```powershell
# Test the API directly
curl -X POST http://localhost:8000/api/fact-check \
  -H "Content-Type: application/json" \
  -d '{"text": "The Earth is flat"}'
```

### Extension Test
1. Find a tweet with a factual claim on X.com
2. Click the magnifying glass icon
3. Wait 3-5 seconds for the fact-check overlay
4. Verify the label, sources, and explanation

---

## 📂 Project Structure

```
QHacks-2026/
├── truthlens-extension/
│   ├── manifest.json          # Extension configuration
│   ├── content.js             # Main content script
│   ├── styles.css             # UI styling
│   ├── popup.html             # Extension popup
│   └── icons/                 # Extension icons (add your own)
│       ├── icon16.png
│       ├── icon48.png
│       └── icon128.png
│
├── truthlens-backend/
│   ├── main.py                # FastAPI application
│   ├── requirements.txt       # Python dependencies
│   └── .env.example           # Environment template
│
└── README.md                  # This file
```

---

## 🔧 Configuration

### API Endpoint
By default, the extension calls `http://localhost:8000/api/fact-check`. To change this:

Edit `content.js` line 4:
```javascript
const API_ENDPOINT = 'https://your-deployed-backend.com/api/fact-check';
```

### Trusted Sources
The backend prioritizes these sources (edit in `main.py` line 154):
- Reuters
- AP News
- BBC
- Snopes
- FactCheck.org
- PolitiFact
- NPR

---

## 🎓 How It Works

1. **User clicks magnifying glass** on a tweet
2. **Extension extracts tweet text** using `data-testid="tweetText"`
3. **Backend receives request** at `/api/fact-check`
4. **Gemini extracts core claim** from tweet text
5. **Tavily searches** for authoritative sources
6. **Gemini synthesizes verdict** based on search results
7. **Extension displays result** with label, sources, and explanation

---

## ⚠️ Known Limitations

- **Coverage**: Only verifies claims found in indexed sources
- **Speed**: 3-5 second delay for web search + AI processing
- **Breaking news**: Very recent events may be unverifiable
- **Opinions**: Subjective statements return "Unverifiable"
- **Rate limits**: Dependent on API quotas

---

## 🚨 Troubleshooting

### Icon doesn't appear
- **Issue**: X.com changed its DOM structure
- **Fix**: Inspect tweet elements and update `data-testid` selectors in `content.js`

### API errors
- **Issue**: Missing or invalid API keys
- **Fix**: Verify `.env` file contains valid keys

### CORS errors
- **Issue**: Backend rejecting extension requests
- **Fix**: Check CORS middleware in `main.py` (line 19)

### "Unverifiable" for obvious facts
- **Issue**: Tavily didn't find relevant sources
- **Fix**: Check API quota or adjust search query in `main.py`

---

## 🏆 Built for QHacks 2026

**Team Members**: [Add your names]

**Technologies**:
- Frontend: Manifest V3, Vanilla JS, CSS
- Backend: FastAPI, Python
- AI: Google Gemini 1.5 Flash
- Search: Tavily API

---

## 📝 License

MIT License - feel free to use and modify for your hackathon projects!

---

## 🤝 Contributing

This is a hackathon project, but suggestions are welcome! Open an issue or submit a PR.

---

## 🙏 Acknowledgments

- Google Gemini for AI capabilities
- Tavily for search API
- X.com for... existing
- QHacks organizers for the opportunity
