# 데이터의 흐름: 정적(Static) vs 동적(Dynamic)
  -기존 방식: 개발자인 사용자님이 "메뉴 빈도수를 분석해서 워드클라우드를 그려라"라고 코드를 미리 짜두었습니다. (정적)<br>

  -랭체인 방식: 사용자가 "요즘 잘 나가는 메뉴가 뭐야? 그래프로 보여줘"라고 채팅을 치면, 랭체인이 시각화에 필요한 데이터를 RAG로 가져온 뒤 어떤 그래프를 그릴지 실시간으로 결정합니다. (동적)

# requirements.txt 추가 
# --- 기존 라이브러리 ---
pandas
streamlit
matplotlib
wordcloud

# --- LangChain & AI 관련 추가 ---
langchain
langchain-openai  # 또는 langchain-community (Gemini 사용 시)
chromadb          # 벡터 저장소
tiktoken          # 토큰 계산용
tabulate          # 데이터프레임 처리 보조


## 🤖 Upgrading to AI-Powered Visualization
* **Core:** LangChain + RAG (Retrieval-Augmented Generation)
* **Agent:** Utilizing `PythonAstREPLTool` for dynamic chart generation.
* **Knowledge Base:** Google Sheets data indexed via ChromaDB.


# Secrets 관리
* 랭체인을 쓰면 OPENAI_API_KEY나 GOOGLE_API_KEY가 추가로 필요합니다. 이전에 설정하신 
* secrets.toml에 이 키값들도 꼭 추가해주어야 배포 시 에러가 나지 않습니다.


### 🧩 Semantic Data Mapping (Tuple Logic)
* **Data Ingestion:** 각 데이터 포인트(Text)를 고차원 벡터(Vector)와 1:1 매핑하여 'Semantic Tuple' 생성.
* **Vector DB Storage:** 생성된 튜플을 인덱싱하여 단순 검색이 아닌 '공간적 근접성' 기반의 데이터 추출 구현.
* **Context Assembly:** 검색된 상위 랭킹 튜플들의 텍스트 파트(Metadata)를 결합하여 LLM의 프롬프트 컨텍스트로 주입.

### ⚡ Efficient Retrieval via Vector Indexing
* **Spatial Locality:** 비슷한 의미를 가진 데이터를 벡터 공간상에 인접하게 배치하여 검색 동선 최적화.
* **Clustering Strategy:** 고차원 공간을 여러 구역(Cluster)으로 분할 인덱싱하여, 질의와 무관한 영역을 탐색에서 제외(Pruning).
* **Speed & Accuracy:** 인덱싱을 통해 수만 개의 구글 시트 행 중 가장 관련성 높은 컨텍스트를 밀리초(ms) 단위로 추출.

### 예측 범주'가 넓어지는 이유 (유연한 짝짓기)
* 전통적인 데이터베이스(SQL)는 정확히 일치하는 키만 찾을 수 있는 엄격한 딕셔너리였다면, 
  벡터 DB는 "키가 좀 달라도 느낌이 비슷하면 뽑아주는" 유연한 튜플 시스템입니다.

* SQL (Strict): "사과"가 없으면 에러 혹은 결과 없음.

* Vector (Flexible): "사과"가 없어도 "부사", "청송 과일", "Apple" 같은 
  유사한 좌표의 짝꿍들을 찾아내서 범주를 넓힙니다.
  ->" 생성된 튜플을 인덱싱하여 " -> 아무대나 배치하지않음 -> 스펙트럼을 만듬


  https://docs.google.com/spreadsheets/d/1spR6wI3PADq7qTF-jJC68y061JmAoYQH6cj5MF89HZg/edit?usp=sharing


