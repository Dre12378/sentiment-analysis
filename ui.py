import streamlit as st
import requests

# --- CONFIGURATION ---
# This URL points to our local back-end API server.
API_BASE_URL = "https://sentiment-analysis-hhcd.onrender.com"
SENTIMENT_ENDPOINT = f"{API_BASE_URL}/analyze-sentiment"
NER_ENDPOINT = f"{API_BASE_URL}/extract-entities"

# --- HELPER FUNCTIONS ---
def call_api(endpoint, payload):
    """A reusable function to call our API endpoints."""
    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()  # This will raise an error for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Connection Error: Could not reach the API. Is the back-end server running? Details: {e}")
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
            if entity_type not in grouped_entities:
                grouped_entities[entity_type] = []
            grouped_entities[entity_type].append(word)
    return grouped_entities

# --- STREAMLIT APP INTERFACE ---
st.set_page_config(page_title="Financial Sentiment Analyzer", page_icon="📈", layout="wide")
st.title("📈 Financial News Sentiment & Entity Analyzer")

st.info("This tool analyzes multiple headlines and extracts key entities like organizations (ORG) and people (PER).")

user_input = st.text_area(
    "Enter one or more financial news headlines (one per line):",
    "Federal Reserve hints at interest rate cuts, boosting market confidence.\nApple Inc. is expected to release its new iPhone next quarter, says Tim Cook.\nBerkshire Hathaway reports record earnings from its operations in Omaha.",
    height=150
)

if st.button("Analyze Headlines"):
    headlines = [line.strip() for line in user_input.split('\n') if line.strip()]
    if not headlines:
        st.warning("Please enter at least one headline.")
    else:
        st.subheader("Analysis Results")
        for i, headline in enumerate(headlines):
            st.markdown(f"---")
            st.markdown(f"**Headline {i+1}:** *{headline}*")
            cols = st.columns(2)
            
            with cols[0]:
                st.markdown("**Sentiment**")
                with st.spinner(f"Analyzing sentiment for headline {i+1}..."):
                    sentiment_payload = {"inputs": headline}
                    sentiment_results = call_api(SENTIMENT_ENDPOINT, sentiment_payload)
                
                if sentiment_results and isinstance(sentiment_results, list):
                    sentiment_result_list = sentiment_results[0]
                    if sentiment_result_list:
                        sentiment = sentiment_result_list[0]
                        label = sentiment['label'].upper()
                        score = sentiment['score']
                        if label == 'POSITIVE':
                            st.success(f"{label} (Confidence: {score:.2%})")
                        elif label == 'NEGATIVE':
                            st.error(f"{label} (Confidence: {score:.2%})")
                        else:
                            st.info(f"{label} (Confidence: {score:.2%})")
                else:
                    st.error("Failed to get sentiment result.")

            with cols[1]:
                st.markdown("**Extracted Entities**")
                with st.spinner(f"Extracting entities for headline {i+1}..."):
                     ner_payload = {"inputs": headline}
                     ner_results = call_api(NER_ENDPOINT, ner_payload)
                
                entities = process_ner_results(ner_results)
                if entities:
                    for entity_type, words in entities.items():
                        st.markdown(f"**{entity_type}:** `{', '.join(words)}`")
                else:
                    st.text("No entities found.")

