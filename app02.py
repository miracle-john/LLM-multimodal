import streamlit as st
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.output_parsers import StrOutputParser

# 타이틀 설정
st.title("✨ 나만의 챗봇 V1.0")

# 모델 설정
llm = init_chat_model(model="gpt-4o-mini", temperature=0, max_tokens=500)

# 챗 메시지 히스토리 초기화 (st.session_state)
if "messages" not in st.session_state :
  st.session_state.messages = []

# 챗봇을 시작할 때마다 기존 쳇 메시지를 갱신
for message in st.session_state.messages :
  # role : 대상 (assistant, user), content : 실제 대화내용
  with st.chat_message(message["role"]) :
    st.markdown(message["content"]) 

# 챗봇 기능 구현
# 사용자가 메시지를 입력했다면
# := : walrus 연산자, 바다코끼리 연산자
if prompt := st.chat_input("메시지 입력") :
  # 사용자 대화 내용을 session_state에 추가
  st.session_state.messages.append({"role" : "user", 
                                    "content" : prompt})

  # 사용자 대화 내용 출력
  with st.chat_message("user", avatar="🤔") :
    st.markdown(prompt)

  # AI 응답 출력
  with st.chat_message("assistant", avatar="🤖") :
    result = llm.stream(prompt)
    response = st.write_stream(result)

  # AI 응답을 session_state에 추가
  st.session_state.messages.append({"role" : "assistant", 
                                    "content" : response})      
