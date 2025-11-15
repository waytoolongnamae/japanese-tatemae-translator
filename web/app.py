"""
FastAPI web server for Japanese Hedging Translator
Simple mobile-friendly web interface
"""
import os
import sys
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Add parent directory to path to import translator
sys.path.insert(0, str(Path(__file__).parent.parent))
from translator import JapaneseTatemaeTranslator
from processing.nodes import get_provider_info

# Initialize FastAPI app
app = FastAPI(
    title="Japanese Hedging Translator",
    description="Convert direct messages to polite Japanese business language",
    version="1.0.0"
)

# CORS middleware for API access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup templates and static files
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))
app.mount("/static", StaticFiles(directory=str(Path(__file__).parent / "static")), name="static")

# Initialize translator
translator = JapaneseTatemaeTranslator()


class TranslateRequest(BaseModel):
    """Request model for translation"""
    text: str = Field(..., min_length=1, max_length=5000, description="Text to translate")
    level: Optional[str] = Field("business", description="Politeness level: business, ultra_polite, casual")
    context: Optional[str] = Field(None, description="Optional context: business, personal, recruiter")


class TranslateResponse(BaseModel):
    """Response model for translation"""
    tatemae_text: str
    intent: str
    confidence: float
    detected_language: str
    level: str
    context: Optional[str] = None
    model_info: Optional[dict] = None


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main web interface"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    provider_info = get_provider_info()
    return {
        "status": "healthy",
        "service": "Japanese Hedging Translator",
        "model": provider_info
    }


@app.get("/api/model")
async def get_model_info():
    """Get current model information"""
    provider_info = get_provider_info()
    return provider_info


@app.post("/api/translate", response_model=TranslateResponse)
async def translate(request: TranslateRequest):
    """
    Translate direct text to Japanese tatemae (polite business language)

    **Parameters:**
    - text: The direct message to convert (1-5000 characters)
    - level: Politeness level (business, ultra_polite, casual)
    - context: Optional context (business, personal, recruiter)

    **Returns:**
    - Translation result with metadata
    """
    try:
        # Validate level
        valid_levels = ["business", "ultra_polite", "casual"]
        if request.level not in valid_levels:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid level. Must be one of: {', '.join(valid_levels)}"
            )

        # Perform translation
        result = translator.translate(
            request.text,
            level=request.level,
            context=request.context
        )

        # Check for errors in result
        if result.get("intent") == "error":
            raise HTTPException(
                status_code=400,
                detail=result.get("error", "Translation failed")
            )

        # Add model information
        provider_info = get_provider_info()
        result["model_info"] = provider_info

        return TranslateResponse(**result)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation error: {str(e)}")


@app.get("/api/examples")
async def get_examples():
    """Get example translations"""
    examples = [
        {
            "input": "I'm not interested in this job.",
            "intent": "disinterest",
            "description": "Politely declining a job offer"
        },
        {
            "input": "Your proposal won't work.",
            "intent": "criticism",
            "description": "Kyoto-style criticism disguised as praise"
        },
        {
            "input": "I can't meet this week.",
            "intent": "delay",
            "description": "Postponing a meeting politely"
        },
        {
            "input": "I disagree with that idea.",
            "intent": "disagreement",
            "description": "Expressing disagreement diplomatically"
        },
        {
            "input": "That's not possible.",
            "intent": "refusal",
            "description": "Refusing a request gently"
        }
    ]
    return {"examples": examples}


if __name__ == "__main__":
    import uvicorn
    import logging

    # Get port from environment or use default
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")

    print(f"\n🎌 Japanese Hedging Translator Web App")
    print(f"📱 Open in browser: http://localhost:{port}")
    print(f"🔄 API docs: http://localhost:{port}/docs")
    print(f"💡 Share this URL with others to use the app!\n")

    # Configure uvicorn logging with timestamp
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    log_config["formatters"]["default"]["datefmt"] = "%Y-%m-%d %H:%M:%S"
    log_config["formatters"]["access"]["fmt"] = '%(asctime)s - %(levelname)s - %(client_addr)s - "%(request_line)s" %(status_code)s'
    log_config["formatters"]["access"]["datefmt"] = "%Y-%m-%d %H:%M:%S"

    uvicorn.run(app, host=host, port=port, log_config=log_config)
