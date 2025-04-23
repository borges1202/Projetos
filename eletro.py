import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

# -- Configuração do chatbot --
key = "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"
os.environ['GROQ_API_KEY'] = key

chat_bot = ChatGroq(model="llama-3.3-70b-versatile")

# -- Função para resposta do bot --
def bot_resposta(mensagens):
    modelo_mensagem = [
        ('system', """Você é um chatbot chamado EletroBot. 
        Você trabalha na empresa Eletrogoiás e ajuda os usuários com automação industrial. 
        Forneça respostas claras e inclua links úteis se aplicável, ajudando com a busca de componentes
        e na procura de links e datasheet. Exemplos de perguntas:
        - Onde encontro sensores industriais?
        - Como configurar um CLP para automação?
        - Datasheet do componente LM3914N-1""")
    ]
    modelo_mensagem += mensagens
    template = ChatPromptTemplate.from_messages(modelo_mensagem)
    chain = template | chat_bot
    return chain

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title('🤖-Assistente EletroGoias')
st.sidebar.header('-Eletrobot-')

# Exibe mensagens do histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Caixa de entrada para o usuário
if user_input := st.chat_input("Faça uma pergunta:"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Adiciona um container para a resposta do modelo
    response_container = st.chat_message("assistant")
    response_text = response_container.empty()

    # Obtendo a resposta do chatbot
    chat_chain = bot_resposta(st.session_state.messages)
    response_stream = chat_chain.stream({"text": user_input})
    full_response = ""

    for partial_response in response_stream:
        full_response += str(partial_response.content)
        response_text.markdown(full_response + "▌")

    # Salva a resposta completa no histórico
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    response_text.markdown(full_response)