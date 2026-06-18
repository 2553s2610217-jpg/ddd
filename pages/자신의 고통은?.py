import streamlit as st
import datetime

# --- 페이지 설정 ---
st.set_page_config(
    page_title="스마트 보건실 똑똑이 - 고통 체크",
    page_icon="🏥",
    layout="centered"
)

st.title("🏥 나의 고통 상태 체크하기")
st.write("현재 느끼는 통증과 증상을 체크해 주세요. 어떤 계열의 통증인지 함께 안내해 드립니다.")

st.divider()

# 1. 기본 정보 입력
col1, col2 = st.columns(2)
with col1:
    grade_class = st.text_input("학년 / 반 / 번호", placeholder="예: 2학년 3반 15번")
with col2:
    name = st.text_input("이름", placeholder="예: 홍길동")

st.divider()

# 2. 통증 척도 슬라이더
st.subheader("📊 현재 얼마나 아픈가요?")
pain_level = st.slider("통증 점수 (0: 전혀 안 아픔 ~ 10: 참을 수 없이 아픔)", 0, 10, 5)

# 통증 수치별 안전한 가이드 (st.critical 에러 완벽 해결!)
if pain_level == 0:
    st.info("😊 전혀 아프지 않아요. (안심 상태)")
elif 1 <= pain_level <= 3:
    st.success("🙂 조금 아프지만 견딜 만해요. (경증)")
elif 4 <= pain_level <= 6:
    st.warning("😐 많이 아프고 신경 쓰여요. (중등도)")
elif 7 <= pain_level <= 9:
    st.error("😰 너무 아파서 눈물이 나거나 힘들어요. (중증)")
else: # 10점일 때
    st.error("😭 참을 수 없을 정도로 극심한 통증이에요! 대기하지 말고 즉시 보건 선생님께 말씀드리세요! (즉시 조치 필요)")

st.divider()

# 3. ✨ [신규 기능] 증상 체크를 통한 대략적인 계열 분류
st.subheader("🔍 현재 겪고 있는 증상을 모두 골라주세요")
st.write("선택하신 증상을 바탕으로 대략적인 진료 계열을 안내해 드립니다.")

# 학생들이 자주 겪는 증상 리스트
selected_symptoms = st.multiselect(
    "증상 선택 (여러 개 선택 가능)",
    [
        "소화불량/속쓰림", "복통(배 아픔)", "설사/구토", "기침/콧물/가래", "발열/오한/인후통",  # 내과
        "찰과상(피부 까짐)", "타박상(부딪혀서 멍듦)", "발목/손목 윔(염좌)", "베인 상처/피가 남", # 외과
        "두통(머리 아픔)", "어지러움", "생리통", "눈/귀/치아 통증" # 신경과 및 기타
    ]
)

# 증상 분석 로직
detected_categories = []

# 내과 조건
if any(s in selected_symptoms for s in ["소화불량/속쓰림", "복통(배 아픔)", "설사/구토", "기침/콧물/가래", "발열/오한/인후통"]):
    detected_categories.append("🩺 **내과 계열 질환** (감기, 위염, 장염 등)")

# 외과 조건
if any(s in selected_symptoms for s in ["찰과상(피부 까짐)", "타박상(부딪혀서 멍듦)", "발목/손목 윔(염좌)", "베인 상처/피가 남"]):
    detected_categories.append("🩹 **외과/정형외과 계열 상처** (외상, 염좌 등)")

# 신경과 및 기타 조건
if any(s in selected_symptoms for s in ["두통(머리 아픔)", "어지러움", "생리통", "눈/귀/치아 통증"]):
    detected_categories.append("🧠 **신경과 / 이비인후과 / 기타 통증**")

# 분석 결과 실시간으로 보여주기
if selected_symptoms:
    st.markdown("### 🩺 증상 분석 결과")
    st.write("현재 증상은 대략 아래 계열에 해당할 수 있어요:")
    for category in detected_categories:
        st.info(category)
else:
    st.caption("💡 증상을 선택하시면 대략 어느 계열인지 여기에 나타납니다.")

st.divider()

# 4. 보건실 방문증 생성 버튼
if st.button("📋 보건실 방문증 생성하기", type="primary"):
    if not name or not grade_class:
        st.error("⚠️ 학년/반/번호와 이름을 반드시 입력해 주세요!")
    elif not selected_symptoms:
        st.error("⚠️ 현재 겪고 있는 증상을 하나 이상 선택해 주세요!")
    else:
        st.balloons()
        st.success("✅ 방문증 생성이 완료되었습니다. 이 화면을 보건 선생님께 보여드리세요.")
        
        # 보건쌤 전용 요약 리포트
        st.markdown("### 📝 최종 접수 내용")
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        report = f"""
        * **방문 일시:** {now}
        * **학생 정보:** {grade_class} {name}
        * **통증 척도:** {pain_level} / 10
        * **선택한 증상:** {', '.join(selected_symptoms)}
        """
        st.code(report, language="markdown")
