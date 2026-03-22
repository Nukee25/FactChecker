# FactChecker

AI-powered fact verification system that validates text integrity against real-time web data.

## Features
- **Claim Extraction**: Automatically identifies verifiable claims in text or articles
- **Evidence Retrieval**: Searches the web to find relevant sources for each claim
- **Verification**: AI-powered analysis comparing claims against evidence
- **AI Detection**: Identifies whether content is AI-generated (bonus feature)
- **Real-time Progress**: Streaming updates as each stage completes

## Tech Stack
- **Backend**: Python FastAPI with async streaming
- **Frontend**: React + Vite + TailwindCSS
- **LLM**: Local Ollama models
- **Search**: DuckDuckGo Search API

## Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- Ollama installed and running locally

### Backend
```bash
cd backend
pip install -r requirements.txt
# Optional: choose custom host/model
# export OLLAMA_HOST=http://localhost:11434
# export OLLAMA_MODEL=llama3.1
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 in your browser.

## Usage
1. Choose input type: **Text** or **URL**
2. Enter your content or paste a news article URL
3. Click **Verify Facts**
4. Watch the real-time verification pipeline
5. Review the detailed accuracy report with citations
