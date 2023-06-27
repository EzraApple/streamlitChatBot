import streamlit as st
import azure.cognitiveservices.speech as speechsdk
from openai.error import AuthenticationError
from chatbot import ChatBot, VoiceBot

st.set_page_config(
    page_title='AI ChatBot',
    layout="wide",
    initial_sidebar_state="expanded"
)


def sidebar():
    if "openai" not in st.session_state:
        st.session_state.openai = ""
    if "azure" not in st.session_state:
        st.session_state.azure = ""

    st.sidebar.write("Welcome to my Chatbot")
    st.sidebar.selectbox("How would you like to chat today?",
                         [" ", "Text", "Voice"],
                         key="convo_type")
    if st.session_state.convo_type == "Text":
        st.session_state.openai = st.sidebar.text_input("Enter your OpenAI key: ")
    elif st.session_state.convo_type == "Voice":
        st.session_state.openai = st.sidebar.text_input("Enter your OpenAI key: ")
        st.session_state.azure = st.sidebar.text_input("Enter your Azure Speech Subscription Key: ")


def submit_chat():
    st.session_state.last_chat = st.session_state.chat_input
    st.session_state.chat_input = ''


def init_chat():
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [{
            "role": "system",
            "content": "You are a knowledgeable and helpful assistant. Please greet the user once and then respond helpfully."
        }]
    if 'last_chat' not in st.session_state:
        st.session_state.last_chat = ''


def display_chat_history():
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            out = "USER: " + message["content"]
            st.markdown(out)
        if message["role"] == "assistant":
            out = "BOT: " + message["content"]
            st.markdown(out)


def chat_window():
    if st.session_state.convo_type == "Text" and st.session_state.openai != "":
        try:
            bot = ChatBot(st.session_state.openai)
            init_chat()
            if st.session_state.last_chat != '':
                st.session_state.chat_history = bot.user_chat(st.session_state.last_chat, st.session_state.chat_history)
                st.session_state.chat_history, _ = bot.query_chat(st.session_state.chat_history)
                display_chat_history()
            else:
                st.session_state.chat_history, _ = bot.query_chat(st.session_state.chat_history)
                display_chat_history()
            st.text_input("Chat Input: ", key="chat_input", on_change=submit_chat, label_visibility="hidden")

        except AuthenticationError:
            st.subheader("Invalid OpenAI API Key, please make sure you copied it correctly")
    elif st.session_state.convo_type == "Voice" and st.session_state.openai != "" and st.session_state.azure != "":
        try:
            bot = VoiceBot(st.session_state.openai, st.session_state.azure)
            init_chat()
            if st.session_state.last_chat != '':
                st.write("Speak now")
                st.session_state.chat_history, st.session_state.last_chat = bot.get_speech(st.session_state.chat_history)
                st.write("Speech received")
                st.session_state.chat_history, _ = bot.speak_response(st.session_state.chat_history)
                st.experimental_rerun()
            else:
                st.session_state.chat_history, st.session_state.last_chat = bot.speak_response(st.session_state.chat_history)
                display_chat_history()
                st.experimental_rerun()


        except AuthenticationError:
            st.subheader("Invalid OpenAI API Key, please make sure you copied it correctly")
    else:
        st.write("---")
        st.subheader("Please make a selection from the sidebar and enter the corresponding information."
                 " Then you can chat with the bot.")
        st.write("---")


sidebar()
chat_window()
