import streamlit as st

st.set_page_config(
    page_title="Open AI Examples",

)

st.write("# Welcome to LLM Generative AI Demos.")

st.sidebar.info("Select a demo from sidebar.")

st.markdown(
    """
    # demos

    This is a set of examples created to explore
    - OpenAI API functionalities - content generation, audio transcription and summarization
    - Compare OpenAI and Stability Diffusion Image
    - Langchain and OpenAI API Integration

"""
)
