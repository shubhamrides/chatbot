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

st.set_page_config(page_title="MyAssistant")
st.title("MyAssistant")

st.markdown(
    """
    <style>
      .block-container { padding-bottom: 140px; }

      div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 34px;
        left: 50%;
        transform: translateX(-50%);
        width: min(760px, calc(100% - 3rem));
        box-sizing: border-box;
        z-index: 1000;
      }

      .my-footer {
        position: fixed;
        bottom: 8px;
        left: 0;
        right: 0;
        text-align: center;
        font-size: 12px;
        color: #A7A8AA;
        z-index: 999;
      }
    </style>

    <div class="my-footer">Copyright © Shubham. All rights reserved.</div>
    """,
    unsafe_allow_html=True,
)

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
