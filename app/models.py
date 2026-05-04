"""Pydantic models for request/response validation"""

from pydantic import BaseModel, Field


class SummarizationRequest(BaseModel):
    """Request model for text summarization"""
    dialogue: str = Field(..., min_length=10, max_length=10000, description="Text to summarize")

    class Config:
        schema_extra = {
            "example": {
                "dialogue": "Your text to summarize goes here..."
            }
        }


class SummarizationResponse(BaseModel):
    """Response model for summarization results"""
    summary: str = Field(..., description="Generated summary")

    class Config:
        schema_extra = {
            "example": {
                "summary": "Generated summary text..."
            }
        }
