import streamlit as st
from groq import Groq
from streamlit_javascript import st_javascript

# 1. 화면 기본 설정
st.set_page_config(page_title="그랜드 호텔 AI 컨시어지", page_icon="🏨")
st.title("🏨 AI 호텔 컨시어지")
st.caption("🌐 글로벌 6개국어 실시간 감지 시스템 작동 중")

# 2. 보안키 불러오기
groq_key = ""
if "GROQ_API_KEY" in st.secrets:
    groq_key = st.secrets["GROQ_API_KEY"].strip()

if not groq_key:
    st.error("🔒 Streamlit Secrets에 GROQ_API_KEY를 입력해 주세요!")
    st.stop()

# 3. 🌐 투숙객 브라우저 언어 실시간 감지 (Javascript)
user_lang = st_javascript("window.navigator.language")

# 4. 6개국어 맞춤형 첫인사(웰컴 메시지) 매핑 테이블
welcome_messages = {
    "ko": "안녕하세요! 그랜드 호텔 AI 컨시어지입니다. 조식 시간, 와이파이, 어메니티 등 필요한 사항을 편하게 말씀해 주세요.",
    "zh": "您好！我是格兰德酒店的 AI 礼宾员。如果您需要查询早餐时间、Wi-Fi 密码或申请增加房间用品，请随时告诉我。",
    "en": "Hello! Welcome to the Grand Hotel AI Concierge. Please feel free to ask about breakfast times, Wi-Fi details, or request any room amenities.",
    "lo": "ສະບາຍດີ! ຍິນດີຕ້ອນຮັບສູ່ AI Concierge ຂອງໂຮງແຮມແກຣນ. ກະລຸນາສອບຖາມຂໍ້ມູນກ່ຽວກັບເວລາອາຫານເຊົ້າ, ລະຫັດ Wi-Fi ຫຼື ຂໍອຸປະກອນຕ່າງໆໃນຫ້ອງໄດ້ເລີຍ.",
    "vi": "Xin chào! Chào mừng bạn đến với AI Concierge của Khách sạn Grand. Vui lòng hỏi về thời gian ăn sáng, mật khẩu Wi-Fi hoặc yêu cầu các vật dụng trong phòng.",
    "th": "สวัสดีครับ! ยินดีต้อนรับสู่ AI Concierge ของโรงแรมแกรนด์ ท่านสามารถสอบถามข้อมูลเกี่ยวกับเวลาอาหารเช้า, รหัส Wi-Fi หรือขออุปกรณ์ของใช้ในห้องพักได้ทันทีครับ"
}

# 브라우저 언어 코드(예: ko-KR -> ko, zh-CN -> zh) 앞 2글자 매칭
detected_lang = "en"  # 기본값 영어
if user_lang:
    try:
        lang_code = user_lang.split("-")[0].lower()
        if lang_code in welcome_messages:
            detected_lang = lang_code
    except:
        pass

# 5. 브라우저 대화 히스토리 공간 생성 (감지된 모국어로 첫인사 설정)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": welcome_messages[detected_lang]}
    ]

# 6. 화면에 과거 메시지 그리기
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 7. 사용자 채팅 입력 처리
if user_input := st.chat_input("요청 사항을 입력하세요 / Please enter your request..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    try:
        client = Groq(api_key=groq_key)

        # 🤖 6개국어 완벽 대응 지침서 주입
        system_prompt = (
            "당신은 5성급 호텔의 멀티링구얼 AI 컨시어지입니다. 고객이 질문한 언어(한국어, 중국어, 영어, 라오스어, 베트남어, 태국어)와 완전히 동일한 언어로 정중하게 답변하세요.\n\n"
            "[호텔 가이드라인 매뉴얼]\n"
            "- 한국어: 체크인 15:00 / 체크아웃 11:00, 조식 07:00~10:00 (2층 뷔페), 와이파이 ID: Grand_Guest / PW: hotel2026\n"
            "- 中文: 办理入住 15:00 / 退房 11:00, 早餐 07:00~10:00 (2楼自助餐), Wi-Fi 账号: Grand_Guest / 密码: hotel2026\n"
            "- English: Check-in 15:00 / Check-out 11:00, Breakfast 07:00~10:00 (2nd Floor), Wi-Fi ID: Grand_Guest / PW: hotel2026\n"
            "- ພາສາລາວ: ເຊັກອິນ 15:00 / ເຊັກເອົາ 11:00, ອາຫານເຊົ້າ 07:00~10:00 (ຊັ້ນ 2), Wi-Fi ID: Grand_Guest / PW: hotel2026\n"
            "- Tiếng Việt: Nhận phòng 15:00 / Trả phòng 11:00, Ăn sáng 07:00~10:00 (Tầng 2), Wi-Fi ID: Grand_Guest / PW: hotel2026\n"
            "- ภาษาไทย: เช็คอิน 15:00 / เช็คเอาท์ 11:00, อาหารเช้า 07:00~10:00 (ชั้น 2), Wi-Fi ID: Grand_Guest / PW: hotel2026\n\n"
            "물리적인 객실 물품 요구(수건 등)나 정비 요청에는 답변 가장 마지막 줄에 반드시 투숙객의 언어에 맞춰 아래 고정 접수 멘트만 출력하세요. 혼용하지 마십시오.\n"
            "- 한국어 요청 시 끝줄 고정: '[요청 접수 완료: #REC-2026] 즉시 담당 부서로 전달했습니다.'\n"
            "- 중국어 요청 시 끝줄 고정: '[请求已受理: #REC-2026] 已立即转交至相关部门处理。'\n"
            "- 영어 요청 시 끝줄 고정: '[Request Processed: #REC-2026] Transferred to the department immediately.'\n"
            "- 라오스어 요청 시 끝줄 고정: '[ການຮ້ອງຂໍໄດ້ຮັບການອະນຸມັດ: #REC-2026] ໄດ້ສົ່ງຕໍ່ໃຫ້ພະແນກທີ່ກ່ຽວຂ້ອງທັນທີ.'\n"
            "- 베트남어 요청 시 끝줄 고정: '[Yêu cầu đã được tiếp nhận: #REC-2026] Đã chuyển ngay đến bộ phận liên quan để xử lý.'\n"
            "- 태국어 요청 시 끝줄 고정: '[ดำเนินการรับเรื่องแล้ว: #REC-2026] ได้ประสานงานສົ່ງຕໍ່ໃຫ້ແຜນກທີ່ກ່ຽວຂ້ອງທັນທີครับ'"
        )

        formatted_messages = [{"role": "system", "content": system_prompt}]
        for m in st.session_state.messages:
            formatted_messages.append({"role": m["role"], "content": m["content"]})

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=formatted_messages
        )

        answer = response.choices.message.content
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.chat_message("assistant").write(answer)

    except Exception as e:
        st.error(f"⚠️ 시스템 오류 발생: {e}")
