# Fact-Check Browser Extension

## The Problem

Misinformation is everywhere, and is so easy to come by and just pass by. There is currently no very easy and verifiable way to quickly check if things are true or not, something that is as simple as looking at the misinformation itself.

---

## Solution

A browser extension that adds a magnifying glass icon next to tweets, enabling instant fact-checking with one click.

---

## Features

### Core Functionality
- **One-click verification:** Magnifying glass icon appears next to tweet actions (like, share, etc.)
- **Multi-source verification:** Cross-references multiple fact-checking databases
- **Transparent sourcing:** Shows which organizations verified the claim

### Output Format
- **Verification Label:** TRUE | FALSE | MISLEADING | UNVERIFIABLE
- **Confidence Score:** Based on source quality and consensus
- **Source Links:** Direct links to fact-check articles
- **Brief Explanation:** 1-2 sentence summary of findings

### Future Features
- Bias detection using sentiment analysis
- Support for LinkedIn, Reddit, Wikipedia
- Crowdsourced fact-check requests

---

## Technical Architecture

### Frontend: Chrome Extension
- **Framework:** Manifest V3 (Chrome/Firefox compatible)
- **Content Script:** Injects magnifying glass icons into Twitter DOM
- **UI Library:** React (optional) for popup interface
- **Styling:** Tailwind CSS

### Backend: API Server
- **Framework:** FastAPI (Python)
- **LLM:** Google Gemini API for claim extraction and synthesis
- **Vector Database:** Pinecone for semantic claim matching
- **External APIs:** 
  - Google Fact Check Tools API
  - ClaimBuster API
  - Perplexity/Tavily for web search

### System Flow

```
User clicks magnifying glass
         ↓
Extension extracts tweet text
         ↓
POST /api/fact-check
         ↓
Backend processes:
  1. Extract core claim (Gemini)
  2. Search fact-check databases
  3. Semantic similarity search (Pinecone)
  4. LLM verification if needed
         ↓
Return JSON response
         ↓
Display result in popup
```

---

## How It Works

1. **Claim Extraction:** Gemini API identifies the verifiable claim in the tweet
2. **Database Search:** Query Google Fact Check Tools API for existing fact-checks
3. **Semantic Matching:** Use Pinecone vector search to find similar claims that have been checked
4. **LLM Verification:** If no match found, Gemini performs web search and synthesizes findings
5. **Consensus Scoring:** Aggregate results from multiple sources and calculate confidence

---

## Confidence Scoring

**High Confidence (90-100%):**
- Exact claim match in 3+ fact-check sources
- Sources agree on rating

**Medium Confidence (60-89%):**
- Similar claim found
- 2 sources, or 1 authoritative source

**Low Confidence (30-59%):**
- AI-only verification
- Conflicting sources

**Unverifiable (<30%):**
- No relevant sources found
- Claim is opinion-based or too novel

---

## Limitations & Transparency

- Only checks claims that exist in fact-check databases or can be verified via web search
- Novel/breaking news may be unverifiable until fact-checkers review
- AI-assisted verification is marked separately from human fact-checks
- Privacy-first: No tweet content stored, anonymous API calls

---

## MVP Implementation Plan

### Phase 1: Backend API (Priority)
**Endpoint:** `POST /api/fact-check`
- Input: Tweet text
- Output: Label, sources, explanation, confidence score

**Core integrations:**
- Gemini API for claim processing
- Google Fact Check Tools API
- Pinecone for vector similarity

### Phase 2: Simple Web Interface
- Test backend with copy-paste interface
- Proves functionality before extension development
- Fallback demo if extension isn't complete

### Phase 3: Chrome Extension
- Manifest V3 extension setup
- Content script injection
- Popup UI for results display

---

## Target Platforms

**MVP:** X/Twitter (Chrome extension)

**Future Support:**
- LinkedIn (professional misinformation)
- Reddit (community fact-checking)
- Wikipedia (citation verification)

---

## Demo Strategy

**Test cases:**
1. Verified false claim (e.g., debunked conspiracy theory)
2. Verified true claim (e.g., confirmed news story)
3. Misleading claim (e.g., out-of-context quote)
4. Unverifiable claim (e.g., opinion statement)

**Success metrics:**
- Correctly identifies claim type
- Provides relevant sources
- Clear, understandable explanations
- <3 second response time