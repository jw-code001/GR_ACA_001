# main_crawler.py
import gs_handler  # 위에서 만든 파일을 불러옵니다!

# 1. 설정값 준비
JSON_KEY = 'your-key.json'
SHEET_URL = 'https://docs.google.com/spreadsheets/d/your-id/edit'

def run_scraping():
    print("🔍 스크래핑을 시작합니다...")
    
    # [여기에 실제 스크래핑 로직이 들어갑니다]
    # 예시 데이터 (스크래핑 결과라고 가정)
    results = [
        {"날짜": "2026-03-12", "키워드": "캠핑 용품", "조회수": 1500},
        {"날짜": "2026-03-12", "키워드": "파이썬 기초", "조회수": 3200},
    ]
    
    # 2. 구글 시트 연결 (gs_handler의 함수 호출)
    ws = gs_handler.connect_sheet(JSON_KEY, SHEET_URL)
    
    # 3. 데이터 저장 (gs_handler의 함수 호출)
    gs_handler.save_data(ws, results)

if __name__ == "__main__":
    run_scraping()
