import streamlit as st
import openai
import time

st.title("Simple Chat Bot")

sidebar_container = st.sidebar.container()

styl = """
    <style>
        h1 {font-size: 40px;}
        h2 {font-size: 30px;}
        p {font-size: 14px;}
    </style>
    """

sidebar_container.write("# Welcome to LLM Generative AI Demos.")
sidebar_container.markdown(
    """

    # demos

    This is a set of examples created to explore
    - OpenAI API functionalities - content generation, audio transcription and summarization
    - Compare OpenAI and Stability Diffusion Image
    - Langchain and OpenAI API Integration

""", unsafe_allow_html=True
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

user_avatar = "slalom.png"
while "openai_key" not in st.session_state:
    st.error('Please add OpenAI Key in left panel and Press Enter')
    time.sleep(3)
openai.api_key = st.session_state["openai_key"]

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

def get_assistant_response():
    full_response = ""
    for response in openai.ChatCompletion.create(
        model=st.session_state["openai_model"],
        messages=[{"role":  m['role'], "content": m["content"]} for m in st.session_state.messages],
        stream=True,
    ):
        full_response += response.choices[0].delta.get("content", "")
    return full_response


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user", avatar=user_avatar):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = f"Echo: {prompt}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = get_assistant_response()
        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
