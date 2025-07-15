import streamlit as st
import openai

st.set_page_config(page_title="Virtual Secretary", layout="wide")
st.title("🧠 Virtual Secretary")

# Use your OpenAI key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

prompt = st.text_input("What do you want me to do?", "")

if prompt:
    st.session_state.chat_history.append(("You", prompt))
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    reply = response['choices'][0]['message']['content']
    st.session_state.chat_history.append(("Bot", reply))

for speaker, text in st.session_state.chat_history:
    st.markdown(f"**{speaker}:** {text}")
