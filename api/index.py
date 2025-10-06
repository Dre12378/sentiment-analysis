from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
import os

# Initialize the FastAPI app
app = FastAPI()

# --- Model Loading ---
# We load the model once when the application starts.
# This is more efficient than loading it on every request.
# The pipeline will download the model on the first run.
try:
    sentiment_pipeline = pipeline(
        "sentiment-analysis", 
        model="cardiffnlp/twitter-roberta-base-sentiment-latest"
    )
    model_ready = True
except Exception as e:
    print(f"Error loading model: {e}")
    model_ready = False


# --- Pydantic Model for Request Body ---
# This defines the expected data structure for incoming requests.
# It ensures that any request to our endpoint must have a "text" field which is a string.
class NewsArticle(BaseModel):
    text: str


# --- API Endpoints ---
@app.get("/")
def read_root():
    return {"status": "ok", "model_ready": model_ready}


@app.post("/analyze-financial-sentiment")
def analyze_sentiment(article: NewsArticle):
    """
    Analyzes the sentiment of a given financial news headline.
    """
    if not model_ready:
        return {"error": "Model is not available."}
    
    # The pipeline returns a list, so we take the first element.
    # The result from this model will be 'positive', 'negative', or 'neutral'.
    result = sentiment_pipeline(article.text)[0]
    return result