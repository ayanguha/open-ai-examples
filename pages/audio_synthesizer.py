import streamlit as st
import openai
import time


st.set_page_config(page_title="Upload your own Audio file and synthesize content", page_icon="")
st.markdown("# Audio Synthesizer Demo")
st.sidebar.header("Audio Synthesizer Demo")

model = 'whisper-1'
st.write(
    """This demo illustrates a Audio transcript API and Summarization from Open AI. Enjoy!"""
)

api_key = st.text_input(label= "Open AI Key", value="", max_chars=None, key=None, type="default",
placeholder="Type Your Open AI API Key Here", disabled=False, label_visibility="visible")


while not api_key:
    time.sleep(3)
    st.spinner(text="In progress...")

openai.api_key = api_key

uploaded_file = st.file_uploader("Choose an audio file, in one of these formats: mp3, mp4, mpeg, mpga, m4a, wav, or webm.")

if uploaded_file is not None:
    st.write(uploaded_file)
    transcript = openai.Audio.transcribe("whisper-1",uploaded_file )

    transcribed_text = transcript['text']

    with st.expander("Transcribed Text"):
        st.write(transcribed_text)

    prompt = transcribed_text + "\n \n Tl;dr"

    model = 'text-davinci-003'

    response = openai.Completion.create(model=model,prompt = prompt,max_tokens=100)
    summarized_text = response['choices'][0]['text']

    with st.expander("Summarized Text"):
        st.write(summarized_text)




st.button("Re-run")
