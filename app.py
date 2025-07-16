import streamlit as st
from requests_oauthlib import OAuth2Session
import os

st.set_page_config(page_title="Virtual Secretary", layout="wide")
st.title("🧠 Virtual Secretary")

# Load secrets
client_id = st.secrets["google_oauth"]["client_id"]
client_secret = st.secrets["google_oauth"]["client_secret"]
redirect_uri = st.secrets["google_oauth"]["redirect_uri"]

# OAuth endpoints
authorization_base_url = "https://accounts.google.com/o/oauth2/v2/auth"
token_url = "https://oauth2.googleapis.com/token"
scope = [
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/drive.readonly",
    "openid", "email", "profile"
]

# Session state setup
if "token" not in st.session_state:
    google = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
    authorization_url, state = google.authorization_url(
        authorization_base_url,
        access_type="offline",
        prompt="consent"
    )

    st.markdown(f"[Click here to authenticate with Google]({authorization_url})")

    st.stop()

else:
    # You'd add app logic here (e.g., compose email, add calendar event)
    st.success("✅ Authenticated! Ready to use Gmail, Calendar, and Drive.")
