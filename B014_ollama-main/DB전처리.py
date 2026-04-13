# pip install -U pandas streamlit google-api-python-client google-auth langchain-core langchain-community langchain-text-splitters langchain-chroma langchain-ollama

import os
# os 모듈은 파이썬 프로그램이 컴퓨터의 운영체제(Windows, Linux, macOS 등)와 대화할 수 있게 해주는 통역사 역할


# gspread는 엑셀처럼 셀(Cell) 단위의 제어에 특화되어 있다 보니, 구글 시트의 헤더(Header)가 복잡
# **GoogleSheetsLoader**는 개별 셀의 서식이나 디자인은 다 무시하고, 오직 **'데이터(값) 자체'**를 AI가 읽기 좋은 텍스트 뭉치로 빠르게 퍼올리는 데 최적화
# 어차피 셀의 위치중요하지않아... 데이터를 재편성할 거임


import pandas as pd
import streamlit as st
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from langchain_core.documents import Document

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

from langchain_ollama import OllamaEmbeddings

# 1. 구글 시트 데이터 직접 로드 함수 (Loader 에러 회피용)
def get_sheets_data(spreadsheet_id, sheet_name):
    try:
        # 1. 인증 정보 생성 (이 부분이 빠져있었습니다)
        creds_info = st.secrets["gcp_service_account"]
        creds = Credentials.from_service_account_info(
            creds_info, 
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
        
        # 2. Google Sheets API 연결
        service = build('sheets', 'v4', credentials=creds)
        
        # 3. 데이터 가져오기 (매개변수 이름: spreadsheetId)
        range_name = f"{sheet_name}!A1:Z1000"
        request = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, 
            range=range_name
        )
        result = request.execute()
        values = result.get('values', [])

        if not values:
            print("❌ 시트에 데이터가 없습니다.")
            return []

        # 4. Pandas로 변환하여 LangChain Document 객체로 만들기
        df = pd.DataFrame(values[1:], columns=values[0])
        documents = []
        for _, row in df.iterrows():
            # 모든 컬럼의 내용을 '컬럼명: 값' 형태의 문자열로 합침
            content = " / ".join([f"{col}: {val}" for col, val in row.items() if val])
            documents.append(Document(page_content=content, metadata={"source": sheet_name}))
        
        return documents
    except Exception as e:
        print(f"❌ 구글 시트 로드 중 오류 발생: {e}")
        return []

# 2. 벡터 DB 구축 함수
def build_vector_db_with_ollama(spreadsheet_id, sheet_name):
    # 데이터 가져오기
    print("📡 구글 시트에서 데이터를 불러오는 중...")
    docs = get_sheets_data(spreadsheet_id, sheet_name)
    
    if not docs:
        return None

    # 텍스트 청킹 (Chunking)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = text_splitter.split_documents(docs)

    # Ollama 임베딩 설정 (반드시 Ollama가 실행 중이어야 함)
    print("🧠 Ollama 임베딩 생성 및 벡터 DB 저장 중...")
    # 최신 방식: OllamaEmbeddings 클래스가 langchain_ollama에 위치함
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")
    
    # ChromaDB 저장
    vectorstore = Chroma.from_documents(
        documents=splits, 
        embedding=embeddings,
        persist_directory="./chroma_db_ollama"
    )
    
    print(f"✅ 완료! 총 {len(splits)}개의 데이터 조각이 './chroma_db_ollama'에 저장되었습니다.")
    return vectorstore


# --- 실행부 ---
# 구글 시트 URL의 /d/ 와 /edit 사이의 문자열이 SPREADSHEET_ID입니다.
# 예: https://docs.google.com/spreadsheets/d/1A_BcDeFgHiJkLmNoPqRs.../edit


MY_SPREADSHEET_ID = "18gO4C9nF6rR50UV_1P-583q4iOc3WCewx0JDAP9GuJo" 
SHNM = "서울시 응급실 위치 정보"

if __name__ == "__main__":
    build_vector_db_with_ollama(MY_SPREADSHEET_ID, SHNM)

