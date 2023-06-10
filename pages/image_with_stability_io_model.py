import streamlit as st
import openai
import time
import requests, base64
import os


def stability_image_update(api_key, source_image, prompt, engine_id = "stable-diffusion-v1-5"):
    api_host = 'https://api.stability.ai'
    url = f"{api_host}/v1/generation/{engine_id}/image-to-image"
    headers = {"Accept": "application/json","Authorization": f"Bearer {api_key}"    }
    body = {"text_prompts[0][text]": prompt,
            "style_preset": "digital-art", "samples": 1,"steps": 100, }
    files = {"init_image": source_image }
    response = requests.post(url, headers=headers, files = files, data=body)
    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))
    data = response.json()
    results = []
    for i, image in enumerate(data["artifacts"]):
        image_data = base64.b64decode(image["base64"])
        results.append(image_data)
    return results



st.set_page_config(page_title="Modify Image Using Stability Diffusion", page_icon="")
st.markdown('''

## Functionality
It is a toy example to modify an image by providing a text prompt.

It uses API from `Stability AI`: https://platform.stability.ai/rest-api to modify images


''')


st.sidebar.header("Modify Image Demo")


engine_id = "stable-diffusion-v1-5"
st.write(
    """This demo illustrates how to modify an image using stability diffucion model. Enjoy!"""
)


api_key_sb = st.text_input(label= "Stability Diffusion Key", value="", max_chars=None, key=None, type="default",
placeholder="Type Stability Diffusion Key Here", disabled=False, label_visibility="visible")


while not api_key_sb:
    time.sleep(3)
    st.spinner(text="In progress...")

uploaded_file = st.file_uploader("Choose an image file")

prompt = st.text_input(label="Provide a prompt")

while not prompt:
    time.sleep(3)

images = stability_image_update(api_key = api_key_sb, source_image = uploaded_file, prompt=prompt)
with st.expander("Original Image"):
    st.image(uploaded_file)

with st.expander("Modified Image"):
    st.image(images)

st.button("Re-run")
