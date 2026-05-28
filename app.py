import streamlit as st  # <- 여기를 정확히 st로 가져옵니다!
import random

# 1. 앱 제목 설정
st.title("🍚 오늘 뭐 먹지?")
st.write("결정장애가 온 당신을 위해 준비했습니다. 버튼을 눌러보세요!")

# 2. 음식 메뉴 리스트
menus = [
    "김치찌개", "된장찌개", "제육볶음", "돈가스", "짜장면", 
    "치킨", "피자", "삼겹살", "초밥", "쌀국수", 
    "떡볶이", "햄버거", "마라탕", "샐러드"
]

# 3. 추천 버튼 만들기
if st.button("오늘의 메뉴 추천받기 🎲"):
    # 리스트에서 랜덤으로 하나 뽑기
    selected_menu = random.choice(menus)
    
    # 결과 보여주기
    st.balloons()  # 축하하는 풍선 애니메이션 효과
    st.success(f"오늘 추천하는 메뉴는 바로... **【 {selected_menu} 】** 입니다! 🎉")
