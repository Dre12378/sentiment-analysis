# Financial News Sentiment Analysis API (V2)
A high-performance, serverless REST API for real-time sentiment analysis of financial news headlines, tailored for accuracy in a financial services context.

# Overview
This project provides a robust and scalable solution to automatically classify financial text as positive, negative, or neutral.

Version 2.0 of this API upgrades the underlying NLP model to `Sigma/financial-sentiment-analysis`, a RoBERTa-based model specifically fine-tuned on financial news. This ensures a higher degree of accuracy and a better understanding of domain-specific language compared to general-purpose models.

The application is built with FastAPI and can be deployed as a serverless function on services like Vercel or Render, demonstrating a modern, scalable, and cost-efficient architecture.

# Key Features
- **Domain-Specific Accuracy**: Utilizes a specialized NLP model for superior performance on financial text.
- **High-Performance API**: Built with FastAPI for asynchronous, non-blocking I/O, ensuring low latency.
- **Batch Processing**: A `/analyze-financial-sentiment-batch` endpoint allows for analyzing multiple headlines in a single request, significantly improving efficiency.
- **Serverless Deployment**: Ready for hosting on platforms like Vercel for infinite scalability and zero server management.
- **Data Validation**: Employs Pydantic for robust, type-hinted validation of API requests.

# API Usage

Once the application is running, you can send `POST` requests to its endpoints.

## 1. Analyze a Single Headline

**Endpoint:** `/analyze-financial-sentiment`
**Method:** `POST`
**Body:**
```json
{
  "inputs": "Your financial news headline here"
}
```

## 2. Analyze Multiple Headlines (Batch)

**Endpoint:** `/analyze-financial-sentiment-batch`
**Method:** `POST`
**Body:**
```json
{
  "inputs": [
    "Headline one",
    "Headline two",
    "Headline three"
  ]
}
```

## Example with cURL (Local)

```bash
curl -X POST "http://127.0.0.1:8000/analyze-financial-sentiment" \
-H "Content-Type: application/json" \
-d '{"inputs": "Interest rates are expected to rise next quarter."}'
```

# How To Run Locally

### 1. Set Up Environment
First, create and activate a virtual environment:
```bash
# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

### 2. Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables
The API requires a Hugging Face API token. Export it as an environment variable:
```bash
export HF_TOKEN="your_hugging_face_api_token_here"
```
On Windows, use `set HF_TOKEN="your_token"` instead.

### 4. Run the API Server
Launch the backend server using Uvicorn:
```bash
uvicorn api.index:app --reload
```
The local server will be available at `http://127.0.0.1:8000`.

# How to Run the UI

The Streamlit UI connects to the API server.

### 1. (Optional) Set API URL for UI
If your API is running somewhere other than the default production URL, set the `API_BASE_URL` environment variable:
```bash
export API_BASE_URL="http://127.0.0.1:8000"
```
This tells the UI to connect to your local server.

### 2. Run the Streamlit App
In a **new terminal** (while the API server is still running), launch the UI:
```bash
streamlit run ui.py
```
The UI will be available at `http://localhost:8501`.

# Sample Look:

<img width="744" height="801" alt="image" src="https://github.com/user-attachments/assets/fae93a72-5647-4711-92ca-6612d1066afd" />
