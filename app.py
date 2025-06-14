# from openai import OpenAI
import os
import streamlit as st
from core.question import run_csv_question_chain
from core.csv import get_csv_content

with st.sidebar:  
    openai_api_key = st.text_input("Gemini API Key", key="chatbot_api_key", type="password")
    "[Get an Gemini API key](https://aistudio.google.com/app/apikey)"

st.title("💬 Chatbot")
st.caption("🚀 Notas fiscais do mês de janeiro/2024 - disponibilizado pelo TCU")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Faça sua pergunta?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Por favor adicione sua Gemini API key pra continuar.")
        st.stop()
    
    os.environ["GOOGLE_API_KEY"] = openai_api_key
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    heads = get_csv_content('data/202401_NFs.zip', '202401_NFs_Cabecalho.csv')
    items = get_csv_content('data/202401_NFs.zip', '202401_NFs_Itens.csv')

    msg = run_csv_question_chain(prompt, {"heads": heads, "items": items})
    print(msg)

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)