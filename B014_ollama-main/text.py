# test.py 수정본
from langchain_chroma import Chroma  # 이제 이 줄이 정상 작동합니다.
from langchain_ollama import OllamaEmbeddings

# 1. 임베딩 모델 설정 (DB 생성 때와 동일하게!)
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

# 2. 저장된 벡터 DB 로드
# 저장했던 폴더 경로("./chroma_db_ollama")가 맞는지 확인하세요.
db = Chroma(
    persist_directory="./chroma_db_ollama", 
    embedding_function=embeddings
)

# 3. 유사도 검색 테스트
query = "포랩 메뉴" # 시트에 있을 법한 단어로 테스트해보세요.
docs = db.similarity_search(query, k=3)

print("\n--- 🎯 벡터 DB 검색 결과 ---")
if not docs:
    print("검색 결과가 없습니다. DB 생성 과정을 다시 확인해 보세요.")
else:
    for i, doc in enumerate(docs):
        print(f"[{i+1}순위] {doc.page_content[:150]}...")
        print("-" * 30)