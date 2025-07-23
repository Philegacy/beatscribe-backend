import os
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from typing import Literal
from dotenv import load_dotenv
import uvicorn

# Load environment variables
load_dotenv()

app = FastAPI(
    title="AI Lyric Service",
    description="FastAPI backend service for AI-powered lyric rewriting and continuation",
    version="1.0.0"
)

# Add CORS middleware to allow requests from any frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Pydantic models for request validation
class LyricRequest(BaseModel):
    lyric: str
    action: Literal["rewrite", "next"]
    
    @field_validator('lyric')
    @classmethod
    def lyric_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Lyric cannot be empty')
        return v.strip()

class LyricResponse(BaseModel):
    suggestion: str

# OpenRouter API configuration
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "google/gemma-2-9b-it:free"

async def call_openrouter_api(prompt: str) -> str:
    """
    Call OpenRouter API with the given prompt and return the AI's response
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500, 
            detail="OpenRouter API key not configured. Please set OPENROUTER_API_KEY environment variable."
        )
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5000",  # Optional: for OpenRouter analytics
        "X-Title": "AI Lyric Service"  # Optional: for OpenRouter analytics
    }
    
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 150,
        "temperature": 0.7,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                OPENROUTER_API_URL,
                json=payload,
                headers=headers
            )
            
            if response.status_code != 200:
                error_detail = f"OpenRouter API returned status {response.status_code}"
                try:
                    error_data = response.json()
                    if "error" in error_data:
                        error_detail += f": {error_data['error'].get('message', 'Unknown error')}"
                except:
                    error_detail += f": {response.text}"
                
                raise HTTPException(
                    status_code=502,
                    detail=f"Failed to get response from AI service. {error_detail}"
                )
            
            response_data = response.json()
            
            # Extract the AI's response from the API response
            if "choices" not in response_data or not response_data["choices"]:
                raise HTTPException(
                    status_code=502,
                    detail="Invalid response format from AI service"
                )
            
            ai_response = response_data["choices"][0]["message"]["content"].strip()
            return ai_response
            
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Request to AI service timed out. Please try again."
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to connect to AI service: {str(e)}"
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error occurred: {str(e)}"
        )

def generate_prompt(lyric: str, action: str) -> str:
    """
    Generate the appropriate prompt based on the action
    """
    if action == "rewrite":
        return f"Rewrite this lyric to sound smoother, deeper, or more poetic:\n\n{lyric}"
    elif action == "next":
        return f"Suggest the next line for this lyric:\n\n{lyric}"
    else:
        raise ValueError(f"Invalid action: {action}")

@app.post("/ai-lyric", response_model=LyricResponse)
async def ai_lyric(request: LyricRequest):
    """
    AI-powered lyric rewriting and continuation endpoint
    
    - **lyric**: The lyric text to process
    - **action**: Either "rewrite" to improve the lyric or "next" to suggest the next line
    
    Returns the AI's suggestion in the response.
    """
    try:
        # Generate the appropriate prompt based on the action
        prompt = generate_prompt(request.lyric, request.action)
        
        # Call OpenRouter API
        ai_response = await call_openrouter_api(prompt)
        
        # Return the clean response
        return LyricResponse(suggestion=ai_response)
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Handle any other unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """
    Simple health check endpoint
    """
    return {"status": "healthy", "service": "AI Lyric Service"}

@app.get("/")
async def root():
    """
    Root endpoint with basic service information
    """
    return {
        "message": "AI Lyric Service",
        "version": "1.0.0",
        "endpoints": {
            "ai_lyric": "/ai-lyric (POST)",
            "health": "/health (GET)",
            "docs": "/docs (GET)"
        }
    }

if __name__ == "__main__":
    # Auto-reload configuration for fast development
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=5000,
        reload=True,  # Auto-reload on file changes
        log_level="info"
          )
