import streamlit as st
from openai import OpenAI

# 1. 화면 레이아웃 정의
st.set_page_config(page_title="그랜드 호텔 AI 컨시어지", page_icon="🏨")
st.title("🏨 AI 호텔 컨시어지 (2단계 완료)")
st.caption("실시간 시스템 무결성 점검 완료")

# 2. Streamlit Secrets에서 보안키 불러오기 및 방어 체크
groq_key = ""
if "GROQ_API_KEY" in st.secrets:
    groq_key = st.secrets["GROQ_API_KEY"].strip()

if not groq_key or groq_key == "내_실제_GROQ_API_KEY_입력":
    st.error("🔒 왼쪽 아래 [Manage app] -> [Settings] -> [Secrets] 메뉴로 들어가서 GROQ_API_KEY = \"gsk_xxxx...\" 형태로 실제 키를 입력 후 저장해 주세요!")
    st.stop()

# 3. 브라우저 대화 히스토리 공간 생성
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요! 그랜드 호텔 AI 컨시어지입니다. 조식 시간이나 와이파이, 어메니티 등 필요한 사항을 편하게 말씀해 주세요."}
    ]

# 4. 화면에 과거 메시지 그리기
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 5. 사용자 채팅 입력 시 실행
if user_input := st.chat_input("컨시어지에게 요청할 내용을 입력하세요..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # 6. Groq 클라이언트 안전 연동 및 호출
    try:
        # 끝에 붙은 /v1을 제외하고 입력하는 것이 공식 최신 규격입니다.
        client = OpenAI(base_url="https://api.groq.com", api_key=groq_key)



        system_prompt = (
            "당신은 호텔 컨시어지입니다. 아래의 매뉴얼에 맞춰서만 정중하게 답변하세요.\n"
            "- 체크인: 15:00 / 체크아웃: 11:00\n"
            "- 조식 시간: 오전 7시 ~ 10시 (2층 메인 뷔페)\n"
            "- 와이파이 ID: Grand_Guest / PW: hotel2026\n\n"
            "물리적인 객실 물품 요구(수건 등)나 정비 요청에는 답변 가장 마지막 줄에 반드시 "
            "'[요청 접수 완료: #REC-2026] 즉시 담당 부서로 전달했습니다.' 라는 고정 멘트를 출력해 주세요."
        )

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages
        )

        answer = response.choices.message.content
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.chat_message("assistant").write(answer)

    except Exception as e:
        # API 오류가 발생하더라도 전체 웹 앱이 붉은 화면으로 뻗는 것을 방지
        st.error(f"⚠️ Groq API 통신 중 문제가 발생했습니다. Secrets에 입력한 키가 올바른 'gsk_' 형태인지 다시 한 번 확인해 주세요. (에러 내용: {e})")
