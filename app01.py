import streamlit as st

# chat_input() : 챗팅 입력 컴포넌트
prompt = st.chat_input("대화 입력")

# AI 채팅 메시지
with st.chat_message("assistant", avatar="🤖") :
  # write() : 화면 해당 내용을 출력
  st.write("안녕하세요 AI 챗봇입니다")

# 대화 내용을 입력했다면
if prompt :   
  with st.chat_message("user", avatar="😍") :
    st.write(prompt)
