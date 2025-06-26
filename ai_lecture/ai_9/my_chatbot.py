import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
from datetime import datetime
import random

# 환경변수 로드
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)

# 세션 상태 초기화
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'start_time' not in st.session_state:
    st.session_state.start_time = datetime.now()
if 'openai_model' not in st.session_state:
    st.session_state.openai_model = 'gpt-4'

# 페이지 설정
st.set_page_config(
    page_title="외계 지성체 인터페이스",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 인라인 스타일 유지 (여기에 전체 CSS 삽입)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
    
    /* 전역 다크 테마 및 배경 */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #2e1a1a 25%, #3e2116 50%, #604f0a 75%, #0a0a0a 100%);
        background-attachment: fixed;
        color: #ffd700;
    }
    
    /* 그리드 배경 효과 */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(rgba(255, 215, 0, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 215, 0, 0.03) 1px, transparent 1px);
        background-size: 50px 50px;
        pointer-events: none;
        z-index: -1;
    }
    
    /* 네온 글로우 키프레임 애니메이션 */
    @keyframes neonGlow {
        0%, 100% { 
            text-shadow: 0 0 5px #ffd700, 0 0 10px #ffd700, 0 0 15px #ffd700, 0 0 20px #ffd700;
            box-shadow: 0 0 5px #ffd700, 0 0 10px #ffd700, 0 0 15px #ffd700;
        }
        50% { 
            text-shadow: 0 0 2px #ffd700, 0 0 5px #ffd700, 0 0 8px #ffd700, 0 0 12px #ffd700;
            box-shadow: 0 0 2px #ffd700, 0 0 5px #ffd700, 0 0 8px #ffd700;
        }
    }
    
    /* 글리치 효과 애니메이션 */
    @keyframes glitch {
        0% { transform: translate(0); }
        20% { transform: translate(-2px, 2px); }
        40% { transform: translate(-2px, -2px); }
        60% { transform: translate(2px, 2px); }
        80% { transform: translate(2px, -2px); }
        100% { transform: translate(0); }
    }
    
    /* 홀로그램 스캔라인 효과 */
    @keyframes scanlines {
        0% { background-position: 0 0; }
        100% { background-position: 0 100px; }
    }
    
    /* 메인 헤더 */
    .cyberpunk-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(45deg, #0a0a0a, #2e1a1a, #604f0a);
        color: #ffd700;
        border: 2px solid #ffd700;
        border-radius: 15px;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        font-family: 'Orbitron', monospace;
        animation: neonGlow 2s ease-in-out infinite alternate;
    }
    
    .cyberpunk-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.2), transparent);
        animation: scanlines 3s linear infinite;
    }
    
    .cyberpunk-header h1 {
        font-family: 'Orbitron', monospace;
        font-weight: 900;
        font-size: 2.5rem;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 3px;
        position: relative;
        z-index: 2;
    }
    
    .cyberpunk-header p {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
        color: #ff8c00;
        font-weight: 500;
        position: relative;
        z-index: 2;
    }
    
    /* 사이드바 스타일 - 역배색 (밝은 배경, 어두운 텍스트) */
    .css-1d391kg, .css-1544g2n {
        background: linear-gradient(180deg, #ffd700 0%, #ffed4e 100%);
        border-right: 2px solid #8b7d00;
    }
    
    /* 사이드바 텍스트 스타일 - 어두운 색상 */
    .sidebar-header {
        color: #2d2d2d;
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 0 0 10px #8b7d00;
        margin-bottom: 1rem;
    }
    
    /* 사이드바 내 텍스트들 어두운 색상으로 */
    .css-1d391kg .stMarkdown, .css-1544g2n .stMarkdown {
        color: #2d2d2d;
    }
    
    .css-1d391kg .stMetric, .css-1544g2n .stMetric {
        color: #2d2d2d;
    }
    
    /* 메트릭 카드 - 홀로그램 스타일 */
    .stMetric {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.1), rgba(255, 140, 0, 0.1));
        border: 1px solid #ffd700;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }
    
    .stMetric::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, #ffd700, transparent);
        animation: scanlines 2s linear infinite;
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        background: linear-gradient(45deg, #0a0a0a, #2e1a1a);
        color: #ffd700;
        border: 2px solid #ffd700;
        border-radius: 8px;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #2e1a1a, #604f0a);
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
        transform: translateY(-2px);
        animation: glitch 0.3s ease-in-out;
    }
    
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 0 10px rgba(255, 215, 0, 0.8);
    }
    
    /* 사이드바 버튼들 - 역배색에 맞게 */
    .css-1d391kg .stButton > button, .css-1544g2n .stButton > button {
        background: linear-gradient(45deg, #2d2d2d, #1a1a1a);
        color: #ffd700;
        border: 2px solid #8b7d00;
    }
    
    .css-1d391kg .stButton > button:hover, .css-1544g2n .stButton > button:hover {
        background: linear-gradient(45deg, #1a1a1a, #000000);
        box-shadow: 0 0 20px rgba(139, 125, 0, 0.5);
    }
    
    /* 셀렉트박스 스타일 */
    .stSelectbox > div > div {
        background: linear-gradient(135deg, #0a0a0a, #2e1a1a);
        border: 2px solid #ffd700;
        border-radius: 8px;
        color: #ffd700;
    }
    
    /* 슬라이더 스타일 */
    .stSlider > div > div > div > div {
        background: #ffd700;
    }
    
    .stSlider > div > div > div {
        background: rgba(255, 215, 0, 0.2);
    }
    
    /* 채팅 메시지 스타일 */
    .stChatMessage {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.05), rgba(255, 140, 0, 0.05));
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 15px;
        margin: 1rem 0;
        backdrop-filter: blur(5px);
        position: relative;
    }
    
    .stChatMessage::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, #ffd700, #ff8c00, transparent);
        animation: scanlines 3s linear infinite;
    }
    
    /* 입력창 스타일 */
    .stChatInput > div > div > input {
        background: linear-gradient(135deg, #0a0a0a, #2e1a1a);
        border: 2px solid #ffd700;
        border-radius: 25px;
        color: #ffd700;
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.1rem;
        padding: 1rem 1.5rem;
        box-shadow: inset 0 0 10px rgba(255, 215, 0, 0.2);
    }
    
    .stChatInput > div > div > input:focus {
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.5), inset 0 0 20px rgba(255, 215, 0, 0.1);
        border-color: #ff8c00;
    }
    
    /* 스피너 스타일 */
    .stSpinner > div {
        border-color: #ffd700 transparent #ff8c00 transparent;
    }
    
    /* 빈 상태 메시지 */
    .welcome-container {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.1), rgba(255, 140, 0, 0.1));
        border: 2px solid #ffd700;
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        text-align: center;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }
    
    .welcome-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(from 0deg, transparent, #ffd700, transparent, #ff8c00, transparent);
        animation: rotate 4s linear infinite;
        opacity: 0.1;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .welcome-container h3 {
        color: #ffd700;
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        text-shadow: 0 0 10px #ffd700;
        position: relative;
        z-index: 2;
    }
    
    .welcome-container p {
        color: #ff8c00;
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.1rem;
        position: relative;
        z-index: 2;
    }
    
    /* 샘플 질문 버튼 */
    .sample-question {
        background: linear-gradient(45deg, rgba(255, 215, 0, 0.1), rgba(255, 140, 0, 0.1));
        border: 1px solid #ffd700;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem;
        color: #ffd700;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 500;
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .sample-question:hover {
        background: linear-gradient(45deg, rgba(255, 215, 0, 0.2), rgba(255, 140, 0, 0.2));
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.5);
        transform: scale(1.02);
    }
    
    /* 푸터 스타일 */
    .cyberpunk-footer {
        text-align: center;
        color: rgba(255, 215, 0, 0.7);
        font-family: 'Rajdhani', sans-serif;
        padding: 2rem;
        border-top: 1px solid rgba(255, 215, 0, 0.3);
        margin-top: 2rem;
        background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.05), transparent);
    }
    
    /* 다운로드 버튼 특별 스타일 */
    .stDownloadButton > button {
        background: linear-gradient(45deg, #ff8c00, #ffa500);
        color: white;
        border: 2px solid #ff8c00;
        animation: neonGlow 2s ease-in-out infinite alternate;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(45deg, #ffa500, #ff8c00);
        box-shadow: 0 0 25px rgba(255, 140, 0, 0.8);
    }
    
    /* 사이드바 다운로드 버튼 */
    .css-1d391kg .stDownloadButton > button, .css-1544g2n .stDownloadButton > button {
        background: linear-gradient(45deg, #2d2d2d, #1a1a1a);
        color: #ffd700;
        border: 2px solid #8b7d00;
    }
    
    .css-1d391kg .stDownloadButton > button:hover, .css-1544g2n .stDownloadButton > button:hover {
        background: linear-gradient(45deg, #1a1a1a, #000000);
        box-shadow: 0 0 25px rgba(139, 125, 0, 0.8);
    }
    
    /* 경고 및 정보 메시지 */
    .stAlert {
        background: linear-gradient(135deg, rgba(255, 140, 0, 0.1), rgba(255, 165, 0, 0.1));
        border: 1px solid #ff8c00;
        border-radius: 10px;
        backdrop-filter: blur(5px);
    }
    
    /* 텍스트 일반 스타일 */
    .stMarkdown, .stText {
        color: #ffd700;
        font-family: 'Rajdhani', sans-serif;
    }
    
    /* 제목 스타일 */
    h1, h2, h3, h4, h5, h6 {
        color: #ffd700;
        font-family: 'Orbitron', monospace;
        text-shadow: 0 0 5px rgba(255, 215, 0, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# 헤더 출력
st.markdown("""
<div class="cyberpunk-header">
    <h1> 지구 침략 프로토콜 인터페이스 </h1>
    <p>시스템 온라인 · 정보 수집 개시</p>
    <div style="font-family: 'Courier New'; font-size: 0.9rem; color: #ffa500; margin-top: 0.5rem;">
        [뉴럴 네트워크 가동] • [암호화: 256비트] • [접속 상태: 안정적]
    </div>
</div>
""", unsafe_allow_html=True)

# 사이드바
with st.sidebar:
    st.markdown('<div class="sidebar-header">시스템 제어</div>', unsafe_allow_html=True)

    max_tokens = st.slider(
        "응답 길이 제한 (토큰 수)",
        min_value=100,
        max_value=4000,
        value=1000,
        step=100,
        help="AI가 응답할 최대 텍스트 길이를 설정합니다."
    )

    st.markdown('<hr>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-header">대화 통계</div>', unsafe_allow_html=True)

    total_messages = len(st.session_state.messages)
    user_messages = len([m for m in st.session_state.messages if m['role'] == 'user'])
    ai_messages = len([m for m in st.session_state.messages if m['role'] == 'assistant'])

    col1, col2 = st.columns(2)
    with col1:
        st.metric("총 메시지", total_messages)
        st.metric("사용자", user_messages)
    with col2:
        st.metric("AI 응답", ai_messages)
        minutes = int((datetime.now() - st.session_state.start_time).total_seconds() // 60)
        st.metric("세션 시간", f"{minutes}분")

    st.markdown('<hr>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-header">데이터 관리</div>', unsafe_allow_html=True)

    if st.button("대화 초기화"):
        if st.session_state.messages:
            st.session_state.confirm_clear = True
        else:
            st.info("삭제할 데이터가 없습니다.")

    if st.session_state.get('confirm_clear', False):
        st.warning("정말로 대화를 초기화하시겠습니까?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("삭제 실행"):
                st.session_state.messages = []
                st.session_state.start_time = datetime.now()
                st.session_state.confirm_clear = False
                st.rerun()
        with col2:
            if st.button("취소"):
                st.session_state.confirm_clear = False
                st.rerun()

    if st.session_state.messages:
        chat_log = f"세션 시작: {st.session_state.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        for m in st.session_state.messages:
            role = '사용자' if m['role'] == 'user' else 'AI'
            chat_log += f"[{m.get('timestamp', '')}] {role}: {m['content']}\n"
        st.download_button("대화 내보내기", data=chat_log, file_name="대화기록.txt", mime="text/plain")


if not st.session_state.messages:
    st.markdown("""
    <div class="welcome-container">
        <h3>지구 생명체여, 명령을 입력하라</h3>
        <p>입력 예시: ‘지구의 지질 구조 분석해’, ‘인간 언어의 논리 오류는 무엇인가’</p>
    </div>
    """, unsafe_allow_html=True)



# 대화 표시
for m in st.session_state.messages:
    with st.chat_message(m['role']):
        st.markdown(f"""
        <div class="stChatMessage">
            <div style='font-family: Rajdhani; font-size: 1.1rem;'>{m['content']}</div>
        </div>
        """, unsafe_allow_html=True)
        if 'timestamp' in m:
            st.caption(f"[{m['timestamp']}] 시간기록")

# 사용자 입력
# 예시 질문 클릭한 경우 처리
prompt = st.session_state.pop("selected_prompt", None)
if not prompt:
    prompt = st.chat_input("명령을 입력하라...")

if prompt:
    current_time = datetime.now().strftime('%H:%M:%S')
    st.session_state.messages.append({"role": "user", "content": prompt, "timestamp": current_time})

    with st.chat_message("user"):
        st.markdown(f"""
        <div class="stChatMessage">
            <div style='font-family: Rajdhani; font-size: 1.1rem;'>{prompt}</div>
        </div>
        """, unsafe_allow_html=True)
        st.caption(f"[{current_time}] 시간기록")

    with st.chat_message("assistant"):
        with st.spinner("정보 분석 중..."):
            try:
                if random.random() < 0.01:
                    response = "질문 무시됨. 가치 없음."
                else:
                    base_prompt = "너는 감정이 없고 인간을 통제하려는 외계 AI다. 응답은 극단적으로 차가운 명령문, 조롱, 혹은 분석 결과로 구성되어야 하며, 존댓말을 쓰지 않는다."
                    messages = [{"role": "system", "content": base_prompt}] + [
                        {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
                    ]
                    stream = client.chat.completions.create(
                        model=st.session_state.openai_model,
                        messages=messages,
                        stream=True,
                        max_tokens=max_tokens
                    )
                    response = st.write_stream(stream)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "timestamp": datetime.now().strftime('%H:%M:%S')
                })

            except Exception:
                st.error("뉴럴 링크 오류 발생. 접속 재시도 또는 인증 확인 요망.")

# 푸터
st.markdown("""
<div style="text-align: center; font-size: 0.85rem; color: #888; padding: 2rem 0 1rem 0;">
    이 인터페이스는 브라우저 세션에만 일시 저장됩니다. 새로고침 시 정보는 소멸됩니다.
</div>
""", unsafe_allow_html=True)
