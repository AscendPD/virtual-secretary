import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Virtual Secretary", layout="wide")
st.title("🧠 Virtual Secretary")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Initialize prompt input state
if "prompt_input" not in st.session_state:
    st.session_state.prompt_input = ""

# Capture user input
prompt = st.text_input("What do you want me to do?", value=st.session_state.prompt_input, key="prompt_input")

if prompt:
    # Append user message
    st.session_state.chat_history.append(("You", prompt))

    # Get assistant reply
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    reply = response.choices[0].message.content
    st.session_state.chat_history.append(("Bot", reply))

    # Clear input field
    st.session_state.prompt_input = ""

# Display chat history
for speaker, text in st.session_state.chat_history:
    st.markdown(f"**{speaker}:** {text}")
