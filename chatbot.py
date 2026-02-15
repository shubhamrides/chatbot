import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("Missing GROQ_API_KEY. Put it in .env or your environment.")
    st.stop()

client = Groq(api_key=api_key)

st.set_page_config(page_title="Chatbot")
st.title("Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]

for m in st.session_state.messages:
    if m["role"] in ("user", "assistant"):
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

prompt = st.chat_input("Type a message...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        streamed_text = ""

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages,
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=True,
        )

        for chunk in completion:
            delta = chunk.choices[0].delta.content or ""
            streamed_text += delta
            placeholder.markdown(streamed_text)

    st.session_state.messages.append({"role": "assistant", "content": streamed_text})
