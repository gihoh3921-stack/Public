import streamlit as st
from openai import OpenAI

# 1. 화면 설정
st.set_page_config(page_title="그랜드 호텔 AI 컨시어지", page_icon="🏨")
st.title("🏨 AI 호텔 컨시어지 (2단계 완료)")
st.caption("온라인 무료 환경 세팅 완료 버전")

# 2. Streamlit Secrets 금고에서 안전하게 키 가져오기
try:
    groq_key = st.secrets["GROQ_API_KEY"]
except:
    st.error("오류: Streamlit 클라우드 설정(Secrets)에 GROQ_API_KEY를 등록해 주세요!")
    st.stop()

# 3. 대화 세션 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요! 그랜드 호텔 AI 컨시어지입니다. 무엇을 도와드릴까요?"}
    ]

# 4. 이전 대화 출력
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 5. 고객 메시지 처리
if user_input := st.chat_input("컨시어지에게 요청할 내용을 입력하세요..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # API 클라이언트 자동 연결
    client = OpenAI(base_url="https://groq.com", api_key=groq_key)

    system_prompt = (
        "당신은 호텔 컨시어지입니다. 아래 가이드를 기반으로 답변하세요.\n"
        "- 체크인: 15:00 / 체크아웃: 11:00\n"
        "- 조식 시간: 오전 7시 ~ 10시 (2층 메인 뷔페)\n"
        "- 와이파이 ID: Grand_Guest / PW: hotel2026\n\n"
        "물리적 요청(수건 등)에는 반드시 '[요청 접수 번호: #REC-001] 담당 부서로 전달했습니다.'를 포함하세요."
    )

    # 최신 고성능 무료 모델 호출
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages
    )

    answer = response.choices.message.content
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer)
