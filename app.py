import streamlit as st
import datetime

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="스마트 보건실 가이드",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. 보건실 테마에 맞는 커스텀 스타일 적용 (에메랄드/그린 톤)
st.markdown("""
    <style>
    .main-title {
        color: #00875A;
        text-align: center;
        font-weight: bold;
    }
    .sub-title {
        color: #4A5568;
        text-align: center;
        margin-bottom: 30px;
    }
    .info-box {
        background-color: #E6FFFA;
        border-left: 5px solid #319795;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 헤더 영역 (메인 페이지 느낌 전달)
st.markdown("<h1 class='main-title'>🏥 스마트 보건실 안내 시스템</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>안전하고 건강한 하루를 위해 보건실 이용 방법을 안내해 드립니다.</p>", unsafe_allow_html=True)
st.divider()

# 4. 실시간 보건실 현황 안내
col1, col2 = st.columns(2)
with col1:
    current_time = datetime.datetime.now().time()
    if datetime.time(9, 0) <= current_time <= datetime.time(17, 0):
        st.success("🟢 현재 보건실 운영 중 (이용 가능)")
    else:
        st.warning("🟡 현재 보건실 운영 시간 외")

with col2:
    st.info("🕒 운영 시간: 평일 09:00 ~ 17:00")

st.write("") # 간격 조절

# 5. 핵심 기능: 증상별 방문 가이드 & 기능 설명
st.subheader("🩺 증상별 맞춤 이용 가이드")
st.write("현재 겪고 계신 증상을 선택하시면, 보건실 방문 전 대처법과 이용 안내를 확인하실 수 있습니다.")

# 탭을 이용한 직관적인 기능 설명 화면 구성
tab1, tab2, tab3, tab4 = st.tabs(["🩹 외상/찰과상", "💊 두통/발열", "🤢 복통/소화불량", "🏃 휴식/안정"])

with tab1:
    st.markdown("""
    <div class='info-box'>
        <h4>🩹 외상 및 찰과상 발생 시</h4>
        <p><strong>방문 전 행동:</strong> 흐르는 깨끗한 물에 상처 부위를 먼저 씻어주세요. 출혈이 심할 경우 깨끗한 거즈나 수건으로 압박하며 방문하세요.</p>
        <p><strong>보건실 처치:</strong> 소독, 연고 도포, 밴드 및 붕대 드레싱</p>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown("""
    <div class='info-box'>
        <h4>💊 두통 및 발열 발생 시</h4>
        <p><strong>방문 전 행동:</strong> 최근 4시간 이내에 다른 해열진통제를 복용했는지 기억해 주세요. (중복 복용 방지)</p>
        <p><strong>보건실 처치:</strong> 체온 측정, 증상에 따른 해열진통제 투약, 필요 시 냉찜질</p>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown("""
    <div class='info-box'>
        <h4>🤢 복통 및 소화불량 발생 시</h4>
        <p><strong>방문 전 행동:</strong> 마지막으로 식사한 시간과 메뉴를 생각하고 와주세요. 공복 상태인지 확인이 필요합니다.</p>
        <p><strong>보건실 처치:</strong> 소화제나 위장약 처방 후 필요시 침상 안정을 병행할 수 있습니다.</p>
    </div>
    """, unsafe_allow_html=True)

with tab4:
    st.markdown("""
    <div class='info-box'>
        <h4>🏃 침상 안정 및 휴식이 필요할 때</h4>
        <p><strong>이용 규칙:</strong> 보건선생님의 확인 후 최대 1시간 동안 침상을 이용할 수 있습니다.</p>
        <p><strong>주의사항:</strong> 휴식 중에는 스마트폰 사용을 자제하고 편안하게 안정을 취해주세요.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()
