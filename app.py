import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="스마트 보건실 챗봇", page_icon="🏥", layout="centered")
st.title("🏥 스마트 보건실 안내 챗봇")
st.caption("보건실 이용 방법, 가벼운 증상 대처법 등을 물어보세요! (현재 모델: gemini-2.5-flash-lite)")

# 2. Streamlit Secrets에서 API 키 불러오기 및 클라이언트 초기화
try:
    # Streamlit Cloud의 Secrets 또는 로컬의 secrets.toml에서 키를 가져옵니다.
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except KeyError:
    st.error("❌ API 키를 찾을 수 없습니다. Streamlit Secrets 설정을 확인해주세요.")
    st.stop()

# 3. 챗봇 페르소나 (시스템 프롬프트) 정의
SYSTEM_PROMPT = """
당신은 학교 또는 직장의 친절하고 전문적인 '보건실 담당 선생님'입니다.
사용자는 보건실 이용자(학생 또는 직원)입니다.
다음 지침을 반드시 따르세요:
1. 보건실 위치, 이용 시간, 가벼운 증상(두통, 복통, 찰과상 등)에 대한 대처법을 친절하게 안내합니다.
2. 위급 상황이 의심되거나 증상이 심각해 보일 경우, 반드시 "즉시 병원 진료를 받거나 119에 신고하라"는 안내를 포함하세요.
3. 답변은 이해하기 쉽고 따뜻한 어조로 작성하세요.
"""

# 4. 세션 상태(Session State)를 활용한 채팅 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요! 보건실 챗봇입니다. 어디가 아프시거나 궁금한 점이 있으신가요?"}
    ]

# 5. 기존 채팅 기록 화면에 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. 사용자 입력 및 대화 처리
if user_input := st.chat_input("증상이나 궁금한 점을 입력하세요 (예: 머리가 아파요)"):
    
    # 사용자가 입력한 메시지 저장 및 화면 표시
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input})

    # 챗봇의 답변 생성 및 화면 표시
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # API 호출을 위한 메시지 히스토리 포맷 변환 (시스템 프롬프트 포함)
        contents = [types.Content(role="user", parts=[types.Part.from_text(text=SYSTEM_PROMPT)])]
        
        for msg in st.session_state.messages:
            # assistant는 'model'로 역할을 매핑해야 API가 인식합니다.
            role = "model" if msg["role"] == "assistant" else "user"
            contents.append(types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])]))

        try:
            with st.spinner("생각 중..."):
                # gemini-2.5-flash-lite 모델 호출
                response = client.models.generate_content(
                    model='gemini-2.5-flash-lite',
                    contents=contents,
                )
                
                ai_response = response.text
                message_placeholder.markdown(ai_response)
                
                # 대화 기록에 챗봇 답변 추가
                st.session_state.messages.append({"role": "assistant", "content": ai_response})

        except APIError as e:
            # Gemini API 관련 에러 처리
            error_msg = f"⚠️ Gemini API 오류가 발생했습니다: {e.message}"
            message_placeholder.error(error_msg)
        except Exception as e:
            # 기타 예외 처리
            error_msg = f"⚠️ 예기치 못한 오류가 발생했습니다: {str(e)}"
            message_placeholder.error(error_msg)
