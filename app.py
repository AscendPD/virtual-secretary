import streamlit as st
import os
import urllib.parse
import time
import requests

# Load secrets
CLIENT_ID = st.secrets["google_oauth"]["client_id"]
REDIRECT_URI = st.secrets["google_oauth"]["redirect_uri"]
CLIENT_SECRET = st.secrets["google_oauth"]["client_secret"]

SCOPES = (
    "https://www.googleapis.com/auth/calendar.readonly "
    "https://www.googleapis.com/auth/gmail.readonly "
    "https://www.googleapis.com/auth/drive.metadata.readonly"
)

# Build Google OAuth URL
AUTH_URL = (
    "https://accounts.google.com/o/oauth2/v2/auth"
    f"?client_id={CLIENT_ID}"
    f"&redirect_uri={urllib.parse.quote(REDIRECT_URI)}"
    f"&response_type=code"
    f"&scope={urllib.parse.quote(SCOPES)}"
    f"&access_type=offline"
    f"&prompt=consent"
)

st.title("🧠 Virtual Secretary")
st.write("Loading app...")

query_params = st.query_params
st.write("Full query params:", query_params)  # ✅ DEBUG: See what's inside

if "code" in query_params:
    raw_code = query_params["code"]
    st.write("Raw code value:", raw_code)  # ✅ DEBUG: Before checking type

    # If it's a list, extract the first item
    if isinstance(raw_code, list):
        code = raw_code[0]
    else:
        code = raw_code

    st.write("Final code used:", code)  # ✅ DEBUG: The actual code being sent


    # Exchange authorization code for tokens
    st.write("✅ Step 2: Preparing token request...")

    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    st.write("✅ Step 3: Sending POST to token endpoint...")

    try:
        response = requests.post(token_url, data=data, timeout=10)
        st.write("✅ Step 4: Response received.")
    except Exception as e:
        st.error(f"❌ Request failed: {e}")
    else:
        if response.status_code == 200:
            st.write("✅ Step 5: Token retrieved successfully.")
            tokens = response.json()
            st.success("🎉 Access token retrieved!")
            st.json(tokens)
        else:
            st.error("❌ Failed to exchange code for token.")
            st.write(response.text)

else:
    st.write("To begin, sign in with Google:")
    st.markdown(f"[Click here to authenticate with Google]({AUTH_URL})")
