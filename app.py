import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Virtual Secretary", layout="wide")
st.title("🧠 Virtual Secretary")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

prompt = st.text_input("What do you want me to do?", "")

if prompt:
    st.session_state.chat_history.append(("You", prompt))

    response = client.chat.completions.create(
        model="gpt-4-1106-nano",
        messages=[{"role": "user", "content": prompt}]
    )

    reply = response.choices[0].message.content
    st.session_state.chat_history.append(("Bot", reply))

for speaker, text in st.session_state.chat_history:
    st.markdown(f"**{speaker}:** {text}")
