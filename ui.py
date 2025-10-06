# ui.py

import streamlit as st
import requests
import json

# --- CONFIGURATION ---
# Replace this with the actual URL your Vercel deployment gives you.
# It's crucial that this URL points to your live FastAPI back-end.
API_URL = "/api/analyze-financial-sentiment" 


# --- HELPER FUNCTION ---
def call_sentiment_api(text_to_analyze):
    """
    Sends text to our FastAPI back-end for analysis and returns the result.
    """
    # The data we are sending in the POST request.
    # It needs to match the Pydantic model in our FastAPI app.
    payload = {"text": text_to_analyze}
    
    try:
        # Make the POST request to our API.
        # json.dumps converts our Python dictionary to a JSON string.
        response = requests.post(API_URL, data=json.dumps(payload))
        
        # If the request was successful (status code 200)
        if response.status_code == 200:
            # Return the JSON response from the API
            return response.json()
        else:
            # If the API returned an error, show it on the UI
            st.error(f"Error from API: {response.status_code} - {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        # Handle connection errors (e.g., API is down, no internet)
        st.error(f"Connection Error: Could not reach the API. Details: {e}")
        return None


# --- STREAMLIT APP INTERFACE ---

# Set the title of the web app
st.title("📈 Financial News Sentiment Analyzer")
st.subheader("A front-end for the sentiment analysis API tailored for JPMorgan")

# Create a text area for user input
user_input = st.text_area(
    "Enter a financial news headline to analyze:", 
    "Federal Reserve hints at interest rate cuts, boosting market confidence."
)

# Create a button. The code inside this 'if' block runs when the button is clicked.
if st.button("Analyze Sentiment"):
    if not user_input.strip():
        # Check if the user has entered any text
        st.warning("Please enter some text to analyze.")
    else:
        # Show a spinner while we wait for the API response
        with st.spinner("Analyzing..."):
            # Call our helper function to get the sentiment from the API
            result = call_sentiment_api(user_input)
            
            if result:
                # If we got a result back, display it
                st.subheader("Analysis Result:")
                
                label = result.get('label', 'N/A').upper()
                score = result.get('score', 0)
                
                # Display the result with some nice formatting
                if label == 'POSITIVE':
                    st.success(f"Sentiment: {label}")
                elif label == 'NEGATIVE':
                    st.error(f"Sentiment: {label}")
                else:
                    st.info(f"Sentiment: {label}")
                
                # Display the confidence score as a progress bar
                st.progress(score, text=f"Confidence: {score:.2%}")
                
                # Show the raw JSON response for technical users
                with st.expander("Show Raw API Response"):
                    st.json(result)