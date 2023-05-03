from flask import Flask, render_template,request,jsonify
import os

import time

import openai

model = 'text-davinci-003'

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/show_image', methods=['POST'])
def show_image():
    openai.api_key = request.json.get("api_key")
    response = openai.Completion.create(
                      model="text-davinci-003",
                      prompt="generate one original weird photo creation idea",
                      max_tokens=100,
                      temperature=0.5
                        )
    prompt = response['choices'][0]['text']
    response = openai.Image.create(
      prompt=prompt,
      n=1,
      size="256x256"
    )
    image_url = response['data'][0]['url']

    result = {'image_url': image_url, 'prompt': prompt}

    print(result)
    return jsonify(result)

@app.route('/translate', methods=['POST'])
def translate_data():
    inputText = request.json.get("inputText")
    sourceLanguageCode = request.json.get('sourceLanguageCode')
    translated_1 = translate.translate_text(Text=inputText,
                                      SourceLanguageCode=sourceLanguageCode,
                                      TargetLanguageCode="en")
    translated_1_text = translated_1.get('TranslatedText')

    gpt_response = translated_1_text
    translated_2 = translate.translate_text(Text=gpt_response,
                                      SourceLanguageCode="en",
                                      TargetLanguageCode=sourceLanguageCode)
    translated_2_text = translated_2.get('TranslatedText')

    result = {'original_text': inputText,
              'outputTextEng': gpt_response,
              'outputText': translated_2_text,
              }


    return jsonify(result)

def configure_app(flask_app):
    pass

def initialize_app(flask_app):
    configure_app(flask_app)

initialize_app(app)


def main():

    app.run(debug=True,host='0.0.0.0',port=5010)

if __name__ == "__main__":
    main()
