from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow all CORS (you can tighten this later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request model
class PromptRequest(BaseModel):
    input: str
    type: str  # e.g. "next-line", "rewrite", etc.

@app.post("/prompt")
async def generate_prompt(prompt_request: PromptRequest):
    input_text = prompt_request.input
    prompt_type = prompt_request.type

    # Define how each type should be handled
    if prompt_type == "next-line":
        return {"result": f"Next line suggestion for: {input_text}"}
    elif prompt_type == "rewrite":
        return {"result": f"Rewritten version of: {input_text}"}
    elif prompt_type == "finish":
        return {"result": f"Completed version of: {input_text}"}
    elif prompt_type == "inspire":
        return {"result": f"Inspiration based on: {input_text}"}
    elif prompt_type == "hook":
        return {"result": f"Hook suggestion for: {input_text}"}
    else:
        return {"result": f"Unknown prompt type: {prompt_type}"}
