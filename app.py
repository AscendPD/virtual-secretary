import streamlit as st
import os
import urllib.parse

# Load secrets
CLIENT_ID = st.secrets["google_oauth"]["client_id"]
REDIRECT_URI = st.secrets["google_oauth"]["redirect_uri"]
SCOPES = "https://www.googleapis.com/auth/calendar.readonly https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/drive.metadata.readonly"

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

query_params = st.query_params

import requests

if "code" in query_params:
    code = query_params["code"][0]

    # Exchange code for tokens
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": st.secrets["google_oauth"]["client_secret"],
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    response = requests.post(token_url, data=data)

    if response.status_code == 200:
        tokens = response.json()
        st.success("🎉 Access token retrieved successfully!")
        st.json(tokens)
    else:
        st.error("❌ Failed to exchange code for token.")
        st.write(response.text)

else:
    st.write("To begin, sign in with Google:")
    st.markdown(f"[Click here to authenticate with Google]({AUTH_URL})")
