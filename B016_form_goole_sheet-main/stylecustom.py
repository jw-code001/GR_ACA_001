# 특정 식별자를 주입하는 함수를 만들어 우회하는 방식으로 퍼블리셔와 협업
import streamlit as st
import gspread
import time




# --- 1. 기본 설정 및 세션 상태 초기화 ---
st.set_page_config(page_title="피부 고민 설문조사", page_icon="🌿")

# 👇 외부 CSS 파일을 읽어와서 적용하는 함수 (include_once 역할)
def local_css(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# 함수 실행! (style.css 파일의 내용을 화면에 주입)
local_css("style.css")
# 👆 이렇게 한 줄만 적어두면 끝입니다!

# 진행 단계(step), 응답 데이터(responses), 식별자(user_id)를 기억하는 저장소
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'responses' not in st.session_state:
    st.session_state.responses = {}
if 'user_id' not in st.session_state:
    st.session_state.user_id = ""


# --- 2. 구글 시트 연결 및 데이터 로드 ---
SPREADSHEET_NAME = '피부 고민 설문조사 시스템 (Streamlit 연동용)'

@st.cache_data(ttl=600)
def load_questions():
    credentials_dict = dict(st.secrets["gcp_service_account"])
    gc = gspread.service_account_from_dict(credentials_dict)
    return gc.open(SPREADSHEET_NAME).worksheet('질문관리').get_all_records()

def get_worksheet_responses():
    credentials_dict = dict(st.secrets["gcp_service_account"])
    gc = gspread.service_account_from_dict(credentials_dict)
    return gc.open(SPREADSHEET_NAME).worksheet('응답결과')

try:
    questions_data = load_questions()
except Exception as e:
    st.error(f"구글 시트 연결 오류: {e}")
    st.stop()


# --- 상단 프로그레스 바 표시 (질문 진행 중에만) ---
if 1 <= st.session_state.step <= len(questions_data):
    progress = st.session_state.step / len(questions_data)
    st.progress(progress, text=f"진행 상황: {st.session_state.step} / {len(questions_data)}")


# --- 3. 슬라이드형 화면 렌더링 ---

# [단계 0] 시작 및 식별자 입력
if st.session_state.step == 0:
    st.title("🌿 피부 고민 설문조사")
    st.write("원활한 진행과 중복 참여 방지를 위해 연락처 또는 이메일을 입력해주세요.")
    
    user_id_input = st.text_input(
    "연락처/이메일", 
    value=st.session_state.user_id, 
    key="contact_email_input_key" # <-- 이 줄을 추가합니다!
    )
    
    if st.button("시작하기 ➡️", type="primary"):
        if not user_id_input:
            st.warning("연락처 또는 이메일을 입력해야 시작할 수 있습니다.")
        else:
            with st.spinner("참여 이력 확인 중..."):
                ws_responses = get_worksheet_responses()
                existing_responses = ws_responses.get_all_values()
                existing_ids = [row[0] for row in existing_responses if len(row) > 0]
                
                if user_id_input in existing_ids:
                    st.error(f"'{user_id_input}' 님은 이미 설문에 참여하셨습니다.")
                else:
                    st.session_state.user_id = user_id_input
                    st.session_state.step = 1
                    st.rerun()

# [단계 1 ~ N] 개별 질문 슬라이드
elif 1 <= st.session_state.step <= len(questions_data):
    q_idx = st.session_state.step - 1
    current_q = questions_data[q_idx]
    q_num = current_q['문항번호']
    q_type = current_q['질문유형']
    options = [opt.strip() for opt in str(current_q['선택지']).split(',')] if current_q['선택지'] else []
    
    st.markdown(f"### Q{q_num}. {current_q['질문내용']}")
    
    # 이전 응답값 가져오기 (뒤로가기 시 데이터 보존용)
    saved_ans = st.session_state.responses.get(q_num, None)

    # 📌 단일 선택 (선택 즉시 다음 화면으로 이동)
    if q_type == 'radio':
        radio_key = f"radio_{q_num}"
        
        # 세션에 해당 문항 키가 없으면 초기값 세팅
        if radio_key not in st.session_state:
            st.session_state[radio_key] = saved_ans

        # 라디오 버튼이 클릭되었을 때 즉시 실행되는 함수
        def on_radio_change():
            st.session_state.responses[q_num] = st.session_state[radio_key]
            st.session_state.step += 1

        st.radio(
            "하나만 선택해주세요:", 
            options, 
            key=radio_key, 
            on_change=on_radio_change # 선택 시 즉시 다음 슬라이드로 넘어갑니다
        )
        
        st.write("---")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("⬅️ 이전", key=f"prev_{q_num}"):
                st.session_state.step -= 1
                st.rerun()
        with col2:
            # 이미 선택한 기록이 있어서 뒤로가기로 돌아온 경우, 변경 없이 넘어가기 위한 버튼
            if st.session_state[radio_key] is not None:
                if st.button("다음 ➡️", type="primary", key=f"next_{q_num}"):
                    st.session_state.responses[q_num] = st.session_state[radio_key]
                    st.session_state.step += 1
                    st.rerun()

    # 📌 다중 선택
    elif q_type == 'checkbox':
        multi_key = f"multi_{q_num}"
        raw_key = f"{q_num}_raw"
        saved_raw = st.session_state.responses.get(raw_key, [])
        
        selected = st.multiselect("해당하는 항목을 모두 골라주세요:", options, default=saved_raw, key=multi_key)
        
        st.write("---")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("⬅️ 이전", key=f"prev_{q_num}"):
                st.session_state.step -= 1
                st.rerun()
        with col2:
            if st.button("다음 ➡️", type="primary", key=f"next_{q_num}"):
                if len(selected) == 0:
                    st.warning("최소 1개 이상 선택해주세요.")
                else:
                    st.session_state.responses[raw_key] = selected
                    st.session_state.responses[q_num] = ", ".join(selected)
                    st.session_state.step += 1
                    st.rerun()

    # 📌 주관식 텍스트
    elif q_type == 'text':
        text_key = f"text_{q_num}"
        user_text = st.text_area("자유롭게 적어주세요:", value=saved_ans if saved_ans else "", key=text_key)
        
        st.write("---")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("⬅️ 이전", key=f"prev_{q_num}"):
                st.session_state.step -= 1
                st.rerun()
        with col2:
            if st.button("다음 ➡️", type="primary", key=f"next_{q_num}"):
                st.session_state.responses[q_num] = user_text
                st.session_state.step += 1
                st.rerun()

# [단계 N+1] 제출 확인 화면
elif st.session_state.step > len(questions_data):
    st.subheader("🎉 모든 질문에 답하셨습니다!")
    st.write("아래 버튼을 눌러 설문을 최종 제출해주세요.")
    
    st.write("---")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅️ 마지막 질문 확인하기"):
            st.session_state.step -= 1
            st.rerun()
    with col2:
        if st.button("최종 제출하기 🚀", type="primary"):
            with st.spinner("데이터 저장 중..."):
                ws_responses = get_worksheet_responses()
                
                # 제출 직전 안전하게 기존 데이터를 다시 확인하여 중복 입력을 차단합니다.
                existing_responses = ws_responses.get_all_values()
                existing_ids = [row[0] for row in existing_responses if len(row) > 0]
                
                if st.session_state.user_id in existing_ids:
                    st.error("이미 제출된 이력이 존재합니다. 중복 제출이 차단되었습니다.")
                else:
                    row_to_append = [st.session_state.user_id]
                    for q in questions_data:
                        ans = st.session_state.responses.get(q['문항번호'], "")
                        row_to_append.append(ans)
                        
                    ws_responses.append_row(row_to_append)
                    st.success("설문 응답이 성공적으로 등록되었습니다. 감사합니다!")
                    
                    # 성공 메시지를 잠깐 보여준 뒤 폼을 깨끗하게 비우고 새로고침합니다.
                    time.sleep(1.5)
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.rerun()