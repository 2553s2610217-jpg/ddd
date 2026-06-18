import streamlit as st
import requests
from streamlit_lottie import st_lottie
import datetime

# 1. 페이지 설정 (반드시 가장 최상단에 위치)
st.set_page_config(
    page_title="Smart Health Hub",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. 메인 페이지 전용 커스텀 CSS 스타일 정의
st.markdown("""
    <style>
    /* 메인 타이틀 스타일 */
    .hero-title {
        font-size: 3.8rem !important;
        font-weight: 900 !important;
        color: #00b894;
        text-align: center;
        margin-bottom: 5px;
        letter-spacing: -1px;
    }
    .hero-subtitle {
        font-size: 1.4rem !important;
        text-align: center;
        color: #636e72;
        margin-bottom: 35px;
    }
    /* 카드형 UI 디자인 */
    .feature-card {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        border: 1px solid #e1e8ed;
        margin-bottom: 20px;
        text-align: center;
    }
    .feature-card h4 {
        color: #2d3436;
        margin-bottom: 12px;
        font-weight: 700;
    }
    .feature-card p {
        color: #636e72;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Lottie 애니메이션 로드 함수
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# --- [비주얼 레이아웃 시작] ---

# 4. 최상단 히어로 섹션 (움직이는 아이콘 + 타이틀)
col_left, col_center, col_right = st.columns([1, 2, 1])
with col_center:
    # 헬스케어 관련 공식 움직이는 Lottie 그래픽
    lottie_json = load_lottieurl("https://lottie.host/50534246-86d3-4811-9a7d-5a82200ec09f/zC69uVnZ7F.json")
    if lottie_json:
        st_lottie(lottie_json, height=220, key="health_animation")
        
    st.markdown("<h1 class='hero-title'>🏥 SMART HEALTH HUB</h1>", unsafe_allow_html=True)
    st.markdown("<p class='hero-subtitle'>교내 보건실 이용 및 디지털 종합 안내 시스템</p>", unsafe_allow_html=True)

st.divider()

# 5. 실시간 보건실 상황판 (메인 페이지 핵심 기능)
st.markdown("### 🕒 실시간 보건실 현황")
status_col1, status_col2 = st.columns(2)

with status_col1:
    now = datetime.datetime.now().time()
    # 평일 09:00 ~ 17:00 기준 운영 여부 체크
    if datetime.time(9, 0) <= now <= datetime.time(17, 0):
        st.success("🟢 **현재 보건실 정상 운영 중** (지금 방문하시면 처치를 받을 수 있습니다)")
    else:
        st.warning("🟡 **현재 보건실 운영 시간 종료** (응급 상황 시 교무실이나 119로 연락하세요)")

with status_col2:
    st.info("⏰ **이용 시간 안내** : 평일 09:00 ~ 17:00 (점심시간: 12:00 ~ 13:00)")

st.write("")
st.write("")

# 6. 중간 섹션: 카드형 메인 이용 절차
st.markdown("### 📌 보건실 이용 3단계 프로세스")
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class='feature-card'>
        <h3>🌱 STEP 1</h3>
        <h4>입장 및 방문 등록</h4>
        <p>보건실에 들어오시면 입구에 마련된 태블릿 PC 또는 종이 대장에 학과/성명과 방문 목적을 먼저 기록해 주세요.</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class='feature-card'>
        <h3>💊 STEP 2</h3>
        <h4>증상 설명 및 처치</h4>
        <p>보건선생님께 아픈 부위와 증상이 시작된 시간을 명확하게 말씀하신 후 증상에 맞는 의약품 복용 또는 처치를 받습니다.</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class='feature-card'>
        <h3>🛌 STEP 3</h3>
        <h4>안정 및 교실 복귀</h4>
        <p>추가 안정이 필요한 경우 선생님의 확인 하에 최대 1시간 동안 보건실 침상을 이용할 수 있으며, 휴식 후 교실로 복귀합니다.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# 7. 인터랙티브 기능: 증상별 방문 전 셀프 가이드
st.markdown("### 🩺 증상별 방문 전 행동 요령 (원클릭 안내)")
st.write("해당하는 증상 버튼을 누르시면 보건실에 오기 전 해야 할 행동을 알려드립니다.")

s_col1, s_col2, s_col3, s_col4 = st.columns(4)

with s_col1:
    if st.button("🩹 외상/찰과상 (피가 날 때)", use_container_width=True):
        st.info("👉 **행동 요령:** 흐르는 깨끗한 물에 상처 부위의 이물질을 먼저 씻어내세요. 출혈이 있다면 깨끗한 휴지나 거즈로 압박하면서 보건실로 오세요.")

with s_col2:
    if st.button("💊 두통/발열 (머리가 아플 때)", use_container_width=True):
        st.info("👉 **행동 요령:** 최근 4시간 이내에 타이레놀 등 다른 진통제를 먹은 적이 있는지 확인하세요. 약물의 중복 복용을 방지하기 위함입니다.")

with s_col3:
    if st.button("🤢 복통/소화불량 (배가 아플 때)", use_container_width=True):
        st.info("👉 **행동 요령:** 마지막으로 식사한 시간과 메뉴를 떠올려보세요. 보건실에 와서 공복 상태인지 여부를 말씀해 주셔야 정확한 처방이 가능합니다.")

with s_col4:
    if st.button("👁️ 안과/기타 통증", use_container_width=True):
        st.info("👉 **행동 요령:** 눈에 이물질이 들어갔을 때는 손으로 절대 비비지 말고 눈을 깜빡이며 눈물로 빼내거나 식용 정제수로 헹구며 방문하세요.")

# 8. 하단 푸터 (Footer)
st.markdown("<br><br><hr>", unsafe_allow_html=True)
st.markdown("<center style='color: #b2bec3; font-size:0.85rem;'>🏥 본 앱은 교내 보건실의 원활한 이용을 위한 안내용 메인 시스템입니다. | Emergency Call: 119</center>", unsafe_allow_html=True)
