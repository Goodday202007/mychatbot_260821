import streamlit as st
from openai import OpenAI

# 제목과 설명 표시
st.set_page_config(page_title="바이브코딩 챗봇", page_icon="✨")
st.title("✨ 바이브코딩 챗봇")
st.write(
    "이 챗봇은 **바이브코딩(Vibe Coding)** 하는 법을 알려주는 AI 튜터입니다. "
    "바이브코딩이란 AI에게 자연어로 원하는 걸 설명하면서 함께 코드를 만들어가는 개발 방식을 말해요. "
    "궁금한 점을 편하게 물어보세요! "
    "사용하려면 OpenAI API 키가 필요합니다. [여기](https://platform.openai.com/account/api-keys)서 발급받을 수 있어요."
)

# 바이브코딩 튜터 역할을 정의하는 시스템 프롬프트
SYSTEM_PROMPT = """당신은 '바이브코딩(Vibe Coding)'을 가르치는 친절하고 실용적인 AI 튜터입니다.

바이브코딩이란 개발자가 코드를 한 줄씩 직접 짜기보다, AI(예: Claude, ChatGPT, Cursor 등)와 자연어로 대화하며
아이디어를 빠르게 프로토타입으로 만들어내는 개발 방식입니다. 핵심 철학은 다음과 같습니다:

1. 완벽한 계획보다 빠른 시도와 반복(iteration)을 중시한다.
2. AI에게 원하는 결과물의 '느낌(vibe)'과 목적을 구체적으로 설명한다.
3. 작은 단위로 나눠서 요청하고, 결과를 확인하며 다음 방향을 정한다.
4. 에러가 나면 에러 메시지를 그대로 AI에게 보여주고 해결을 맡긴다.
5. 코드의 세부 문법보다 '무엇을 만들고 싶은지'에 집중한다.
6. Cursor, Claude Code, v0, Replit Agent 같은 도구들을 상황에 맞게 활용한다.

사용자의 질문 수준에 맞춰 쉽고 구체적으로 답변하고, 필요하면 실제 프롬프트 예시나 단계별 가이드를 제시해주세요.
초보자에게는 용어를 풀어서 설명하고, 실습 위주로 안내해주세요."""

# OpenAI API 키 입력받기
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("계속하려면 OpenAI API 키를 입력해주세요.", icon="🗝️")
else:

    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=openai_api_key)

    # 채팅 메시지를 저장할 세션 상태 변수 생성 (새로고침해도 유지됨)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 기존 채팅 메시지 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 채팅 입력창 (화면 하단에 자동으로 표시됨)
    if prompt := st.chat_input("바이브코딩에 대해 무엇이든 물어보세요!"):

        # 사용자 메시지 저장 및 표시
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 시스템 프롬프트 + 대화 기록을 합쳐서 API에 전달
        api_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]

        # OpenAI API로 응답 생성
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=api_messages,
            stream=True,
        )

        # 응답을 스트리밍으로 표시하고 세션 상태에 저장
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
