import streamlit as st
import datetime

# --- 페이지 설정 ---
st.set_page_config(
    page_title="스마트 보건실 똑똑이",
    page_icon="🏥",
    layout="centered"
)

# --- 앱 제목 및 소개 ---
st.title("🏥 스마트 보건실 방문 미리보기")
st.write("보건실에 가기 전, 현재 자신의 상태와 아픈 곳을 미리 체크해 보세요. 보건 선생님께 더 정확하게 증상을 말씀드릴 수 있어요!")

st.divider()

# --- 1. 기본 정보 입력 ---
st.header("👤 1. 기본 정보 입력")
col1, col2 = st.columns(2)
with col1:
    grade_class = st.text_input("학년 / 반 / 번호", placeholder="예: 2학년 3반 15번")
with col2:
    name = st.text_input("이름", placeholder="예: 홍길동")

# --- 2. 주요 증상 및 부위 선택 ---
st.header("🔍 2. 어디가 아픈가요?")
symptoms = st.multiselect(
    "증상을 모두 선택해 주세요 (중복 선택 가능)",
    ["두통 (머리 아픔)", "복통 (배 아픔)", "치통 (이 아픔)", "인후통 (목 따가움)", 
     "기침/콧물", "발열/오한", "찰과상 (까짐/상처)", "타박상 (부딪힘/멍)", "근육통/염좌", "생리통", "기타"]
)

if "기타" in symptoms:
    other_symptom = st.text_input("기타 증상을 직접 적어주세요:")

# --- 3. 통증 척도 (Pain Scale) 체크 ---
st.header("📊 3. 얼마나 아픈가요? (통증 척도)")
st.write("현재 느끼는 고통의 정도를 숫자로 선택해 주세요.")

# FPS (Faces Pain Scale) 느낌의 설명 추가
pain_level = st.slider("통증 점수 (0: 전혀 안 아픔 ~ 10: 참을 수 없이 아픔)", 0, 10, 5)

# 통증 점수에 따른 가이드 메시지
if pain_level == 0:
    st.info("😊 전혀 아프지 않아요. (안심 상태)")
elif 1 <= pain_level <= 3:
    st.success("🙂 조금 아프지만 견딜 만해요. (경증)")
elif 4 <= pain_level <= 6:
    st.warning("😐 많이 아프고 신경 쓰여요. (중등도)")
elif 7 <= pain_level <= 9:
    st.error("😰 너무 아파서 눈물이 나거나 힘들어요. (중증)")
else:
    st.critical("😭 참을 수 없을 정도로 극심한 통증이에요! (즉시 조치 필요)")

# --- 4. 추가 전달 사항 ---
st.header("📝 4. 보건 선생님께 하고 싶은 말")
details = st.text_area("언제부터 아팠는지, 또는 복용 중인 약이 있다면 적어주세요.", placeholder="예: 2교시 체육 시간 이후부터 발목이 삐끗해서 계속 시려요.")

st.divider()

# --- 5. 접수 및 확인 ---
if st.button("📋 보건실 방문증 생성하기", type="primary"):
    if not name or not grade_class:
        st.error("⚠️ 학년/반/번호와 이름을 반드시 입력해 주세요!")
    elif not symptoms:
        st.error("⚠️ 아픈 증상을 최소 하나 이상 선택해 주세요!")
    else:
        st.balloons()
        st.success("✅ 방문증이 성공적으로 생성되었습니다! 아래 내용을 보건 선생님께 보여드리거나 캡처하세요.")
        
        # 결과 리포트 서식
        st.subheader("📝 보건실 방문 접수증")
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        report_box = f"""
        **[방문 일시]** {now}  
        **[학생 정보]** {grade_class} {name}  
        **[주요 증상]** {', '.join(symptoms)}  
        **[통증 척도]** {pain_level} / 10  
        **[상세 내용]** {details if details else '없음'}
        """
        st.info(report_box)
        
        st.caption("💡 팁: 이 화면을 캡처해서 보건실에 방문하면 선생님이 빠르게 확인하실 수 있어요!")
