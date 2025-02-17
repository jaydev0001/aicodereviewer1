import streamlit as st
import requests
import os

# Set your Google Gemini API key
GEMINI_API_KEY = os.getenv("AIzaSyALjH2TdADi2sCAvcrCdQ_IumnpZ3QjolY")  # Fetch from environment variable

if not GEMINI_API_KEY:
    st.error("Missing API Key! Set the GOOGLE_API_KEY environment variable.")


# Function to review the Python code using Gemini API
def review_code(user_code):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"Review this Python code for bugs and improvements:\n\n{user_code}"}
                ]
            }
        ]
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        try:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except KeyError:
            return "Unexpected response format. Check API response."
    else:
        return f"Error: {response.status_code} - {response.text}"


# Streamlit UI
def main():
    st.title("GenAI Code Reviewer (Powered by Gemini)")
    st.write("Submit your Python code for AI-powered review and suggestions.")

    user_code = st.text_area("Enter your Python code here:")

    if st.button("Review Code"):
        if user_code.strip():
            with st.spinner("Reviewing your code..."):
                feedback = review_code(user_code)
            st.subheader("AI Review Feedback:")
            st.markdown(feedback)
        else:
            st.warning("Please enter some Python code to review.")


if __name__ == "__main__":
    main()

# #streamlit run main.py
# # set GOOGLE_API_KEY=AIzaSyALjH2TdADi2sCAvcrCdQ_IumnpZ3QjolY

# import os
# print(os.getenv("GOOGLE_API_KEY"))  # Should print your API key

