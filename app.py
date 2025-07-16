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
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/drive.metadata.readonly",
    "https://www.googleapis.com/auth/contacts.readonly",
)


AUTH_URL = (
    "https://accounts.google.com/o/oauth2/v2/auth"
    f"?client_id={CLIENT_ID}"
    f"&redirect_uri={urllib.parse.quote(REDIRECT_URI)}"
    f"&response_type=code"
    f"&scope={urllib.parse.quote(' '.join(SCOPES))}"
    f"&access_type=offline"
    f"&prompt=consent"
)

st.set_page_config(page_title="Virtual Secretary", layout="wide")
st.title("🧠 Virtual Secretary")

query_params = st.query_params

if "code" in query_params and "access_token" not in st.session_state:
    code = query_params["code"]
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    try:
        response = requests.post(token_url, data=data, timeout=10)
    except Exception as e:
        st.error(f"❌ Token request failed: {e}")
        st.stop()

    if response.status_code == 200:
        tokens = response.json()
        st.session_state.access_token = tokens["access_token"]
        st.success("✅ Google access granted!")
    else:
        st.error("❌ Token exchange failed.")
        st.stop()

# Auth step
if "access_token" not in st.session_state:
    st.write("Please sign in with Google to begin:")
    st.markdown(f"[Click here to authenticate with Google]({AUTH_URL})")
    st.stop()

# Chatbot UI
client = OpenAI(api_key=OPENAI_KEY)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    st.subheader("💬 Chat with your Virtual Secretary")

user_input = st.text_input("You:", key="user_input")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.spinner("Thinking..."):
        # Step 2: Enhanced chatbot logic with intent extraction
        system_prompt = (
            "You are a helpful virtual secretary. If the user asks you to send an email, "
            "parse it and reply with a JSON object like this: "
            "{\"action\": \"send_email\", \"name\": \"Priscilla\", \"message\": \"Let's meet at 2pm\"}.\n"
            "If the input is not an actionable command, just reply conversationally."
        )


messages = [
    {"role": "system", "content": system_prompt}
] + st.session_state.chat_history

with st.spinner("Thinking..."):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
    )

    reply = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": reply})

# Display full chat history
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"🧑‍💻 **You:** {msg['content']}")
    else:
        st.markdown(f"🤖 **Assistant:** {msg['content']}")
