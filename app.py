import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError

# 1. 페이지 레이아웃 및 제목 설정
st.set_page_config(page_title="스마트 보건실 챗봇", page_icon="🏥", layout="centered")
st.title("🏥 스마트 보건실 안내 챗봇")
st.caption("보건실 이용 방법이나 가벼운 증상 대처법을 물어보세요. (Model: gemini-2.5-flash-lite)")

# 2. Streamlit Secrets에서 API 키 안전하게 불러오기
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except KeyError:
    st.error("❌ Streamlit Secrets에서 'GEMINI_API_KEY'를 찾을 수 없습니다. 설정 공간을 확인해주세요.")
    st.stop()

# 3. 챗봇 페르소나 (시스템 지침) 정의
SYSTEM_PROMPT = """
당신은 학교 보건실의 친절하고 전문적인 '보건 선생님'입니다.
사용자는 보건실을 방문한 학생 또는 교직원입니다.
다음 지침을 반드시 준수하세요:
1. 보건실 위치, 이용 에티켓, 가벼운 증상(두통, 복통, 가벼운 상처 등)에 대해 따뜻하고 친절하게 안내합니다.
2. 증상이 심각해 보이거나 응급 상황이 의심될 경우, 반드시 "즉시 병원 진료를 받거나 119에 신고해야 한다"는 경고 문구를 포함하세요.
3. 전문 의학 용어보다는 사용자가 이해하기 쉬운 쉬운 단어를 사용하세요.
"""

# 4. 세션 상태(Session State)로 채팅 기록 유지 및 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요! 보건실 챗봇입니다. 어디가 아프시거나 궁금한 점이 있으신가요?"}
    ]

# 5. 기존에 주고받았던 대화 내용을 화면에 다시 그리기
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. 사용자 입력 처리
if user_input := st.chat_input("증상이나 궁금한 점을 입력하세요. (예: 머리가 아파요)"):
    
    # 사용자가 입력한 메시지를 기록하고 화면에 표시
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)  # <- 이 부분의 오타를 수정했습니다!

    # 챗봇 답변 생성 및 화면 표시
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # 시스템 프롬프트(페르소나)를 대화의 시작점(첫 Content)으로 주입
        contents = [
            types.Content(role="user", parts=[types.Part.from_text(text=SYSTEM_PROMPT)])
        ]
        
        # 누적된 대화 기록을 API 규격에 맞춰 변환 (assistant -> model)
        for msg in st.session_state.messages:
            api_role = "model" if msg["role"] == "assistant" else "user"
            contents.append(
                types.Content(role=api_role, parts=[types.Part.from_text(text=msg["content"])])
            )

        try:
            with st.spinner("보건 선생님이 답변을 생각하고 있습니다..."):
                # gemini-2.5-flash-lite 모델 호출
                response = client.models.generate_content(
                    model='gemini-2.5-flash-lite',
                    contents=contents,
                )
                
                ai_response = response.text
                message_placeholder.markdown(ai_response)
                
                # 생성된 답변을 세션 상태에 저장하여 기록 유지
                st.session_state.messages.append({"role": "assistant", "content": ai_response})

        except APIError as e:
            message_placeholder.error(f"⚠️ Gemini API 인증 또는 호출 오류가 발생했습니다: {e.message}")
        except Exception as e:
            message_placeholder.error(f"⚠️ 시스템 오류가 발생했습니다: {str(e)}")
