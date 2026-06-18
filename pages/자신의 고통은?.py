import streamlit as st
import requests
import datetime

# 1. 페이지 설정
st.set_page_config(page_title="스마트 보건실 똑똑이", page_icon="🏥", layout="centered")

# CSS로 디자인 개선
st.markdown("""
    <style>
    .main { background-color: #f9fbfd; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #005088; color: white; height: 3em; font-weight: bold; }
    .pain-box { padding: 20px; border-radius: 15px; border: 1px solid #e2e8f0; background-color: white; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏥 스마트 보건실 커넥트")
st.write("보건실에 가기 전, 현재 상태를 입력하면 선생님께 즉시 전달됩니다.")

# --- 섹션 1: 학생 정보 ---
with st.container():
    st.subheader("👤 학생 정보")
    col1, col2 = st.columns(2)
    with col1:
        grade_class = st.text_input("학년/반", placeholder="예: 2학년 3반")
    with col2:
        name = st.text_input("이름", placeholder="성함을 입력하세요")

# --- 섹션 2: 통증 수치 체크 (Pain Scale) ---
st.subheader("📊 얼마나 아픈가요?")
pain_level = st.select_slider(
    "통증 척도 (0: 안 아픔 ~ 10: 매우 아픔)",
    options=list(range(11)),
    value=5
)

# 통증 수치에 따른 이모지 및 메시지
pain_emojis = ["😊", "🙂", "😐", "😟", "😣", "😫", "😩", "🥵", "🤢", "🚑", "🆘"]
st.info(f"선택한 통증 수치: **{pain_level}** {pain_emojis[pain_level]}")

# --- 섹션 3: 주관적 증상 기술 ---
st.subheader("📝 상세 증상 기술")
pain_desc = st.text_area(
    "어디가 어떻게 아픈지 보건 선생님께 자유롭게 적어주세요.",
    placeholder="예: 오늘 아침부터 머리가 띵하고 열이 나는 것 같아요. 어제 체육시간에 넘어진 발목도 조금 쑤셔요."
)

# --- 섹션 4: 전송 기능 ---
# 배포 시에는 Streamlit Secrets를 사용하여 Webhook URL을 숨기세요.
# 테스트 시 아래 변수에 본인의 Discord Webhook URL을 넣으세요.
DISCORD_WEBHOOK_URL = st.secrets.get("DISCORD_URL", "")

if st.button("🚀 보건 선생님께 전송하기"):
    if not grade_class or not name or not pain_desc:
        st.warning("정보를 모두 입력해 주세요!")
    elif not DISCORD_WEBHOOK_URL:
        st.error("보건 선생님의 수신 설정(Webhook)이 되어있지 않습니다. 관리자에게 문의하세요.")
    else:
        # 전송 데이터 구성
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        payload = {
            "embeds": [{
                "title": "🚑 보건실 방문 예정 알림",
                "color": 15158332 if pain_level > 7 else 3066993,
                "fields": [
                    {"name": "학생 정보", "value": f"{grade_class} {name}", "inline": True},
                    {"name": "통증 수치", "value": f"{pain_level}/10 {pain_emojis[pain_level]}", "inline": True},
                    {"name": "상세 증상", "value": pain_desc},
                    {"name": "전송 시간", "value": current_time}
                ]
            }]
        }

        try:
            response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
            if response.status_code == 204:
                st.success("✅ 선생님께 성공적으로 전송되었습니다! 보건실로 조심히 오세요.")
                st.balloons()
            else:
                st.error("전송에 실패했습니다. 다시 시도해 주세요.")
        except Exception as e:
            st.error(f"오류 발생: {e}")

st.caption("본 서비스는 개인정보를 서버에 저장하지 않으며, 전송 즉시 파기됩니다.")

### 🛠 배포 및 설정 가이드

1.  **GitHub에 올리기:**
    *   새 레포지토리를 생성하고 `app.py`와 `requirements.txt` 파일을 올립니다.
    *   `requirements.txt` 내용:
        ```text
        streamlit
        requests
        2.  **Discord 알림 설정:**
    *   보건 선생님의 Discord 서버에서 **채널 설정 > 연동 > 웹후크 만들기**를 통해 URL을 생성하고 복사합니다.
3.  **Streamlit Cloud Secrets 설정:**
    *   배포된 앱의 관리 페이지에서 **Settings > Secrets**로 들어갑니다.
    *   다음 내용을 입력합니다:
        ```toml
        DISCORD_URL = "복사한_웹후크_URL"
        4.  **완료:** 이제 학생들이 URL에 접속해 내용을 적으면 선생님의 Discord로 실시간 알림이 갑니다!

요청하신 보건실 앱 제안서와 코드가 마음에 드시길 바랍니다. 추가 수정이 필요하시면 언제든 말씀해 주세요!
