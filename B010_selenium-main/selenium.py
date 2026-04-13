from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# 1. 드라이버 설정
options = webdriver.ChromeOptions()
# options.add_argument('--headless') # 창 안 띄우고 싶을 때 주석 해제
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 2. 페이지 접속
driver.get("https://www.kurly.com")
driver.implicitly_wait(10) # 요소를 찾을 때까지 최대 10초 기다려줌

try:
    # 3. 요소 탐색 (예: 검색창에 '고기' 입력)
    search_bar = driver.find_element(By.ID, "search")
    search_bar.send_keys("고기")
    search_bar.submit() # 엔터 입력 효과
    
    time.sleep(2) # 검색 결과 로딩 대기
    
    # 4. 정보 추출 (예: 첫 번째 상품명)
    first_item = driver.find_element(By.CSS_SELECTOR, ".product-name")
    print(f"첫 번째 상품: {first_item.text}")

finally:
    # 5. 종료
    driver.quit()
