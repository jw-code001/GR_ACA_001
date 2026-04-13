# pip install selenium gspread pandas seaborn matplotlib streamlit

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import gspread
from google.oauth2.service_account import Credentials
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import streamlit as st
import time

# 1. 구글 시트 연결 설정 (수정: 워크시트가 아닌 '스프레드시트' 객체를 반환하도록 변경 가능)
def connect_google_spreadsheet(keyfile, googlesheet):
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file(keyfile, scopes=scopes)
    client = gspread.authorize(creds)
    return client.open(googlesheet) # 파일 객체 반환

# 2. 동적 객체 스크래핑 (Selenium)
def scrape_dynamic_data(webpageurl, delay, classnm, target1, target2):
    chrome_options = Options()
    chrome_options.add_argument("--headless") # 배포를 위해 헤드리스 모드 필수
    driver = webdriver.Chrome(options=chrome_options)
    
    driver.get(webpageurl) # 대상 URL
    time.sleep(delay) # 동적 콘텐츠 로딩 대기
    
    # 예시: 데이터 추출 로직 (대상 사이트에 맞게 수정 필요)
    items = driver.find_elements(By.CLASS_NAME, classnm)
    scraped_data = []
    for item in items:
        col1 = item.find_element(By.TAG_NAME, target1).text
        col2 = item.find_element(By.CLASS_NAME, target2).text
        scraped_data.append([time.strftime('%Y-%m-%d %H:%M:%S'), col1, col2])
    
    driver.quit()
    return scraped_data

import pandas as pd

def save_to_sheet(spreadsheet, sheet_name, data):
    """
    spreadsheet: gspread로 오픈한 스프레드시트 객체
    sheet_name: 기본으로 저장할 시트 이름
    data: 저장할 데이터 (리스트의 리스트 형태, 첫 번째 줄은 컬럼명이어야 함)
    """
    # 1. 데이터 프레임으로 변환하여 현재 수집된 컬럼명 확인
    new_df = pd.DataFrame(data[1:], columns=data[0])
    new_columns = list(new_df.columns)
    
    try:
        # 2. 기존 시트 열기 시도
        worksheet = spreadsheet.worksheet(sheet_name)
        existing_header = worksheet.row_values(1) # 첫 번째 줄(헤더) 가져오기
        
        # 3. 컬럼명 비교
        if existing_header == new_columns:
            # 컬럼명이 같으면 기존 시트에 추가 (헤더 제외 데이터만)
            worksheet.append_rows(new_df.values.tolist())
            print(f"'{sheet_name}' 시트에 데이터를 추가했습니다.")
        else:
            # 컬럼명이 다르면 새로운 시트 이름 생성 (예: 시트이름_20240316)
            new_sheet_name = f"{sheet_name}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}"
            new_ws = spreadsheet.add_worksheet(title=new_sheet_name, rows="100", cols="20")
            # 새 시트에는 헤더를 포함하여 전체 데이터 저장
            new_ws.append_rows(data)
            print(f"컬럼명이 달라 새로운 시트 '{new_sheet_name}'를 생성하여 저장했습니다.")
            
    except gspread.exceptions.WorksheetNotFound:
        # 시트가 아예 없는 경우 새로 생성 후 저장
        new_ws = spreadsheet.add_worksheet(title=sheet_name, rows="100", cols="20")
        new_ws.append_rows(data)
        print(f"'{sheet_name}' 시트가 없어 새로 생성 후 저장했습니다.")


# 4. Streamlit UI 및 시각화
def main():
    st.title("🚀 데이터 스크래핑 & 분석 대시보드")
    
    # 설정값 (실제 값으로 변경하세요)
    KEY_FILE = "./key/key.json"
    SHEET_NAME = "포랩메인기획전모집"
    DEFAULT_WS = "메인배너기획"

    # 시트 파일 연결
    try:
        spreadsheet = connect_google_spreadsheet(KEY_FILE, SHEET_NAME)
    except Exception as e:
        st.error(f"구글 시트 연결 실패: {e}")
        return

    if st.button("새 데이터 수집 시작"):
        with st.spinner("스크래핑 중..."):
            # 스크래핑 인자값 설정 (예시)
            new_data_list = scrape_dynamic_data(
                webpageurl="https://fourlab.co.kr/", 
                delay=3, 
                classnm="[df-banner-code='main-banner']", 
                target1=".swiper-slide  p", 
                target2=".swiper-slide  p + span"
            )
            
            # save_to_sheet 가 요구하는 형식: [ [컬럼명], [데이터1], [데이터2]... ]
            # scrape_dynamic_data의 결과에 헤더 추가
            header = ["수집시간", "배너타이틀", "컨텐츠"]
            final_data = [header] + new_data_list
            
            # 저장 로직 호출 (컬럼 다르면 새 시트 생성 포함)
            save_to_sheet(spreadsheet, DEFAULT_WS, final_data)
            st.success(f"데이터 처리가 완료되었습니다!")

    # 데이터 로드 및 시각화 (현재 활성화된 시트 기준)
    st.subheader("📊 수집 데이터 분석")
    try:
        # 가장 최근 시트 혹은 기본 시트 로드
        worksheet = spreadsheet.worksheet(DEFAULT_WS)
        raw_data = worksheet.get_all_records()
        df = pd.DataFrame(raw_data)

        if not df.empty:
            # 시각화 (컬럼명은 스크래핑 시 설정한 것과 맞춰야 함)
            fig, ax = plt.subplots(figsize=(10, 5))
            # 한글 깨짐 방지는 별도 설정 필요 (영어 컬럼 권장)
            sns.barplot(data=df, x='상품명', y='가격', ax=ax)
            plt.xticks(rotation=45)
            st.pyplot(fig)
            
            st.dataframe(df)
        else:
            st.info("시트에 데이터가 없습니다.")
    except Exception as e:
        st.warning("데이터를 불러올 수 없습니다. 수집을 먼저 진행하거나 시트 이름을 확인하세요.")

if __name__ == "__main__":
    main()