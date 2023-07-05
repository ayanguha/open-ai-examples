import streamlit as st
import openai
import time

import time
import requests, base64
import os

model = 'gpt-3.5-turbo'
engine_id = "stable-diffusion-v1-5"

def stability_image_gen(api_key, prompt, engine_id = "stable-diffusion-v1-5"):
    api_host = 'https://api.stability.ai'
    url = f"{api_host}/v1/generation/{engine_id}/text-to-image"
    headers = {"Content-Type": "application/json","Accept": "application/json","Authorization": f"Bearer {api_key}"    }
    body = {"text_prompts": [  {"text": prompt}], "height": 512, "width": 512, "samples": 1,"steps": 100, }
    response = requests.post(url, headers=headers, json=body)
    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))
    data = response.json()
    results = []
    for i, image in enumerate(data["artifacts"]):
        image_data = base64.b64decode(image["base64"])
        results.append(image_data)
    return results

st.set_page_config(page_title="Generate Image Idea", page_icon="")
st.markdown('''## Functionality
It is a toy example to create funny pictures. It provides a prompt `generate one original weird photo creation idea` and then use the result to generate the image

### Image Idea
Ideas are generated by using following APIs
- https://platform.openai.com/docs/api-reference/completions/create
- Python `openai` library https://github.com/openai/openai-python

### Images
Images are created using 2 models
- `Open AI` model using https://platform.openai.com/docs/api-reference/images/create
- `Stability AI` Stable Diffusion model using https://platform.stability.ai/rest-api to generate images

''')


st.sidebar.header("Generate Image Idea Demo")


st.write(
    """This demo illustrates a combination of creating an idea and then turn it to an image. Enjoy!"""
)

api_key_oi = st.text_input(label= "Open AI Key", value="", max_chars=None, key=None, type="default",
placeholder="Type Your Open AI API Key Here", disabled=False, label_visibility="visible")

api_key_sb = st.text_input(label= "Stability Diffusion Key", value="", max_chars=None, key=None, type="default",
placeholder="Type Stability Diffusion Key Here", disabled=False, label_visibility="visible")

while not api_key_oi:
    time.sleep(3)

while not api_key_sb:
    time.sleep(3)

openai.api_key = api_key_oi


completion = openai.ChatCompletion.create(
  model=model,max_tokens=100,
  messages=[
    {"role": "system",
    "content": "You are a creative art designer."},
    {"role": "user",
    "content": "Generate one original excellent photo idea inspired by work of street artist Banksy"},

  ]
)
#prompt = response['choices'][0]['text']
prompt = completion.choices[0].message['content']

st.write(prompt)

response = openai.Image.create(
  prompt=prompt,
  n=1,
  size="512x512"
)
open_ai_image_url = response['data'][0]['url']

stability_images = stability_image_gen(api_key = api_key_sb, prompt=prompt)


open_ai_tab, stability_tab = st.tabs(["Open AI", "Stability"])
with open_ai_tab:
   st.header("Image Generated by Open AI")
   st.image(open_ai_image_url)

with stability_tab:
   st.header("Image Generated by Stability AI")
   st.image(stability_images)

st.button("Re-run")