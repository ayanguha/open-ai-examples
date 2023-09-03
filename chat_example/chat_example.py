import streamlit as st
import openai
import time

from model_interactions import *

st.title("Simple Chat Bot")

sidebar_container = st.sidebar.container()
avatars = {'user': "user.png", 'assistant': "assistant.png"}
def format_chat_history():
    h = []
    user_msg = [m['content'] for m in st.session_state.messages if m['role'] == 'user']
    assistant_msg = [m['content'] for m in st.session_state.messages if m['role'] == 'assistant']
    h = [ m for m in zip(user_msg, assistant_msg)]

    return h

sidebar_container.write("# Welcome to LLM Generative AI Demos.")
sidebar_container.markdown(
    """
    # demos

    This demo is a basic example of Retrieval Augmented Generation useing LLMs.
    It uses following features:
    - ```dataset``` library from Hugging Face https://huggingface.co/docs/datasets/index
    - ```OpenAI``` Embedding
    - ```Chroma``` as Vector Datastore
    - ```Langchain``` for Orchestration
    - ```strealit``` for frontend

"""
)


if api_key_oi := sidebar_container.text_input(label= "Open AI Key",
                                             value="",
                                             max_chars=None,
                                             key=None,
                                             type="default",
                                             placeholder="Type Your Open AI API Key Here",
                                             disabled=False,
                                             label_visibility="visible"):
    st.session_state["openai_key"] = api_key_oi

@st.cache_resource
def load_embeddings():
    ef = EmbeddingFactory(api_key = st.session_state["openai_key"])
    ef.load_vectorstore()
    ef.build_chain()

    st.session_state["embedding_done"] = True
    st.session_state["embedding"] = ef


while "openai_key" not in st.session_state:
    st.error('Please add OpenAI Key in left panel and Press Enter')
    time.sleep(3)

if 'embedding_done' not in st.session_state:
    load_embeddings()
    st.toast("Embedding Completed")


# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar = avatars[message["role"]]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user", avatar=avatars['user']):
        st.markdown(prompt)
    # Add user message to chat history
    # Display assistant response in chat message container
    with st.chat_message("assistant", avatar=avatars['assistant']):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = st.session_state["embedding"].chat_response(prompt, chat_history = format_chat_history())
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

    with sidebar_container:
        with st.container():
            with st.expander("Chat History"):
                for m in st.session_state.messages:
                    st.write(m)
            with st.expander("Relevant Docs"):
                for d in st.session_state["embedding"].get_relevant_docs(prompt):
                    st.write(d)
