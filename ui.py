import streamlit as st
import requests
import os

# --- CONFIGURATION ---
# Allow overriding the API base URL with an environment variable for development
API_BASE_URL = os.getenv("API_BASE_URL", "https://sentiment-analysis-hhcd.onrender.com")
SENTIMENT_ENDPOINT_BATCH = f"{API_BASE_URL}/analyze-financial-sentiment-batch"
NER_ENDPOINT = f"{API_BASE_URL}/extract-financial-entities"

# --- HELPER FUNCTIONS ---
def call_api(endpoint, payload):
    """A reusable function to call our API endpoints."""
    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        # Provide a more user-friendly error message
        st.error(f"Connection Error: Could not reach the API. Please ensure the backend is running and accessible. Details: {e}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None

def process_ner_results(entities):
    """A helper function to clean up and group the raw results from the NER model."""
    if not entities or not isinstance(entities, list):
        return {}
    grouped_entities = {}
    for entity in entities:
        entity_type = entity.get('entity_group')
        word = entity.get('word')
        if entity_type and word:
            # Clean up the word if it's part of a subword token
            if word.startswith("##"):
                word = word[2:]

            if entity_type not in grouped_entities:
                grouped_entities[entity_type] = []

            # Simple logic to merge subwords into a single entity
            if not grouped_entities[entity_type] or not word.startswith("##"):
                grouped_entities[entity_type].append(word)
            else:
                grouped_entities[entity_type][-1] += word

    return grouped_entities


def display_sentiment(result):
    """Displays a single sentiment result in a formatted way."""
    if result and isinstance(result, list) and result[0]:
        sentiment = result[0]
        label = sentiment.get('label', 'UNKNOWN').upper()
        score = sentiment.get('score', 0)

        # The new model uses 'positive', 'negative', 'neutral'
        if label == 'POSITIVE':
            st.success(f"{label} (Confidence: {score:.2%})")
        elif label == 'NEGATIVE':
            st.error(f"{label} (Confidence: {score:.2%})")
        else:
            st.info(f"{label} (Confidence: {score:.2%})")
    else:
        st.error("Failed to parse sentiment result.")


# --- STREAMLIT APP INTERFACE ---
st.set_page_config(page_title="Financial Sentiment Analyzer", page_icon="📈", layout="wide")
st.title("📈 Financial News Sentiment & Entity Analyzer")

st.info("This tool uses a specialized financial NLP model to analyze multiple headlines at once.")
st.warning("Please note: The backend is hosted on a free service and may take a minute to 'wake up' on the first request. Subsequent analyses will be much faster.")

user_input = st.text_area(
    "Enter one or more financial news headlines (one per line):",
    "Federal Reserve hints at interest rate cuts, boosting market confidence.\nApple Inc. is expected to release its new iPhone next quarter, says Tim Cook.\nBerkshire Hathaway reports record earnings from its operations in Omaha.",
    height=150,
    key="headlines_input"
)

if st.button("Analyze Headlines", key="analyze_button"):
    headlines = [line.strip() for line in user_input.split('\n') if line.strip()]
    if not headlines:
        st.warning("Please enter at least one headline.")
    else:
        st.subheader("Analysis Results")

        # --- BATCH SENTIMENT ANALYSIS ---
        with st.spinner("Analyzing sentiment for all headlines..."):
            sentiment_payload = {"inputs": headlines}
            batch_sentiment_results = call_api(SENTIMENT_ENDPOINT_BATCH, sentiment_payload)

        # --- DISPLAY RESULTS PER HEADLINE ---
        for i, headline in enumerate(headlines):
            st.markdown("---")
            st.markdown(f"**Headline {i+1}:** *{headline}*")

            cols = st.columns(2)
            
            # Display sentiment for this headline from the batch results
            with cols[0]:
                st.markdown("**Sentiment**")
                if batch_sentiment_results and len(batch_sentiment_results) > i:
                    display_sentiment(batch_sentiment_results[i])
                else:
                    st.error("Could not retrieve sentiment for this headline.")

            # NER analysis (still done individually)
            with cols[1]:
                st.markdown("**Extracted Entities**")
                with st.spinner(f"Extracting entities for headline {i+1}..."):
                    ner_payload = {"inputs": headline}
                    ner_results = call_api(NER_ENDPOINT, ner_payload)
                
                entities = process_ner_results(ner_results)
                if entities:
                    for entity_type, words in entities.items():
                        # The new model sometimes returns 'LABEL_0', 'LABEL_1' etc.
                        # We can provide a mapping if needed, or just show the raw label.
                        st.markdown(f"**{entity_type}:** `{', '.join(words)}`")
                else:
                    st.text("No entities found.")
