# 한 번에 다 보여주던 폼 -> 단계별 챗봇으로
# 질문 1개 -> 답변 -> 다음 질문 1개 -> 답변
# Streamlit의 **st.session_state (세션 상태)**를 활용해서
# '지금 몇 번째 질문을 하고 있는지'와 '이전 대화 내역'을 기억하도록 코드
# 구글 시트에서 데이터를 매번 새로 불러오면 속도가 느려지므로 
# @st.cache_data를 활용해 데이터를 임시 저장(캐싱)하는 최적화 기법

import streamlit as st
import gspread

# --- 1. 기본 설정 및 세션 상태 초기화 ---
st.title("🤖 피부 고민 상담 챗봇")

# 세션 상태(저장소) 초기화
if 'step' not in st.session_state:
    st.session_state.step = -1  # -1: 시작 및 ID 입력, 0~11: 질문 단계, 12: 완료
if 'responses' not in st.session_state:
    st.session_state.responses = {}
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요! 맞춤형 피부 관리를 위한 상담 챗봇입니다. 🌿\n\n원활한 진행과 중복 참여 방지를 위해, 먼저 **연락처 또는 이메일**을 입력해 주세요."}
    ]
if 'user_id' not in st.session_state:
    st.session_state.user_id = ""

# --- 2. 구글 시트 연결 및 데이터 로드 (캐싱 처리로 속도 향상) ---
SPREADSHEET_NAME = '피부 고민 설문조사 시스템 (Streamlit 연동용)'

@st.cache_data(ttl=600) # 10분 동안 데이터 캐싱
def load_questions():
    credentials_dict = dict(st.secrets["gcp_service_account"])
    gc = gspread.service_account_from_dict(credentials_dict)
    spreadsheet = gc.open(SPREADSHEET_NAME)
    ws_questions = spreadsheet.worksheet('질문관리')
    return ws_questions.get_all_records()

def get_worksheet_responses():
    # 응답 기록용 워크시트 객체 반환 (캐싱하지 않음)
    credentials_dict = dict(st.secrets["gcp_service_account"])
    gc = gspread.service_account_from_dict(credentials_dict)
    spreadsheet = gc.open(SPREADSHEET_NAME)
    return spreadsheet.worksheet('응답결과')

try:
    questions_data = load_questions()
    ws_responses = get_worksheet_responses()
except Exception as e:
    st.error(f"구글 시트 연결 오류: {e}")
    st.stop()


# --- 3. 이전 대화 기록 화면에 그리기 ---
for msg in st.session_state.messages:
    # 챗봇은 로봇 아이콘, 사용자는 사람 아이콘 적용
    avatar = "🤖" if msg["role"] == "assistant" else "🧑"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])


# --- 4. 단계별 입력 및 대화 진행 로직 ---

# [단계 -1] : 식별자(ID) 입력 단계
if st.session_state.step == -1:
    user_input = st.chat_input("연락처 또는 이메일을 입력해 주세요.")
    if user_input:
        # 1) 사용자 메시지 기록
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # 2) 중복 확인
        existing_responses = ws_responses.get_all_values()
        existing_ids = [row[0] for row in existing_responses if len(row) > 0]
        
        if user_input in existing_ids:
            st.session_state.messages.append({"role": "assistant", "content": f"'{user_input}' 님은 이미 상담을 완료하셨습니다. 참여해 주셔서 감사합니다!"})
        else:
            # 3) 중복이 아니면 다음 단계로 넘어감
            st.session_state.user_id = user_input
            st.session_state.step = 0
            # 첫 번째 질문 텍스트 준비
            first_q = questions_data[0]
            bot_msg = f"Q{first_q['문항번호']}. {first_q['질문내용']}"
            st.session_state.messages.append({"role": "assistant", "content": bot_msg})
        
        st.rerun() # 화면 새로고침

# [단계 0 ~ 11] : 질문 진행 단계
elif st.session_state.step < len(questions_data):
    current_q = questions_data[st.session_state.step]
    q_type = current_q['질문유형']
    options = [opt.strip() for opt in str(current_q['선택지']).split(',')] if current_q['선택지'] else []
    
    # 다음 질문으로 넘어가는 내부 함수
    def go_next_step(answer_text, raw_answer):
        # 사용자 대화 기록 추가
        st.session_state.messages.append({"role": "user", "content": answer_text})
        # 응답 데이터 저장
        st.session_state.responses[current_q['문항번호']] = raw_answer
        # 단계 증가
        st.session_state.step += 1
        
        # 다음 질문이 있다면 챗봇 메시지로 추가
        if st.session_state.step < len(questions_data):
            next_q = questions_data[st.session_state.step]
            bot_msg = f"Q{next_q['문항번호']}. {next_q['질문내용']}"
            st.session_state.messages.append({"role": "assistant", "content": bot_msg})
        else:
            # 모든 질문이 끝났을 때
            st.session_state.messages.append({"role": "assistant", "content": "모든 질문이 완료되었습니다! 응답을 저장하는 중입니다... ⏳"})
        
        st.rerun()

    # 질문 유형에 따른 입력 위젯 렌더링
    if q_type == 'text':
        # 주관식: 하단 채팅 입력창 활성화
        user_text = st.chat_input("답변을 자유롭게 입력해 주세요.")
        if user_text:
            go_next_step(user_text, user_text)
            
    elif q_type in ['radio', 'checkbox']:
        # 객관식: 화면 하단에 선택 버튼 제공
        with st.container():
            st.write("---")
            if q_type == 'radio':
                selected = st.radio("항목을 선택해 주세요:", options, index=None, key=f"radio_{st.session_state.step}")
                if st.button("제출하기", type="primary", disabled=(selected is None)):
                    go_next_step(selected, selected)
            else: # checkbox
                selected_multi = st.multiselect("해당하는 항목을 모두 골라주세요 (다중 선택 가능):", options, key=f"multi_{st.session_state.step}")
                if st.button("제출하기", type="primary", disabled=(len(selected_multi) == 0)):
                    ans_str = ", ".join(selected_multi)
                    go_next_step(ans_str, ans_str)

# [단계 12] : 설문 완료 및 구글 시트 저장
elif st.session_state.step == len(questions_data):
    with st.spinner("응답결과 탭에 데이터를 기록하고 있습니다..."):
        row_to_append = [st.session_state.user_id]
        
        for q in questions_data:
            # 사용자가 건너뛴 경우 빈칸 처리
            ans = st.session_state.responses.get(q['문항번호'], "")
            row_to_append.append(ans)
            
        ws_responses.append_row(row_to_append)
        
    st.session_state.messages.append({"role": "assistant", "content": "🎉 데이터 저장이 완료되었습니다. 소중한 의견 진심으로 감사드립니다!"})
    st.session_state.step += 1 # 저장 루프 방지
    st.rerun()

elif st.session_state.step > len(questions_data):
    # 완전히 종료된 상태 (아무 동작도 하지 않고 대화 내역만 보여줌)
    pass