import streamlit as st
from streamlit_chat import message

from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.schema import HumanMessage
from langchain.schema import AIMessage
from langchain.llms import OpenAI
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType

from dotenv import load_dotenv
# 環境変数の読み込み
load_dotenv()

import os
OPENAI_API_TYPE = os.getenv("OPENAI_API_TYPE")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
OPENAI_API_MODEL = os.getenv("OPENAI_API_MODEL")
OPENAI_API_MODEL_DEPROY = os.getenv("OPENAI_API_MODEL_DEPROY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ChatGPT-3.5のモデルのインスタンスの作成
llm = ChatOpenAI(model_name=OPENAI_API_MODEL, model_kwargs={"deployment_id":OPENAI_API_MODEL_DEPROY})

tool_names = ["google-search"]
tools = load_tools(tool_names, llm=llm)   

# セッション内に保存されたチャット履歴のメモリの取得
try:
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
    )
except:
    memory = ConversationBufferMemory(return_messages=True)
    
# チャット用のチェーンのインスタンスの作成
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

# Streamlitによって、タイトル部分のUIをの作成
st.title("Chatbot in Streamlit")
st.caption("testのチャットです")

# 入力フォームと送信ボタンのUIの作成
text_input = st.text_input("Enter your message")
send_button = st.button("Send")

text_input = "Informaticaについて教えてください"

# チャット履歴（HumanMessageやAIMessageなど）を格納する配列の初期化
history = []

# ボタンが押された時、OpenAIのAPIを実行
if send_button:
    send_button = False

    # ChatGPTの実行
    agent.run(text_input)

    # セッションへのチャット履歴の保存
    st.session_state["memory"] = memory

    # チャット履歴（HumanMessageやAIMessageなど）の読み込み
    try:
        history = memory.load_memory_variables({})["history"]
    except Exception as e:
        st.error(e)

# チャット履歴の表示
for index, chat_message in enumerate(reversed(history)):
    if type(chat_message) == HumanMessage:
        message(chat_message.content, is_user=True, key=2 * index)
    elif type(chat_message) == AIMessage:
        message(chat_message.content, is_user=False, key=2 * index + 1)