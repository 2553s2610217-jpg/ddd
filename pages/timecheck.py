
import streamlit as st
from datetime import datetime, time, timedelta

# --- 1. 페이지 기본 설정 ---
st.set_page_config(
    page_title="보건실 이용 안내 시스템",
    page_icon="🏥",
    layout="centered"
)

# --- 2. 보건실 운영 시간 정의 ---
# 주말 및 공휴일 제외 (월~금 운영 기준)
OPEN_TIME = time(9, 0)       # 오전 9시 오픈
LUNCH_START = time(12, 0)    # 12시 점심시간 시작
LUNCH_END = time(13, 0)      # 1시 점심시간 종료
CLOSE_TIME = time(18, 0)     # 오후 6시 마감

# --- 3. 현재 시간 및 상태 계산 ---
now = datetime.now()
current_time = now.time()
current_weekday = now.weekday()  # 0: 월, ..., 5: 토, 6: 일

# 테스트를 위한 시간 고정 기능 (개발/확인용, 실제 배포 시 현재 시간 기준)
# current_time = time(12, 30) 

def get_status_and_message(weekday, c_time):
    # 주말인 경우
    if weekday >= 5:
        return "CLOSED_WEEKEND", "주말 및 공휴일은 보건실을 운영하지 않습니다. 🚑"
    
    # 오픈 전
    if c_time < OPEN_TIME:
        return "BEFORE_OPEN", f"아직 운영 전입니다. **오전 9시**에 오픈합니다."
    
    # 오전 운영 시간
    elif OPEN_TIME <= c_time < LUNCH_START:
        # 마감(점심)까지 남은 시간 계산
        rem_hours = LUNCH_START.hour - c_time.hour - 1
        rem_mins = 60 - c_time.minute
        if rem_mins == 60:
            rem_hours += 1
            rem_mins = 0
        time_str = f"{rem_hours}시간 {rem_mins}분" if rem_hours > 0 else f"{rem_mins}분"
        return "OPEN", f"현재 정상 운영 중입니다! (점심시간까지 **{time_str}** 남음)"
    
    # 점심 시간
    elif LUNCH_START <= c_time < LUNCH_END:
        rem_mins = 60 - c_time.minute
        return "LUNCH", f"지금은 점심시간입니다. **오후 1시({rem_mins}분 후)**에 다시 운영을 시작합니다."
    
    # 오후 운영 시간
    elif LUNCH_END <= c_time < CLOSE_TIME:
        rem_hours = CLOSE_TIME.hour - c_time.hour - 1
        rem_mins = 60 - c_time.minute
        if rem_mins == 60:
            rem_hours += 1
            rem_mins = 0
        time_str = f"{rem_hours}시간 {rem_mins}분" if rem_hours > 0 else f"{rem_mins}분"
        return "OPEN", f"현재 정상 운영 중입니다! (오늘 마감까지 **{time_str}** 남음)"
    
    # 마감 이후
    else:
        return "CLOSED", "오늘 운영이 종료되었습니다. 내일 **오전 9시**에 다시 문을 엽니다."

status, message = get_status_and_message(current_weekday, current_time)

# --- 4. UI 렌더링 ---
st.title("🏥 캠퍼스 보건실 실시간 안내")
st.write(f"📅 현재 시각: **{now.strftime('%Y-%m-%d %H:%M')}**")
st.markdown("---")

# 4-1. 실시간 운영 상태 배너
st.subheader("🔔 현재 보건실 상태")
if status == "OPEN":
    st.success(f"### 🎉 {message}")
elif status == "LUNCH":
    st.warning(f"### 🍱 {message}")
elif status in ["BEFORE_OPEN", "CLOSED", "CLOSED_WEEKEND"]:
    st.error(f"### 🚪 {message}")

st.markdown("---")

# 4-2. 운영 시간표 안내
st.subheader("🕒 정규 운영 시간 안내")
col1, col2 = st.columns(2)
with col1:
    st.info("**평일(월~금)**\n* **오전 운영:** 09:00 ~ 12:00\n* **점심 시간:** 12:00 ~ 13:00\n* **오후 운영:** 13:00 ~ 18:00")
with col2:
    st.error("**주말 및 공휴일**\n* **휴무**\n\n📢 *긴급 응급상황 발생 시에는 즉시 119 또는 인근 병원을 이용해 주세요.*")

st.markdown("---")

# 4-3. 차별화 기능: 증상별 사전 체크 및 안내
st.subheader("🩹 보건실 방문 전 증상별 체크")
st.write("현재 겪고 계신 증상을 선택하시면 간단한 대처법과 보건실 지원 사항을 알려드립니다.")

symptom = st.selectbox(
    "어디가 아프신가요?",
    ["선택하세요", "두통 / 발열", "복통 / 소화불량", "상처 / 화상 / 출혈", "근육통 / 삐었음"]
)

if symptom != "선택하세요":
    st.markdown(f"### 📝 **{symptom}** 대처 가이드")
    if symptom == "두통 / 발열":
        st.write("📌 **보건실 지원:** 해열진통제(타이레놀 등) 처방 및 침상 안정 가능")
        st.caption("💡 **Tip:** 보건실 방문 후 체온 측정을 먼저 진행해 주세요. 충분한 수분 섭취가 도움이 됩니다.")
    elif symptom == "복통 / 소화불량":
        st.write("📌 **보건실 지원:** 소화제, 지설제 처방 및 온찜질 팩 대여")
        st.caption("💡 **Tip:** 증상이 심할 경우 침상 안정을 요청할 수 있습니다. 마지막 식사 시간을 보건선생님께 말씀해 주세요.")
    elif symptom == "상처 / 화상 / 출혈":
        st.write("📌 **보건실 지원:** 소독, 연고 도포, 밴드/붕대 드레싱, 화상 거즈 조치")
        st.caption("🚨 **주의:** 흐르는 깨끗한 물에 상처를 먼저 씻고 오시면 더 빠른 조치가 가능합니다.")
    elif symptom == "근육통 / 삐었음":
        st.write("📌 **보건실 지원:** 냉/온찜질 팩 제공, 파스 부착, 압박붕대 고정")
        st.caption("💡 **Tip:** 부상을 입은 지 24시간 이내라면 냉찜질이 효과적입니다.")
