# Financial News Sentiment Analysis API
A high-performance, serverless REST API for real-time sentiment analysis of financial news headlines, tailored for accuracy in a financial services context.

# Overview
In the fast-paced world of finance, market sentiment can shift in minutes based on breaking news. This project provides a robust and scalable solution to automatically classify financial text as positive, negative, or neutral.

Unlike general-purpose sentiment models, this API leverages a RoBERTa-based model (cardiffnlp/twitter-roberta-base-sentiment-latest) specifically fine-tuned on financial and social media text. This ensures a higher degree of accuracy and a better understanding of domain-specific language (e.g., "bullish," "bearish," "rate hikes").

The application is built with FastAPI and deployed as a serverless function on Vercel, demonstrating a modern, scalable, and cost-efficient architecture.

# Live Demo URL: https://YOUR_VERCEL_APP_URL

# Key Features
Domain-Specific Accuracy: Utilizes a specialized NLP model for superior performance on financial text.

High-Performance API: Built with FastAPI for asynchronous, non-blocking I/O, ensuring low latency.

Serverless Deployment: Hosted on Vercel for infinite scalability and zero server management.

Data Validation: Employs Pydantic for robust, type-hinted validation of API requests.

Easy Integration: Provides a simple JSON-based RESTful endpoint for easy integration into trading algorithms, dashboards, or research platforms.

# API Usage

Once the application is running (either locally or on Vercel), you can send `POST` requests to the `/analyze-financial-sentiment` endpoint.

**Endpoint:** `/analyze-financial-sentiment`

**Method:** `POST`

**Body:**

```json
{
  "text": "Your financial news headline here"
}
```

## Example with cURL (Local)

```bash
curl -X POST "http://127.0.0.1:8000/analyze-financial-sentiment" -H "Content-Type: application/json" -d '{"text": "Interest rates are expected to rise next quarter."}'
```

# How To Run locally

to run this you need to create first a virtual environment:

- For macOS/Linux
python3 -m venv venv
source venv/bin/activate

- For Windows
python -m venv venv
.\venv\Scripts\activate

Install dependencies:

- python -m pip install --upgrade pip

- pip install -r requirement.txt

Run dev server:

- uvicorn api.index:app --reload

The local server will be available at `http://127.0.0.1:8000`.

# Run UI

To Run the UI for the analysis:

Open another CMD and reinstall dependencies:

- For Windows
python -m venv venv
.\venv\Scripts\activate

- python -m pip install --upgrade pip

- pip install -r requirement.txt

Run UI command via Streamlit:

- streamlit run ui.py

Most likely it will run as http://localhost:8501/