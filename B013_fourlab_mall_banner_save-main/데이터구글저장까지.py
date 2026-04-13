# 1. 셀레니움으로 9개 배너 전체 수집, 2. 오늘 날짜로 구글 시트 자동 생성, 3. 데이터 저장

import pandas as pd
import gspread
import time
import datetime
import os
from google.oauth2.service_account import Credentials
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# ==========================================
# [설정값] 본인의 환경에 맞게 수정하세요
# ==========================================
KEY_FILE = "../key/key.json"          # 서비스 계정 키 파일 경로
SHEET_NAME = "포랩메인기획전모집"       # 구글 스프레드시트 전체 이름
TARGET_URL = "https://fourlab.co.kr/" # 수집 대상 사이트
# ==========================================

def get_spreadsheet_client(keyfile):
    """구글 API 인증 및 클라이언트 반환"""
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file(keyfile, scopes=scopes)
    return gspread.authorize(creds)

def scrape_fourlab_banners():
    """포랩 사이트에서 메인 배너 리스트 수집"""
    chrome_options = Options()
    # 실행 과정을 보고 싶다면 아래 headless 줄을 주석 처리하세요
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    scraped_data = []
    
    try:
        print(f"1. {TARGET_URL} 접속 중...")
        driver.get(TARGET_URL)
        
        print("2. 동적 데이터 로딩 대기 (10초)...")
        time.sleep(10)
        
        # 메인 배너 섹션(#w_mv) 내의 모든 슬라이드 찾기
        parent_section = driver.find_element(By.CSS_SELECTOR, "#w_mv")
        items = parent_section.find_elements(By.CLASS_NAME, "swiper-slide")
        
        print(f"3. 데이터 추출 시작 (찾은 요소: {len(items)}개)...")
        
        for item in items:
            # Swiper 복제본 제외
            class_name = item.get_attribute("class")
            if "swiper-slide-duplicate" in class_name:
                continue
                
            try:
                # innerText를 사용하여 숨겨진 텍스트까지 수집
                title = item.find_element(By.TAG_NAME, "p").get_attribute("innerText").strip()
                content = item.find_element(By.TAG_NAME, "span").get_attribute("innerText").strip()
                
                if title:
                    # [수집시간, 제목, 내용] 순서로 리스트 생성
                    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    scraped_data.append([now, title, content])
            except:
                continue
                
    finally:
        driver.quit()
        
    return scraped_data

def save_to_google_sheet(scraped_list):
    """오늘 날짜의 시트를 생성하여 데이터 저장"""
    if not scraped_list:
        print("❌ 수집된 데이터가 없어 저장을 중단합니다.")
        return

    try:
        # 1. 구글 시트 열기
        client = get_spreadsheet_client(KEY_FILE)
        spreadsheet = client.open(SHEET_NAME)
        
        # 2. 오늘 날짜로 시트 이름 결정
        today_name = datetime.datetime.now().strftime('%Y-%m-%d')
        
        # 3. 시트 존재 여부 확인 및 생성
        try:
            worksheet = spreadsheet.worksheet(today_name)
            print(f"📂 기존 시트 '{today_name}'에 데이터를 추가합니다.")
        except gspread.exceptions.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title=today_name, rows="100", cols="5")
            # 새 시트면 헤더 추가
            worksheet.append_row(["수집시간", "배너타이틀", "컨텐츠"])
            print(f"✨ 새 시트 '{today_name}'를 생성했습니다.")

        # 4. 데이터 저장
        worksheet.append_rows(scraped_list)
        print(f"✅ 성공적으로 {len(scraped_list)}건의 데이터를 저장했습니다!")

    except Exception as e:
        print(f"❌ 구글 시트 저장 중 에러 발생: {e}")

if __name__ == "__main__":
    print("🚀 작업을 시작합니다.")
    
    # [Step 1] 스크래핑 실행
    data = scrape_fourlab_banners()
    print(f"📊 수집 완료: {len(data)}건의 데이터를 확보했습니다.")
    
    # [Step 2] 구글 시트 저장 실행
    save_to_google_sheet(data)
    
    print("🏁 모든 작업이 완료되었습니다.")