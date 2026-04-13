# pip install selenium

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def test_fourlab_scraping():
    # 1. 크롬 옵션 설정
    chrome_options = Options()
    #chrome_options.add_argument("--headless")  # 창을 띄우지 않음 (보고 싶으면 이 줄 주석 처리)
    
    # 2. 드라이버 실행
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        url = "https://fourlab.co.kr/"
        print(f"1. {url} 접속 중...")
        driver.get(url)
        
        # 3. 동적 로딩 대기 (배너가 그려질 시간)
        print("2. 데이터 로딩 대기 중 (7초)...")
        time.sleep(7)
        
        # 4. 메인 배너 섹션(#w_mv) 안의 슬라이드들 찾기
        # ID가 w_mv인 섹션 내의 swiper-slide 클래스를 가진 모든 요소 탐색
        print("3. 데이터 추출 시작...")
        items = driver.find_elements(By.CSS_SELECTOR, "#mcategory a")
        
        results = []
        for item in items:
            # Swiper에서 무한루프용으로 복사한 슬라이드는 제외
            class_name = item.get_attribute("class")
            if "swiper-slide-duplicate" in class_name:
                continue
                
            try:
                # 제목(p)과 설명(span) 추출
                title = item.find_element(By.TAG_NAME, "p").text
                content = item.find_element(By.TAG_NAME, "span").text
                
                if title: # 내용이 있는 것만 수집
                    results.append({
                        "title": title.replace('\n', ' '), 
                        "content": content.replace('\n', ' ')
                    })
            except:
                continue
        
        # 5. 결과 출력
        print("\n" + "="*50)
        print(f"총 {len(results)}개의 배너를 찾았습니다.")
        print("="*50)
        for i, res in enumerate(results, 1):
            print(f"[{i}] 제목: {res['title']}")
            print(f"    내용: {res['content']}")
            print("-" * 50)

    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        
    finally:
        driver.quit()
        print("\n브라우저를 종료했습니다.")

if __name__ == "__main__":
    test_fourlab_scraping()