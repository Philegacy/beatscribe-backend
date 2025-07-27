from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model for incoming request
class LyricRequest(BaseModel):
    lyric: str
    action: Literal["rewrite", "next", "hook", "finish", "inspire"]

# Function to generate prompt
def generate_prompt(lyric: str, action: str) -> str:
    if action == "rewrite":
        return f"Rewrite this lyric to sound smoother, deeper, or more poetic:\n\n{lyric}"
    elif action == "next":
        return f"Suggest the next line for this lyric:\n\n{lyric}"
    elif action == "hook":
        return f"Generate a catchy hook based on this lyric or its mood:\n\n{lyric}"
    elif action == "finish":
        return f"Finish this verse creatively, continuing the flow:\n\n{lyric}"
    elif action == "inspire":
        return f"Provide a unique and inspiring idea for a new song based on this fragment or feeling:\n\n{lyric}"
    else:
        raise ValueError(f"Invalid action: {action}")

# FastAPI route
@app.post("/ai-lyric")
async def ai_lyric(request: LyricRequest):
    prompt = generate_prompt(request.lyric, request.action)

    # Call OpenRouter AI API
    headers = {
        "Authorization": "Bearer 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",  # Replace with your actual key
        "Content-Type": "application/json",
    }

    payload = {
        "model": "google/gemma-7b-it",  # Adjust model name if needed
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )

            data = response.json()
            reply = data["choices"][0]["message"]["content"]
            return {"suggestion": reply}
    except Exception as e:
        return {"error": str(e)}
