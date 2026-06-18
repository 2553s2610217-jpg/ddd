import streamlit as st
import datetime

# --- 페이지 설정 ---
st.set_page_config(
    page_title="스마트 보건실 똑똑이 - 고통 체크",
    page_icon="🏥",
    layout="centered"
)

st.title("🏥 나의 고통 상태 체크하기")
st.write("현재 느끼는 통증의 정도를 솔직하게 체크해 주세요.")

st.divider()

# 학년/반/이름 입력
col1, col2 = st.columns(2)
with col1:
    grade_class = st.text_input("학년 / 반 / 번호", placeholder="예: 2학년 3반 15번")
with col2:
    name = st.text_input("이름", placeholder="예: 홍길동")

st.divider()

# 통증 척도 슬라이더
st.subheader("📊 현재 얼마나 아픈가요?")
pain_level = st.slider("통증 점수 (0: 전혀 안 아픔 ~ 10: 참을 수 없이 아픔)", 0, 10, 5)

# ✨ [수정 완료] 존재하지 않는 st.critical 대신 안전한 st.error와 상태창 사용
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

# 보건실 방문증 생성 버튼
if st.button("📋 보건실 방문증 생성하기", type="primary"):
    if not name or not grade_class:
        st.error("⚠️ 학년/반/번호와 이름을 반드시 입력해 주세요!")
    else:
        st.balloons()
        st.success("✅ 방문증 생성이 완료되었습니다. 이 화면을 선생님께 보여드리세요.")
