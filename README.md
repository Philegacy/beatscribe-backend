d lyric rewriting and continuation functionality for the BeatScribe app.

## Features

- **Lyric Rewriting**: Transform existing lyrics to sound smoother, deeper, or more poetic
- **Lyric Continuation**: Generate the next line for existing lyrics
- **OpenRouter AI Integration**: Uses Google Gemma model for high-quality AI responses
- **CORS Enabled**: Ready for frontend integration
- **Health Check**: Built-in monitoring endpoint

## API Endpoints

- `POST /ai-lyric` - Main lyric processing endpoint
- `GET /health` - Health check endpoint
- `GET /` - Service information
- `GET /docs` - Interactive API documentation

## Quick Start

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set environment variable: `OPENROUTER_API_KEY`
4. Run: `uvicorn main:app --host 0.0.0.0 --port 5000`

## Deployment

This project is configured for deployment on Render. See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## API Usage

```bash
curl -X POST "http://localhost:5000/ai-lyric" \
  -H "Content-Type: application/json" \
  -d '{"lyric": "Walking down the street at night", "action": "next"}'
```

## Tech Stack

- FastAPI
- OpenRouter AI (Google Gemma model)
- Uvicorn
- Pydantic for validation
- HTTPX for async requests

## Environment Variables

- `OPENROUTER_API_KEY` - Required for AI functionality
