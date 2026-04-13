# pip install requests beautifulsoup4

import requests
from bs4 import BeautifulSoup

def get_simple_data():
    # 1. 접속할 웹사이트 주소
    url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=105" # IT/과학 뉴스
    
    # 2. 브라우저인 척 하기 (차단 방지용 헤더 추가)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    # 3. 페이지 요청 및 HTML 데이터 가져오기
    response = requests.get(url, headers=headers)
    
    # 4. BeautifulSoup 객체 생성 (HTML 파싱)
    soup = BeautifulSoup(response.text, "html.parser")
    # text 외 2개 처리확인하기, html.parser 외 2개 파서별 특징확인하기

    # 5. 원하는 데이터 추출 (태그와 클래스 찾기)
    # 예: 네이버 뉴스의 제목 태그가 'a'이고 클래스가 'sh_text_headline'인 경우
    titles = soup.select(".sh_text_headline") # 클래스 이름 앞에 마침표(.)를 붙입니다.

    print(f"--- 수집된 뉴스 제목 ({len(titles)}건) ---")
    
    scraped_results = []
    for idx, title in enumerate(titles, 1):
        text = title.get_text().strip() # 텍스트만 추출하고 공백 제거
        link = title['href']           # 링크 주소 추출
        
        print(f"{idx}. {text}")
        scraped_results.append({"순위": idx, "제목": text, "링크": link})
    
    return scraped_results

if __name__ == "__main__":
    data = get_simple_data()
    # 나중에는 여기서 gs_handler.save_data(ws, data)를 호출하게 됩니다!
