from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from typing import List

# --- Configuration ---
app = FastAPI(
    title="Financial Sentiment Analysis API",
    description="A high-performance API for financial sentiment analysis and named entity recognition.",
    version="2.0.0"
)

# Get your Hugging Face API token from environment variables
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise ValueError("Hugging Face API token not found. Please set the HF_TOKEN environment variable.")

# Define the models we'll use from the Hugging Face Inference API
# Using a model fine-tuned for financial news
SENTIMENT_API_URL = "https://api-inference.huggingface.co/models/Sigma/financial-sentiment-analysis"
NER_API_URL = "https://api-inference.huggingface.co/models/dslim/bert-base-NER"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

# --- Pydantic Models for Data Validation ---
class TextPayload(BaseModel):
    inputs: str

class BatchTextPayload(BaseModel):
    inputs: List[str]

# --- Helper Function for API calls ---
def query_hf_api(api_url: str, payload: dict):
    """Reusable function to query the Hugging Face Inference API."""
    response = requests.post(api_url, headers=HEADERS, json=payload)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"Error from Hugging Face API: {response.text}")
    return response.json()

# --- API Endpoints ---

@app.get("/", tags=["Health Check"])
def read_root():
    """ A simple health-check endpoint. """
    return {"status": "ok", "message": "API is running"}

@app.post("/analyze-financial-sentiment", tags=["Sentiment Analysis"])
def analyze_financial_sentiment_single(payload: TextPayload):
    """
    Analyzes the sentiment of a single financial news headline.
    """
    return query_hf_api(SENTIMENT_API_URL, payload.dict())

@app.post("/analyze-financial-sentiment-batch", tags=["Sentiment Analysis"])
def analyze_financial_sentiment_batch(payload: BatchTextPayload):
    """
    Analyzes the sentiment of a batch of financial news headlines for improved performance.
    """
    # The `wait_for_model` option can be useful if the model is not always "hot"
    api_payload = {"inputs": payload.inputs, "options": {"wait_for_model": True}}
    return query_hf_api(SENTIMENT_API_URL, api_payload)

@app.post("/extract-financial-entities", tags=["Entity Recognition"])
def extract_financial_entities(payload: TextPayload):
    """
    Extracts named entities (like organizations, people, locations) from a single text.
    """
    return query_hf_api(NER_API_URL, payload.dict())

