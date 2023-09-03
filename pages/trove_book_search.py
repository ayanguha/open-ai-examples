from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.document_loaders import CSVLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI

import streamlit as st
import os, time

print(os.path.dirname(os.path.realpath(__file__)))
print(os.listdir())



st.set_page_config(page_title="Trove Book Search", page_icon="")

st.sidebar.header("Trove Book Search Using Langchain Demo")


st.markdown('''## Functionality
It is a toy example to search a book catalog - code is using Langchain and Open AI.
This example uses following Langchain functionalities:
- CSV Loader: to load a csv file
- CharacterTextSplitter: to slice the document in 1000 Character chunks
- OpenAIEmbeddings: Get Embeddings from OpenAI API. Requires OpenAI API Keys
- Chroma.from_documents: Initialise a local Chroma storage and store documents with embeddings
- similarity_search_with_score: Run similarity search between query and stored embeddings
- RetrievalQA: A complete chain to retrieve documents from the vector store and then pass on to OpenAI LLM
               for sematic search and the finally complete the response

''')

loader = CSVLoader(file_path="trove_digitised_books.csv")
documents = loader.load()
text_splitter = CharacterTextSplitter(separator = "\n\n", chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)



api_key_oi = st.text_input(label= "Open AI Key", value="", max_chars=None, key=None, type="default",
placeholder="Type Your Open AI API Key Here", disabled=False, label_visibility="visible")

while not api_key_oi:
    time.sleep(3)

embeddings = OpenAIEmbeddings(openai_api_key=api_key_oi)
with st.spinner('Embedding...'):
    vectorstore = Chroma.from_documents(texts, embeddings)

st.write("Embedding Completed...")

query = st.text_input(label="Provide search string..")
while not query:
    time.sleep(3)


docs = vectorstore.similarity_search_with_score(query)

st.markdown("### Result of Vector Search ")
st.write(docs)

qa = ConversationalRetrievalChain.from_llm(OpenAI(temperature=0, openai_api_key=api_key_oi),
                                           vectorstore.as_retriever(),
                                           condense_question_llm = ChatOpenAI(openai_api_key=api_key_oi, temperature=0, model='gpt-3.5-turbo'),)
chat_history = []
result = qa({"question": query, "chat_history": chat_history})



st.markdown("### Result of LLM ")
st.write(result['answer'])



st.button("Re-run")
