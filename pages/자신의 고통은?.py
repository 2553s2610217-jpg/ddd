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
    .stButton>button { width: 100%; border-radius: 10px; background-color: #10b981; color: white; }
    .report-box { padding: 20px; border-radius: 15px; border: 2px solid #34d399; background-color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 앱 로직 시작 ---
st.title("🏥 스마트 보건실 똑똑이")
st.write("보건실에 오셨나요? 선생님께 증상을 더 정확하게 알려드릴 수 있도록 아래 내용을 작성해 주세요.")

st.divider()

# 1. 기본 정보 입력
st.subheader("👤 1. 학생 정보")
col1, col2 = st.columns(2)
with col1:
    grade_class = st.text_input("학년/반 (예: 2-3)")
with col2:
    student_name = st.text_input("이름")

# 2. 고통 척도 (Pain Scale)
st.subheader("📊 2. 얼마나 아픈가요?")
pain_score = st.select_slider(
    "현재 느끼는 고통의 정도를 선택하세요 (0: 안 아픔 ~ 10: 매우 아픔)",
    options=list(range(11)),
    value=5
)

# 고통 수치에 따른 이모지 가이드
pain_emojis = ["😊", "🙂", "😐", "😟", "😣", "😫", "😩", "🥵", "🤢", "🚑", "🆘"]
st.info(f"선택한 통증 수치: **{pain_score}** {pain_emojis[pain_score]}")

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
if st.button("📋 처치 리포트 생성하기"):
    if not grade_class or not student_name or not symptoms:
        st.error("이름, 학급, 증상을 모두 입력해 주세요!")
    else:
        st.balloons()
        st.success("리포트가 생성되었습니다! 아래 화면을 보건 선생님께 보여주세요.")
        
        # 리포트 카드 디자인
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        st.markdown(f"""
            <div class="report-box">
                <h3 style="text-align: center; color: #065f46;">🚑 보건실 방문 리포트</h3>
                <p><b>일시:</b> {now}</p>
                <p><b>학생:</b> {grade_class} {student_name}</p>
                <hr>
                <p><b>통증 정도:</b> {pain_score}/10 {pain_emojis[pain_score]}</p>
                <p><b>주요 증상:</b> {", ".join(symptoms)}</p>
                <p><b>관련 계열:</b> {", ".join(detected_categories)}</p>
                <p><b>상세 내용:</b> {details}</p>
            </div>
        """, unsafe_allow_html=True)

### 💡 배포 방법 (GitHub & Streamlit Community Cloud)

1.  **GitHub 저장소 만들기:** GitHub에서 새 레포지토리를 만들고 위 소스 코드를 `app.py`로 저장하여 업로드하세요.
2.  **`requirements.txt` 파일 추가:** 저장소에 아래 내용을 포함한 `requirements.txt` 파일을 만드세요.
    ```text
    streamlit
    pandas
    3.  **Streamlit Cloud 연결:** [Streamlit Community Cloud](https://share.streamlit.io/)에 접속하여 GitHub 저장소를 연결하면 즉시 배포됩니다.

제안해 드린 보건실 앱과 발표 자료가 프로젝트에 큰 도움이 되길 바랍니다! 추가로 수정하고 싶은 기능이 있다면 말씀해 주세요.
