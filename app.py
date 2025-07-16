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
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        tokens = response.json()
        st.session_state.access_token = tokens["access_token"]
        st.success("✅ Google access granted!")
    else:
        st.error("❌ Token exchange failed.")
        st.stop()

# Show auth link if not authenticated yet
if "access_token" not in st.session_state:
    st.write("Please sign in with Google to begin:")
    st.markdown(f"[Click here to authenticate with Google]({AUTH_URL})")
    st.stop()

# Chatbot UI
client = OpenAI(api_key=OPENAI_KEY)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

prompt = st.text_input("What do you want me to do?", "")

if prompt:
    st.session_state.chat_history.append(("You", prompt))
    
    system_message = (
        "You are a virtual assistant with access to the user's Gmail, Calendar, and Drive. "
        f"The user's Google access token is: {st.session_state.access_token}. "
        "Use this info to decide what to do next. Respond with clear steps."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
    )

    reply = response.choices[0].message.content
    st.session_state.chat_history.append(("Secretary", reply))

for speaker, text in st.session_state.chat_history:
    st.markdown(f"**{speaker}:** {text}")
