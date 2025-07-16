import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Virtual Secretary", layout="wide")
st.title("🧠 Virtual Secretary")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

def handle_input():
    prompt = st.session_state.user_input.strip()
    if prompt:
        st.session_state.chat_history.append(("You", prompt))

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        reply = response.choices[0].message.content
        st.session_state.chat_history.append(("Bot", reply))

        # Clear the input box
        st.session_state.user_input = ""

# Input box with callback
st.text_input("What do you want me to do?", key="user_input", on_change=handle_input)

# Display chat history
for speaker, text in st.session_state.chat_history:
    st.markdown(f"**{speaker}:** {text}")
