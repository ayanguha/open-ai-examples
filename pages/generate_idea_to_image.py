import streamlit as st
import openai
import time


st.set_page_config(page_title="Generate Image Idea", page_icon="")
st.markdown('''## Objective:
This example explores following APIs
- https://platform.openai.com/docs/api-reference/completions/create
- https://platform.openai.com/docs/api-reference/images/create
- Python `openai` library https://github.com/openai/openai-python


## Functionality
It is a toy example to create funny pictures. It provides a prompt `generate one original weird photo creation idea` and then use the result to generate the image''')


st.sidebar.header("Generate Image Idea Demo")

model = 'text-davinci-003'
st.write(
    """This demo illustrates a combination of creating an idea and then turn it to an image via Open AI API. Enjoy!"""
)

api_key = st.text_input(label= "Open AI Key", value="", max_chars=None, key=None, type="default",
placeholder="Type Your Open AI API Key Here", disabled=False, label_visibility="visible")


while not api_key:
    time.sleep(3)
    st.spinner(text="In progress...")

openai.api_key = api_key

response = openai.Completion.create(
                  model=model,
                  prompt="generate one original weird photo creation idea",
                  max_tokens=100,
                  temperature=0.5
                    )
prompt = response['choices'][0]['text']

st.write(prompt)

response = openai.Image.create(
  prompt=prompt,
  n=1,
  size="512x512"
)
image_url = response['data'][0]['url']

st.image(image_url)

st.button("Re-run")
