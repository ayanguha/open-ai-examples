from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from langchain import OpenAI, LLMChain
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
import streamlit as st
import time

model = 'text-davinci-003'

st.set_page_config(page_title="Jeopardy using Langchain", page_icon="")

st.sidebar.header("Jeopardy Using Langchain Demo")


st.markdown('''## Functionality
It is a toy example to play Jeopardy - code is using Langchain and Open AI.
This example uses following Langchain functionalities:
- PromptTemplate
- FewShotPromptTemplate
- Example Selectors - specifically SemanticSimilarityExampleSelector to choose most relevant examples.
   -- Vector DB as Chroma
   -- Embedding using OpenAIEmbeddings
- Example Sets
- LLM Chain - Using OpenAI

''')

api_key_oi = st.text_input(label= "Open AI Key", value="", max_chars=None, key=None, type="default",
placeholder="Type Your Open AI API Key Here", disabled=False, label_visibility="visible")

while not api_key_oi:
    time.sleep(3)

example_prompt = PromptTemplate(
    input_variables=["question", "answer"],
    template="Question: {question}\nAnswer: {answer}",
)

# These are a lot of examples of a pretend task of answering jeopardy.
examples = [
    {"question": 'The name of this Caribbean liqueur is from the Spanish for “aunt Mary.”',
     "answer": "What is Tia Maria"},
    {"question": 'If you’re in Central Asia, ask for shashlik; if you head down to the Middle East, ask for this 2-word skewered meat equivalent.',
     "answer": "What is Shish kebab"},
     {"question": 'How fitting that she starred in “Twelfth Night” in 2009—she has the same name as Shakespeare’s wife',
      "answer": "Who is Anne Hathaway"},
    {"question": 'In 1965, at age 20, Helen Mirren played this Egyptian at the Old Vic',
     "answer": "Who is Cleopatra"},
    {"question": 'In 2020 Dominic Thiem completed a comeback to win this event & became the first new male Grand Slam winner in 6 years.',
     "answer": "What is The U.S. Open"},
    {"question": 'In 2014, 2015 & 2019 Novak Djokovic defeated this Swiss player in the Wimbledon final.',
     "answer": "Who is Roger Federer"}
]

example_selector = SemanticSimilarityExampleSelector.from_examples(
    # This is the list of examples available to select from.
    examples,
    # This is the embedding class used to produce embeddings which are used to measure semantic similarity.
    OpenAIEmbeddings(openai_api_key=api_key_oi),
    # This is the VectorStore class that is used to store the embeddings and do a similarity search over.
    Chroma,
    # This is the number of examples to produce.
    k=3
)



similar_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    input_variables=["question"],
    validate_template = False,
    prefix='',
    suffix="Question: {question}\nAnswer:"
)

input = st.text_input(label="Provide a jeopardy question")
while not input:
    time.sleep(3)
#input = "At the 2012 French Open, this Russian completed her career slam."

llm = OpenAI(temperature=0,
             openai_api_key=api_key_oi,
             model = model)
llm_chain = LLMChain(llm=llm,prompt=similar_prompt)



result = llm_chain(input)
st.write(result['text'] + "?")

st.button("Re-run")
