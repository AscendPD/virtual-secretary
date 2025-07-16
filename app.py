import streamlit as st
import os
import urllib.parse
import requests
from openai import OpenAI

# Load secrets
CLIENT_ID = st.secrets["google_oauth"]["client_id"]
CLIENT_SECRET = st.secrets["google_oauth"]["client_secret"]
REDIRECT_URI = st.secrets["google_oauth"]["redirect_uri"]
OPENAI_KEY = st.secrets["OPENAI_API_KEY"]

SCOPES = (
    "https://www.googleapis.com/auth/calendar "
    "https://www.googleapis.com/auth/gmail.send "
    "https://www.googleapis.com/auth/drive.metadata.readonly"
)

AUTH_URL = (
    "https://accounts.google.com/o/oauth2/v2/auth"
    f"?client_id={CLIENT_ID}"
    f"&redirect_uri={urllib.parse.quote(REDIRECT_URI)}"
    f"&response_type=code"
    f"&scope={urllib.parse.quote(SCOPES)}"
    f"&access_type=offline"
    f"&prompt=consent"
)

st.set_page_config(page_title="Virtual Secretary", layout="wide")
st.title("🧠 Virtual Secretary")

query_params = st.query_params

if "code" in query_params and "access_token" not in st.session_state:
    code = query_params["code"][0]
    st.markdown(f"✅ Step 1: Code received: `{code}`")
    
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    st.markdown("✅ Step 2: Preparing token request...")
    st.json(data)

    try:
        response = requests.post(token_url, data=data, timeout=10)
    except Exception as e:
        st.error(f"❌ Step 3: Request failed: {e}")
        st.stop()

    st.markdown("✅ Step 3: Response received.")
    st.json(response.json())

    if response.status_code == 200:
        tokens = response.json()
        st.session_state.access_token = tokens["access_token"]
        st.success("✅ Google access granted!")
    else:
        st.error("❌ Token exchange failed.")
        st.code(response.text)
        st.stop()

# Auth step
if "access_token" not in st.session_state:
    st.write("Please sign in with Google to begin:")
    st.markdown(f"[Click here to authenticate with Google]({AUTH_URL})")
    st.stop()

# Chatbot UI
client = OpenAI(api_key=OPENAI_KEY)
if "chat_history" not in st.se_:
