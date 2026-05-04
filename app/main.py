"""FastAPI application for Text Summarization"""

from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import logging

from .models import SummarizationRequest, SummarizationResponse
from .utils import load_model_and_tokenizer, summarize_text

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize FastAPI app
app = FastAPI(
    title="Text Summarizer API",
    description="AI-powered text summarization using Hugging Face T5 transformer model",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# Setup template directory
templates = Jinja2Templates(directory=str(BASE_DIR / "app" / "templates"))

# Mount static files
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "app" / "static")), name="static")

# Load model and tokenizer
logger.info("Loading T5 model and tokenizer...")
try:
    model_path = BASE_DIR / "models" / "saved_summary_model"
    model, tokenizer, device = load_model_and_tokenizer(str(model_path))
    logger.info(f"Model loaded successfully on device: {device}")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    raise


# ==================== Routes ====================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the homepage"""
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/summarize", response_model=SummarizationResponse)
async def summarize(request_body: SummarizationRequest):
    """
    Generate a summary for the provided text.
    
    **Parameters:**
    - **dialogue** (str): Text content to summarize (10-10000 characters)
    
    **Returns:**
    - **summary** (str): AI-generated summary of the input text
    
    **Example:**
    ```json
    {
        "dialogue": "Your long text here..."
    }
    ```
    """
    try:
        # Generate summary
        summary = summarize_text(
            text=request_body.dialogue,
            model=model,
            tokenizer=tokenizer,
            device=device,
            max_length=150,
            num_beams=4
        )
        
        logger.info(f"Successfully generated summary (input: {len(request_body.dialogue)} chars, output: {len(summary)} chars)")
        return SummarizationResponse(summary=summary)
    
    except Exception as e:
        logger.error(f"Error during summarization: {e}")
        raise


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "model": "T5", "device": str(device)}


# ==================== Startup/Shutdown Events ====================

@app.on_event("startup")
async def startup_event():
    """Actions to perform on application startup"""
    logger.info("Text Summarizer API starting up...")
    logger.info(f"Base directory: {BASE_DIR}")
    logger.info(f"Using device: {device}")


@app.on_event("shutdown")
async def shutdown_event():
    """Actions to perform on application shutdown"""
    logger.info("Text Summarizer API shutting down...")
