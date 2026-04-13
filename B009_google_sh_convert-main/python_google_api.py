from google.oauth2.service_account import Credentials
import gspread
import pandas as pd

# 1. 인증 및 구글 시트 연결
def connect_google_sheet(json_file, sheet_url):
    # 권한 범위 설정
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    # 서비스 계정 인증
    creds = Credentials.from_service_account_file(json_file, scopes=scopes)
    client = gspread.authorize(creds)
    
    # 시트 열기 (URL 또는 시트 이름 사용 가능)
    doc = client.open_by_url(sheet_url)
    return doc.get_worksheet(0)  # 첫 번째 시트 선택 파이썬 / 프로그램이 해당 시트를 제어할 수 있는 권한(Object)을 메모리에 들고 있다는 뜻
# worksheet = doc.worksheet("Sheet2") -> 시트이름을 정확히 알고 있는 경우

# 2. 크롤링 결과 저장 로직
def save_to_sheet(worksheet, data_list):
    # 데이터를 Pandas DataFrame으로 변환
    df = pd.DataFrame(data_list)
    
    # 구글 시트의 기존 내용을 지우고 새로운 데이터 쓰기
    # 데이터프레임을 리스트 형태로 변환 (헤더 포함)
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    print("성공적으로 구글 시트에 저장되었습니다.")

# df.columns.values.tolist() : 데이터프레임의 컬럼명(예: '상품명', '가격')만 뽑아서 하나의 리스트 ['순위', '상품명', '가격']
# df.values.tolist() 결과: [[1, '아이폰', '120만'], [2, '갤럭시', '110만']]

# --- 메인 실행 흐름 ---
if __name__ == "__main__":
    # 설정값 (본인의 환경에 맞게 수정하세요)
    JSON_KEY_FILE = 'your-service-account-key.json' 
    SHEET_URL = 'https://docs.google.com/spreadsheets/d/your-id/edit'
   # https://docs.google.com/spreadsheets/d/1GnY-UaiL4gsznS7vNVy43agfsPefu3IZhRm0lHyhklM/edit
    
    # 가상의 스크래핑 결과 데이터 (예시)
    scraped_data = [
        {"순위": 1, "상품명": "아이폰 15", "가격": "1,200,000"},
        {"순위": 2, "상품명": "갤럭시 S24", "가격": "1,150,000"},
    ]
    
    # 실행
    ws = connect_google_sheet(JSON_KEY_FILE, SHEET_URL)
    save_to_sheet(ws, scraped_data)
