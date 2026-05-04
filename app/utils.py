"""Utility functions for text processing and model inference"""

import re
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
from typing import Tuple


def get_device() -> torch.device:
    """Detect and return the appropriate device (MPS, CUDA, or CPU)"""
    if torch.backends.mps.is_available():
        return torch.device("mps")
    elif torch.cuda.is_available():
        return torch.device("cuda")
    else:
        return torch.device("cpu")


def load_model_and_tokenizer(model_path: str) -> Tuple[T5ForConditionalGeneration, T5Tokenizer, torch.device]:
    """
    Load the T5 model and tokenizer from the specified path.
    
    Args:
        model_path: Path to the saved model directory
        
    Returns:
        Tuple of (model, tokenizer, device)
    """
    device = get_device()
    model = T5ForConditionalGeneration.from_pretrained(model_path)
    tokenizer = T5Tokenizer.from_pretrained(model_path)
    model.to(device)
    return model, tokenizer, device


def clean_text(text: str) -> str:
    """
    Clean and normalize input text for summarization.
    
    Removes:
    - Line breaks (\\r\\n)
    - Extra whitespace
    - HTML tags
    - Converts to lowercase
    
    Args:
        text: Raw input text
        
    Returns:
        Cleaned text
    """
    text = re.sub(r"\r\n", " ", text)      # Remove line breaks
    text = re.sub(r"\s+", " ", text)       # Normalize whitespace
    text = re.sub(r"<.*?>", " ", text)     # Remove HTML tags
    text = text.strip().lower()             # Strip and lowercase
    return text


def summarize_text(
    text: str,
    model: T5ForConditionalGeneration,
    tokenizer: T5Tokenizer,
    device: torch.device,
    max_length: int = 150,
    num_beams: int = 4
) -> str:
    """
    Generate a summary for the input text using T5 model.
    
    Args:
        text: Input text to summarize
        model: T5 model instance
        tokenizer: T5 tokenizer instance
        device: Torch device to use for inference
        max_length: Maximum length of generated summary
        num_beams: Number of beams for beam search
        
    Returns:
        Generated summary text
    """
    # Clean the input text
    cleaned_text = clean_text(text)
    
    # Tokenize
    inputs = tokenizer(
        cleaned_text,
        padding="max_length",
        max_length=512,
        truncation=True,
        return_tensors="pt"
    ).to(device)
    
    # Generate summary
    with torch.no_grad():  # Disable gradient computation for inference
        summary_ids = model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=max_length,
            num_beams=num_beams,
            early_stopping=True
        )
    
    # Decode the summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary
