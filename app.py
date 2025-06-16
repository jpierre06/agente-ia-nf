import os
import streamlit as st
from core.question import run_csv_question_chain
#from core.csv import get_csv_content
from core.data_loader import load_dataframes
from core.logger import save_chat_log

# Configurações do Streamlit
with st.sidebar:  
    api_key = st.text_input("Gemini API Key", key="chatbot_api_key", type="password")
    "[Get an Gemini API key](https://aistudio.google.com/app/apikey)"
    save_history = st.checkbox("Salvar histórico da conversa", value=False)
    

st.title("💬 Chatbot")
st.caption("🚀 Dados de Notas Fiscais - Disponibilizado pelo TCU")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Faça sua pergunta?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Digite sua pergunta sobre os dados..."):
    if not api_key:
        st.info("Por favor adicione sua Gemini API key pra continuar.")
        st.stop()
    
    os.environ["GOOGLE_API_KEY"] = api_key
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    with st.spinner("🔍 Analisando sua pergunta e consultando os dados..."):

        data = load_dataframes('data/202401_NFs.zip', [
        '202401_NFs_Cabecalho.csv',
        '202401_NFs_Itens.csv'
        ])

        if isinstance(data, str):  # erro ao carregar
            st.session_state.messages.append({"role": "assistant", "content": f"❌ {data}"})
            st.chat_message("assistant").write(f"❌ {data}")
            st.stop()

        code = ""

        try:
            msg, code = run_csv_question_chain(
                prompt, 
                {"heads": data['202401_NFs_Cabecalho.csv'],
                "items": data['202401_NFs_Itens.csv']}, 
                api_key=api_key
            )
        except Exception as e:
            msg = f"⚠️ Ocorreu um erro ao processar sua pergunta: {str(e)}"
            code = "Error."

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

    if save_history:
        save_chat_log(prompt, msg, code)