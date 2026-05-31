import streamlit as st
from openai import OpenAI

# 1. 브라우저 화면 레이아웃 및 타이틀 세팅
st.set_page_config(page_title="그랜드 호텔 AI 컨시어지", page_icon="🏨")
st.title("🏨 AI 호텔 컨시어지 (2단계)")
st.caption("온라인 무료 API 기반 실시간 프로토타입 서비스")

# 2. 사이드바에 무료 API 키 입력창 생성 (보안 및 편의성 확보)
with st.sidebar:
    st.header("🔑 시스템 설정")
    groq_key = st.text_input("Groq API Key를 입력하세요", type="password")
    st.info("API Key는 ://groq.com에서 무료로 발급받을 수 있습니다.")

# 3. 채팅 세션 데이터베이스 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요! 그랜드 호텔 AI 컨시어지입니다. 조식 시간이나 어메니티 요청 등 필요한 사항을 말씀해 주세요."}
    ]

# 4. 화면에 대화 기록 출력
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 5. 고객 메시지 입력 시 동작 처리
if user_input := st.chat_input("컨시어지에게 요청할 내용을 입력하세요..."):
    if not groq_key:
        st.warning("왼쪽 사이드바에 Groq API Key를 먼저 입력해 주세요!")
        st.stop()

    # 화면에 고객 입력 추가
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # 무료 오픈소스 모델 연결용 클라이언트 설정
    client = OpenAI(base_url="https://groq.com", api_key=groq_key)

    # 핵심 컨시어지 지침서 주입
    system_prompt = (
        "당신은 호텔 컨시어지입니다. 아래 호텔 가이드를 기반으로 답변하세요.\n"
        "- 체크인: 15:00 / 체크아웃: 11:00\n"
        "- 조식 시간: 오전 7시 ~ 10시 (2층 메인 뷔페)\n"
        "- 와이파이 ID: Grand_Guest / PW: hotel2026\n\n"
        "만약 수건 추가, 청소 요청 등 직원이 움직여야 하는 '물리적 요청'이 들어오면 "
        "반드시 대답 끝에 '[요청 접수 번호: #REC-001] 담당 부서로 접수를 완료했습니다.'라는 문구를 포함하세요."
    )

    # 초고속 무료 추론 엔진 호출
    response = client.chat.completions.create(
        model="llama3-8b-8192", # 무료 티어 중 가장 빠르고 성능이 좋은 모델
        messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages
    )

    answer = response.choices.message.content

    # 화면에 AI 답변 추가
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer)
