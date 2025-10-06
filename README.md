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

# How To Run locally

to run this you need to create first a virtual environment:

- For macOS/Linux
python3 -m venv venv
source venv/bin/activate

- For Windows
python -m venv venv
.\venv\Scripts\activate

- Install dependencies

pip install -r requirement.txt

- Run dev server

uvicorn api.index:app --reload