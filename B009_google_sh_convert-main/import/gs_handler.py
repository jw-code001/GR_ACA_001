# gs_handler.py
from google.oauth2.service_account import Credentials
import gspread
import pandas as pd

def connect_sheet(json_file, sheet_url):
    scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_file(json_file, scopes=scopes)
    client = gspread.authorize(creds)
    return client.open_by_url(sheet_url).get_worksheet(0)

def save_data(worksheet, data_list):
    df = pd.DataFrame(data_list)
    # 기존 데이터 아래에 추가하고 싶으면 append_rows, 새로 다 덮으려면 update 사용
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    print("✅ 구글 시트 업데이트 완료!")

# 이 아래는 이 파일만 따로 테스트할 때만 실행됨
if __name__ == "__main__":
    print("이 파일은 모듈입니다. 다른 파일에서 import 해서 사용하세요.")
