import streamlit as st
import requests
import datetime

# --- 페이지 설정 ---
st.set_page_config(
    page_title="스마트 보건실 똑똑이",
    page_icon="🏥",
    layout="centered"
)

# --- 앱 제목 및 소개 ---
st.title("🏥 스마트 보건실 방문 미리보기")
st.write("보건실에 가기 전, 현재 자신의 상태와 아픈 곳을 미리 체크해 보세요. 완료 시 보건 선생님께 즉시 전송됩니다.")

st.divider()

# --- 1. 기본 정보 입력 ---
st.header("👤 1. 기본 정보 입력")
col1, col2 = st.columns(2)
with col1:
    grade_class = st.text_input("학년 / 반 / 번호", placeholder="예: 2학년 3반 15번")
with col2:
    name = st.text_input("이름", placeholder="예: 홍길동")

# --- 2. 통증 척도 (Pain Scale) 체크 ---
st.header("📊 2. 얼마나 아픈가요? (통증 척도)")
st.write("현재 느끼는 고통의 정도를 슬라이더로 선택하고, 아픈 느낌을 직접 적어주세요.")

# 시각적 통증 척도
pain_level = st.slider("통증 점수 (0: 전혀 안 아픔 ~ 10: 참을 수 없이 아픔)", 0, 10, 5)

# 통증 점수에 따른 가이드 메시지 및 이모지
pain_emojis = ["😊", "🙂", "😐", "😟", "😣", "😫", "😩", "🥵", "🤢", "🚑", "🆘"]
if pain_level == 0:
    st.info(f"{pain_emojis[0]} 전혀 아프지 않아요. (안심 상태)")
elif 1 <= pain_level <= 3:
    st.success(f"{pain_emojis[pain_level]} 조금 아프지만 견딜 만해요. (경증)")
elif 4 <= pain_level <= 6:
    st.warning(f"{pain_emojis[pain_level]} 많이 아프고 신경 쓰여요. (중등도)")
elif 7 <= pain_level <= 9:
    st.error(f"{pain_emojis[pain_level]} 너무 아파서 눈물이 나거나 힘들어요. (중증)")
else:
    st.critical(f"{pain_emojis[10]} 참을 수 없을 정도로 극심한 통증이에요! (즉시 조치 필요)")

# --- 3. 주관적 고통 직접 기술 ---
# 사용자가 직접 고통을 적을 수 있는 공간
user_pain_text = st.text_area(
    "어디가 어떻게 아픈지 구체적으로 적어주세요 (자유 기술)", 
    placeholder="예: 2교시 체육 시간 이후부터 오른쪽 발목이 삐끗해서 시큰거리고 걷기 힘들어요. 욱신욱신 쑤시는 느낌입니다."
)

st.divider()

# --- 4. 보건 선생님께 즉시 전송 ---
if st.button("📋 작성 완료 및 보건실 전송하기", type="primary"):
    if not name or not grade_class:
        st.error("⚠️ 학년/반/번호와 이름을 반드시 입력해 주세요!")
    elif not user_pain_text:
        st.error("⚠️ 고통이나 증상이 어떤지 최소한의 설명을 적어주세요!")
    else:
        # 현재 시간 생성
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # 1. 화면에 접수증 출력 (백업용)
        st.balloons()
        st.success("✅ 완료! 아래 내용이 보건 선생님께 전송되었습니다.")
        
        st.subheader("📝 보건실 방문 접수증 (확인용)")
        report_box = f"""
        **[방문 일시]** {now}  
        **[학생 정보]** {grade_class} {name}  
        **[통증 척도]** {pain_level} / 10 {pain_emojis[pain_level]}  
        **[상세 고통 내용]** {user_pain_text}
        """
        st.info(report_box)

        # 2. 보건쌤 메신저(디스코드)로 실시간 전송
        # Streamlit Secrets에 저장된 웹후크 URL을 안전하게 가져옵니다. (없으면 None 반환)
        DISCORD_WEBHOOK_URL = st.secrets.get("DISCORD_URL", None)
        
        if DISCORD_WEBHOOK_URL:
            # 디스코드로 보낼 예쁜 카드(Embed) 형태의 데이터
            payload = {
                "embeds": [{
                    "title": "🚑 [보건실 신규 접수] 학생이 아파요!",
                    "color": 15158332 if pain_level >= 7 else 3066993, # 아픈 정도에 따라 빨간색/초록색 변경
                    "fields": [
                        {"name": "👤 학생 정보", "value": f"{grade_class} {name}", "inline": True},
                        {"name": "📊 통증 수치", "value": f"{pain_level} / 10", "inline": True},
                        {"name": "📝 고통 내용", "value": user_pain_text, "inline": False},
                        {"name": "⏰ 접수 시간", "value": now, "inline": False}
                    ]
                }]
            }
            
            try:
                response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
                if response.status_code == 204:
                    st.toast("보건 선생님 디스코드 알림 전
