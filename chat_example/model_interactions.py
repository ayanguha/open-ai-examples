from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.document_loaders import CSVLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI

from datasets import load_dataset


class EmbeddingFactory:
    def __init__(self, api_key, embedding_provider='OpenAI', sample_size = 100):
        self.embedding_provider = embedding_provider
        self.sample_size = sample_size
        self.api_key = api_key
        if self.embedding_provider == 'OpenAI':
            self.embeddings = OpenAIEmbeddings(openai_api_key=api_key)

    def load_vectorstore(self):
        data = load_dataset('squad', split='train')
        data = data.to_pandas()
        data.drop_duplicates(subset='context', keep='first', inplace=True)
        data = data.to_dict('records')[:self.sample_size] ## Sample
        metadatas = [ {'title': record['title']} for record in data]
        texts =  [ record['context'] for record in data]
        self.vectorstore = Chroma(embedding_function = self.embeddings)
        vectors = self.vectorstore.add_texts(texts = texts, metadatas = metadatas)

    def get_relevant_docs(self, query):
        docs = self.vectorstore.similarity_search_with_score(query)
        return docs

    def build_chain(self):
        if self.embedding_provider == 'OpenAI':
            self.chain = ConversationalRetrievalChain.from_llm(OpenAI(temperature=0,
                                                   openai_api_key=self.api_key),
                                                   self.vectorstore.as_retriever(),
                                                   condense_question_llm = ChatOpenAI(openai_api_key=self.api_key, temperature=0, model='gpt-3.5-turbo'),)
    def chat_response(self, query, chat_history = []):
        result = self.chain({"question": query, "chat_history": chat_history})
        return result['answer']
