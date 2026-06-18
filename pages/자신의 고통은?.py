import streamlit as st
import datetime

# --- 페이지 설정 ---
st.set_page_config(
    page_title="스마트 보건실 똑똑이",
    page_icon="🏥",
    layout="centered"
)

# --- 스타일링 (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #f0fdf4; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #10b981; color: white; height: 3em; font-weight: bold; }
    .report-box { padding: 20px; border-radius: 15px; border: 2px solid #34d399; background-color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .emergency-box { padding: 20px; border-radius: 15px; border: 2px solid #ef4444; background-color: #fef2f2; color: #b91c1c; font-weight: bold; text-align: center; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏥 스마트 보건실 똑똑이")
st.write("보건실에 오셨나요? 선생님께 증상을 더 정확하게 알려드릴 수 있도록 아래 내용을 작성해 주세요.")

st.divider()

# 1. 기본 정보 입력
st.subheader("👤 1. 학생 정보")
col1, col2 = st.columns(2)
with col1:
    grade_class = st.text_input("학년/반 (예: 2-3)", key="grade_class")
with col2:
    student_name = st.text_input("이름", key="student_name")

# 2. 고통 척도 (Pain Scale)
st.subheader("📊 2. 얼마나 아픈가요?")
pain_score = st.select_slider(
    "현재 느끼는 고통의 정도를 선택하세요 (0: 안 아픔 ~ 10: 매우 아픔)",
    options=list(range(11)),
    value=5
)

# ✨ [에러 해결 포인트] 0부터 10까지 총 11개의 이모지를 정확히 매칭했습니다.
pain_emojis = ["😊", "🙂", "😐", "😟", "😣", "😫", "😩", "🥵", "🤢", "🚑", "🆘"]
current_emoji = pain_emojis[pain_score]

# 통증 수치별 안내 메시지 (10점 에러 완벽 방지)
if pain_score == 0:
    st.info(f"선택한 통증 수치: **{pain_score}** {current_emoji} (전혀 안 아파요)")
elif 1 <= pain_score <= 3:
    st.success(f"선택한 통증 수치: **{pain_score}** {current_emoji} (조금 아프지만 참을 만해요)")
elif 4 <= pain_score <= 6:
    st.warning(f"선택한 통증 수치: **{pain_score}** {current_emoji} (꽤 아파서 신경 쓰여요)")
elif 7 <= pain_score <= 9:
    st.error(f"선택한 통증 수치: **{pain_score}** {current_emoji} (너무 아파서 힘들어요)")
else:  # pain_score == 10 인 경우
    # 🚨 통증 10일 때는 시각적으로 위험을 알리는 빨간 상자 표시!
    st.markdown(f"""
        <div class="emergency-box">
            🚨 {current_emoji} 통증 수치: 10/10 (참을 수 없을 정도로 극심한 고통!) 🚨<br>
            대기하지 말고 즉시 보건 선생님께 말씀드리거나 주변에 도움을 요청하세요!
        </div>
    """, unsafe_allow_html=True)

# 3. 증상 선택 및 계열 분류
st.subheader("🔍 3. 증상 및 계열 확인")
symptoms = st.multiselect(
    "해당하는 증상을 모두 선택하세요.",
    ["두통", "복통", "인후통(목)", "기침/콧물", "발열/오한", "찰과상(까짐)", "염좌(빰)", "타박상(멍)", "어지러움", "생리통", "기타"]
)

# 계열 분류 로직
category_map = {
    "내과 계열": ["복통", "인후통(목)", "기침/콧물", "발열/오한"],
    "외과 계열": ["찰과상(까짐)", "염좌(빰)", "타박상(멍)"],
    "신경과/기타": ["두통", "어지러움", "생리통", "기타"]
}

detected_categories = set()
for s in symptoms:
    for cat, items in category_map.items():
        if s in items:
            detected_categories.add(cat)

if symptoms:
    st.write("🩺 예상되는 관련 계열:")
    for cat in detected_categories:
        st.success(f"📍 **{cat}**")
else:
    st.write("증상을 선택하면 관련 계열을 알려드립니다.")

# 4. 상세 내용 작성
st.subheader("📝 4. 상세 내용")
details = st.text_area("언제부터, 어떻게 아픈지 더 자세히 적어주세요.", placeholder="예: 2교시 체육시간 이후부터 발목이 욱신거려요.")

st.divider()

# 5. 결과 확인 및 제출 버튼
if st.button("📋 처치 리포트 생성하기", type="primary"):
    if not grade_class or not student_name or not symptoms:
        st.error("⚠️ 이름, 학급, 증상을 모두 입력해 주세요!")
    else:
        st.balloons()
        st.success("리포트가 생성되었습니다! 아래 화면을 보건 선생님께 보여주세요.")
        
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # 통증이 10점일 때는 리포트 테두리를 빨간색으로 변경하는 센스
        box_border = "#ef4444" if pain_score == 10 else "#34d399"
        
        st.
