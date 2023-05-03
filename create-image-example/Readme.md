# create-image-example

## Objective:
This example explores following APIs
- https://platform.openai.com/docs/api-reference/completions/create
- https://platform.openai.com/docs/api-reference/images/create
- Python `openai` library https://github.com/openai/openai-python


## Functionality
It is a toy example to create funny pictures. It provides a prompt `generate one original weird photo creation idea` and then use the result to generate the image

## Deployed Example:
https://0gzujy8pfk.execute-api.ap-southeast-2.amazonaws.com/dev

## How to deploy
- Clone this repo
- Create a python virtual environment 
- Install Python dependencies `pip install requirements.txt`
- Install `serverless` for deployment (refer: https://www.serverless.com/)
- run `serverless deploy`
