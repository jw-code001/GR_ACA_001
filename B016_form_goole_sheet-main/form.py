import streamlit as st
import gspread

# 1. API 인증 및 구글 스프레드시트 연결
try:
    credentials_dict = dict(st.secrets["gcp_service_account"])
    gc = gspread.service_account_from_dict(credentials_dict)
except Exception as e:
    st.error("인증 정보를 불러오지 못했습니다. secrets.toml 설정을 확인해주세요.")
    st.stop()

# 2. 스프레드시트 및 탭 연결
SPREADSHEET_NAME = '피부 고민 설문조사 시스템 (Streamlit 연동용)'

try:
    spreadsheet = gc.open(SPREADSHEET_NAME)
    ws_questions = spreadsheet.worksheet('질문관리')
    ws_responses = spreadsheet.worksheet('응답결과')
except gspread.exceptions.SpreadsheetNotFound:
    st.error("스프레드시트를 찾을 수 없습니다. 서비스 계정 이메일이 시트에 공유되었는지 확인해주세요.")
    st.stop()

# 3. '질문관리' 탭에서 데이터 읽어오기
# get_all_records()를 사용하면 첫 줄을 키(Key)로 하는 딕셔너리 리스트를 반환하여 다루기 쉽습니다.
questions_data = ws_questions.get_all_records()

st.title("📋 피부 고민 설문조사")
st.write("소중한 의견을 남겨주시면 감사하겠습니다.")

# 중복 참여 방지를 위한 식별자 입력란 (폼 밖에 배치)
user_id = st.text_input("연락처 또는 이메일을 입력해주세요 (중복 참여 확인용)", placeholder="010-0000-0000 또는 email@example.com")

# 4. 설문조사 폼 동적 생성
with st.form("survey_form"):
    responses = {} # 사용자 응답을 저장할 딕셔너리
    
    for q in questions_data:
        q_num = q['문항번호']
        q_text = f"Q{q_num}. {q['질문내용']}"
        q_type = q['질문유형']
        
        # 선택지가 있는 경우 쉼표로 분리하여 리스트로 만듭니다.
        q_options = [opt.strip() for opt in str(q['선택지']).split(',')] if q['선택지'] else []
        
        # 질문 유형에 따라 스트림릿 위젯 렌더링
        if q_type == 'radio':
            responses[q_num] = st.radio(q_text, options=q_options, index=None, key=f"q_{q_num}")
            
        elif q_type == 'checkbox':
            # 체크박스(다중 선택)는 스트림릿의 multiselect 활용
            responses[q_num] = st.multiselect(q_text, options=q_options, key=f"q_{q_num}")
            
        elif q_type == 'text':
            responses[q_num] = st.text_area(q_text, key=f"q_{q_num}")
            
        st.write("---") # 문항 사이 구분선

    # 폼 제출 버튼
    submitted = st.form_submit_button("설문 제출하기", type="primary")

    if submitted:
        if not user_id:
            st.warning("설문을 제출하려면 연락처 또는 이메일을 입력해주세요.")
        else:
            with st.spinner("제출 중입니다..."):
                # 5. 기존 응답 확인 (중복 체크)
                existing_responses = ws_responses.get_all_values()
                # 첫 번째 열(인덱스 0)이 식별자(연락처/이메일)
                existing_ids = [row[0] for row in existing_responses if len(row) > 0]
                
                if user_id in existing_ids:
                    st.error(f"'{user_id}' 님은 이미 설문에 참여하셨습니다. 참여해주셔서 감사합니다!")
                else:
                    # 6. '응답결과' 탭에 새 데이터 추가
                    # 저장할 데이터 한 줄(리스트) 만들기: [식별자, 1번응답, 2번응답, ...]
                    row_to_append = [user_id]
                    
                    for q in questions_data:
                        ans = responses[q['문항번호']]
                        
                        # 다중 선택(multiselect) 결과는 리스트이므로 쉼표로 연결된 문자열로 변환
                        if isinstance(ans, list):
                            ans = ", ".join(ans)
                            
                        # 응답을 하지 않은 None 상태 처리
                        if ans is None:
                            ans = ""
                            
                        row_to_append.append(ans)
                    
                    # 시트에 한 줄 추가 (append_row)
                    ws_responses.append_row(row_to_append)
                    st.success("성공적으로 제출되었습니다. 설문에 참여해 주셔서 감사합니다!")
# 임시 개발용 로컬 서버 streamlit run form.py