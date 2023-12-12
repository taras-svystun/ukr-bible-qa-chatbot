import os
import sys
import streamlit as st
import openai
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.memory import ConversationSummaryMemory
from langchain.vectorstores import FAISS


openai.api_key = os.environ["OPENAI_API_KEY"] or st.secrets.openai_key
FIRST_AI_MESSAGE = 'Спитайся мене що завгодно по Біблії'


st.set_page_config(
    page_title="Питання по Біблії",
    page_icon="🤲",
    layout='centered',
    initial_sidebar_state="auto",
    menu_items=None)


if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": FIRST_AI_MESSAGE}
    ]


def clear_chat_history():
    st.session_state.messages = [
        {"role": "assistant", "content": FIRST_AI_MESSAGE}
    ]


with st.sidebar:
    st.info('Це чатбот, який має доступ до всього тексту Біблії та може відповідати на запитання.', icon="ℹ️")
    st.write("Цю демку створив [Тарас Свистун](https://github.com/taras-svystun).")
    st.write('Поглянути на код застосунку можна [тут](https://github.com/taras-svystun/ukr-bible-qa-chatbot).')
    st.write("Текст Біблії в українському перекладі було взято [звідси](https://www.jw.org/uk/бібліотека/біблія/nwt/книги/).")
    st.button(":red[Стерти історію чату]", on_click=clear_chat_history)


st.title("Відповіді на питання по Біблії👼")


@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading..."):
        loader = TextLoader("bible.txt")
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1150, chunk_overlap=150, length_function = len,
                                                       separators=[" ", ",", "\n"]
                                                       )
        text_chunks = text_splitter.split_documents(documents)
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_documents(text_chunks, embeddings)
        return vectorstore.as_retriever()
        

retriever = load_data()


if "chat_engine" not in st.session_state.keys():
    llm = ChatOpenAI(temperature=.2)
    memory = ConversationSummaryMemory(
        llm=llm, memory_key="chat_history", return_messages=True
    )
    qa = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory)
    st.session_state['chat_engine'] = qa


if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Дай подумаю...🤔"):
            response = st.session_state.chat_engine(prompt)
            st.write(response['answer'])
            message = {"role": "assistant", "content": response['answer']}
            st.session_state.messages.append(message)