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

if "code" in query_params:
    st.success("Authorization code received!")
    st.write("This is where we’ll handle token exchange next.")
    st.code(query_params["code"][0])
else:
    st.write("To begin, sign in with Google:")
    st.markdown(f"[Click here to authenticate with Google]({AUTH_URL})")
