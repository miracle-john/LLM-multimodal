import streamlit as st
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.output_parsers import StrOutputParser

# 메모리 관련 라이브리리
from uuid import uuid4
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# 타이틀 설정
st.title("✨ 나만의 챗봇 V1.1")

# 메모리 설정
if "storage" not in st.session_state:
  st.session_state.storage = {}

# 메모리 검색 함수
def get_session_history(session_id:str) -> ChatMessageHistory :
  if session_id not in st.session_state.storage :
    st.session_state.storage[session_id] = ChatMessageHistory()

  return st.session_state.storage[session_id]

# 모델 설정
llm = init_chat_model(model="gpt-4o-mini", temperature=0, max_tokens=500)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "너는 대화용 어시스턴트이다. 대화 맥락을 확인해서 응답을 해줘"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ]
)

chain = prompt | llm 

memory_chain = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history"
)

# 챗 메시지 히스토리 초기화 (st.session_state)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 챗봇을 시작할 때마다 기존 쳇 메시지를 갱신
for message in st.session_state.messages :
  # role : 대상 (assistant, user), content : 실제 대화내용
  with st.chat_message(message["role"]) :
    st.markdown(message["content"]) 

# 챗봇 내용을 저장하기 위한 session_id 생성
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid4())

session_id = st.session_state.session_id  

# 챗봇 기능 구현
# 사용자가 메시지를 입력했다면
# := : walrus 연산자, 바다코끼리 연산자
if user_input := st.chat_input("메시지 입력") :
  # 사용자 대화 내용을 session_state에 추가 (화면 출력용)
  st.session_state.messages.append({"role" : "user", 
                                    "content" : user_input})

  # 사용자 대화 내용 출력
  with st.chat_message("user", avatar="🤔") :
    st.markdown(user_input)

  # AI 응답을 메모리에 등록하고 출력
  with st.chat_message("assistant", avatar="🤖") :
    response = memory_chain.stream({"input": user_input},
                                    config = {"configurable":{"session_id" : session_id}})
    
    final_response = st.write_stream(response)

  # AI 응답을 session_state에 추가 (화면 출력용)
  st.session_state.messages.append({"role" : "assistant", 
                                    "content" : final_response})      
