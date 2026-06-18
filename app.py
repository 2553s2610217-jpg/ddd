import streamlit as st
import requests
from streamlit_lottie import st_lottie
import google.generativeai as genai
import datetime

# 1. 페이지 설정
st.set_page_config(
    page_title="Smart Health Hub",
    page_icon="🩺",
    layout="wide"
)

# 2. AI 설정 (Gemini)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.0-flash-lite')
else:
    st.warning("Secrets에 GEMINI_API_KEY가 설정되지 않아 AI 기능을 사용할 수 없습니다.")

# 3. 애니메이션 로드 함수
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_status != 200:
        return None
    return r.json()

# 애니메이션 URL (의료/건강 관련)
lottie_health = "https://assets5.lottiefiles.com/packages/lf20_5njp3vnu.json"

# 4. 커스텀 CSS (메인 페이지를 더욱 메인 페이지답게)
st.markdown("""
    <style>
    /* 메인 타이틀 폰트 및 애니메이션 */
    .hero-text {
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        color: #00b894;
        text-align: center;
        margin-bottom: 0px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-text {
        font-size: 1.5rem !important;
        text-align: center;
        color: #636e72;
        margin-bottom: 30px;
    }
    /* 카드 디자인 */
    .stCard {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #f1f2f6;
        transition: transform 0.3s;
    }
    .stCard:hover {
        transform: translateY(-5px);
    }
    </style>
""", unsafe_allow_html=True)

# --- 메인 화면 시작 ---

# 5. 헤더 섹션 (움직이는 그래픽 + 타이틀)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Lottie 애니메이션 표시
    lottie_json = requests.get("https://lottie.host/50534246-86d3-4811-9a7d-5a82200ec09f/zC69uVnZ7F.json").json()
    st_lottie(lottie_json, height=250, key="main_ani")
    st.markdown("<p class='hero-text'>SMART HEALTH HUB</p>", unsafe_allow_html=True)
    st.markdown("<p class='sub-text'>당신의 건강을 위한 가장 빠른 연결</p>", unsafe_allow_html=True)

st.divider()

# 6. 메인 기능 선택 (탭 메뉴)
tab_main, tab_ai, tab_info = st.tabs(["🏠 메인 가이드", "🤖 AI 증상 상담", "📋 방문 기록 안내"])

with tab_main:
    st.markdown("### 🏥 보건실 이용 방법")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("""<div class='stCard'>
        <h4>1. 방문 전 체크</h4>
        <p>심한 출혈이나 통증 시 주변 친구나 선생님께 즉시 알리고 동행하세요.</p>
        </div>""", unsafe_allow_html=True)
    
    with c2:
        st.markdown("""<div class='stCard'>
        <h4>2. 방문 및 등록</h4>
        <p>보건실 입구의 태블릿이나 대장을 통해 방문 기록을 작성합니다.</p>
        </div>""", unsafe_allow_html=True)
        
    with c3:
        st.markdown("""<div class='stCard'>
        <h4>3. 안정 및 처치</h4>
        <p>선생님의 안내에 따라 처치를 받고, 필요시 침상 안정을 취합니다.</p>
        </div>""", unsafe_allow_html=True)

    st.info("💡 점심시간은 긴급 환자 위주로 운영되오니 가급적 쉬는시간을 이용해 주세요.")

with tab_ai:
    st.markdown("### 🤖 AI 건강 상담소 (Nurse Bot)")
    st.caption("※ 본 상담은 참고용이며 반드시 전문가의 진료를 받아야 합니다.")
    
    user_input = st.text_input("현재 어디가 어떻게 아프신가요?", placeholder="예: 아침부터 머리가 지끈거리고 열이 나는 것 같아요.")
    
    if st.button("AI 상담 시작"):
        if user_input:
            try:
                with st.spinner("상담 내용을 분석 중입니다..."):
                    prompt = f"너는 학교 보건실의 친절한 보건 선생님이야. 학생이 다음과 같은 증상을 호소해: '{user_input}'. 보건실에 와서 해야 할 행동과 간단한 대처법을 3문장 이내로 다정하게 알려줘."
                    response = model.generate_content(prompt)
                    st.write("---")
                    st.subheader("👩‍⚕️ 보건 선생님의 조언")
                    st.write(response.text)
            except Exception as e:
                st.error(f"상담 중 오류가 발생했습니다: {e}")
        else:
            st.warning("증상을 입력해 주세요.")

with tab_info:
    st.markdown("### 📋 보건실 기타 정보")
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.success("🕒 **운영 시간**\n- 평일: 08:30 ~ 16:30\n- 점심시간: 12:30 ~ 13:30")
    
    with col_right
