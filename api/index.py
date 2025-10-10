from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

# --- Configuration ---
app = FastAPI()

# Get your Hugging Face API token from environment variables
HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise ValueError("Hugging Face API token not found. Please set the HF_TOKEN environment variable.")

# Define the models we'll use from the Hugging Face Inference API
SENTIMENT_API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"
NER_API_URL = "https://api-inference.huggingface.co/models/dslim/bert-base-NER"

HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

# --- Pydantic Models for incoming data validation ---
class TextPayload(BaseModel):
    inputs: str

# --- API Endpoints ---

@app.get("/")
def read_root():
    """ A simple health-check endpoint. """
    return {"status": "ok", "message": "API is running"}


@app.post("/analyze-sentiment")
def analyze_sentiment_single(payload: TextPayload):
    """
    Analyzes the sentiment of a SINGLE text. This endpoint is called by the front-end.
    """
    response = requests.post(SENTIMENT_API_URL, headers=HEADERS, json=payload.dict())
    response.raise_for_status()  # This will raise an error for bad responses (4xx or 5xx)
    return response.json()


@app.post("/extract-entities")
def extract_entities(payload: TextPayload):
    """
    Extracts named entities from a single text.
    """
    response = requests.post(NER_API_URL, headers=HEADERS, json=payload.dict())
    response.raise_for_status()
    return response.json()

