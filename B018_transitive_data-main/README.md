# transitive_data
구글 시트를 시작점으로 해서 벡터 DB를 거쳐 스트림릿(Streamlit) 시각화까지 이어지는 흐름은 RAG(Retrieval-Augmented Generation) 시스템의 정석적인 구조


🏗️ 전체 아키텍처 흐름[데이터 소스: 구글 시트]
[가공/임베딩: Python/LangChain] 
[저장소: 벡터 DB] 
[인터페이스: 스트림릿]

1단계: 구글 시트 데이터 로드 및 전처리
구글 시트의 데이터를 벡터 DB에 넣기 위해 먼저 텍스트 형태로 가져와야 합니다.

방법: Python의 gspread 라이브러리나 LangChain의 GoogleSheetsLoader를 사용합니다.

핵심: 시트의 각 행(Row)을 하나의 문서(Document) 단위로 변환합니다.

2단계: 벡터 DB(Vector Store) 생성 및 저장
슈파베이스를 이미 고려 중이시라면, 슈파베이스의 pgvector를 벡터 DB로 사용하는 것이 가장 효율적입니다. 별도의 DB를 추가할 필요가 없으니까요.

Chunking: 긴 텍스트를 의미 있는 단위로 쪼갭니다.

Embedding: OpenAI의 text-embedding-3-small 같은 모델을 사용하여 텍스트를 숫자의 배열(벡터)로 바꿉니다.

Upsert: 변환된 벡터 데이터를 슈파베이스 테이블에 저장합니다.

3단계: 스트림릿(Streamlit) 인터페이스 및 시각화
이제 사용자가 질문을 하면 챗봇이 답하고 관련 데이터를 시각화해줄 차례입니다.

검색(Retrieval): 사용자의 질문을 벡터로 변환해 슈파베이스에서 유사한 데이터를 찾아옵니다.

LLM 응답: 찾아온 데이터를 바탕으로 챗봇이 답변을 생성합니다.

시각화(Visualization): 답변에 포함된 수치 데이터를 **Streamlit의 차트 기능(st.bar_chart, st.line_chart)**이나 Plotly를 활용해 화면에 뿌려줍니다.


💡 이 과정에서의 핵심 포인트
1. "실시간성" 확보 (동기화)
구글 시트에서 내용을 수정했을 때 벡터 DB에도 반영되어야 합니다.

추천 방식: 스트림릿 앱에 '데이터 새로고침' 버튼을 만들거나, 슈파베이스 Edge Function을 이용해 시트 업데이트 시 자동으로 임베딩을 다시 수행하게 만듭니다.


무결성(Data Integrity)과 실무적인 관리 효율성을 고려할 때, [구글 폼 → 구글 앱스 스크립트 → Supabase 전송 → 성공 시 구글 시트 기록] 순서로 처리하는 것이 가장 확실

2. 데이터 구조화
시트에 단순히 글만 적는 게 아니라, [카테고리 / 날짜 / 수치 / 설명] 식으로 열(Column)을 잘 구분해두어야 나중에 스트림릿에서 그래프를 그릴 때 훨씬 편합니다.

3. 보안
구글 시트 API 키와 슈파베이스 API 키는 반드시 스트림릿의 .streamlit/secrets.toml 파일에 따로 관리하여 코드에 노출되지 않도록 하세요.


데이터베이스는 **[사용자] - [질문] - [응답]**의 관계


# 무결성(Data Integrity)과 실무적인 관리 효율성을 고려할 때,
***[구글 폼 → 구글 앱스 스크립트 → Supabase 전송 → 성공 시 구글 시트 기록] 순서로 처리하는 것이 가장 확실


# 인덱스 추가 (조회 성능 향상 - 취업용 디테일)
create index idx_answers_user_email on survey_answers (user_email);
create index idx_answers_question_no on survey_answers (question_no);
