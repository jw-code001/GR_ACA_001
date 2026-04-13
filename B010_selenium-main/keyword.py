# 검색 페이지 스크래핑 핵심 메서드 흐름
# 검색 페이지에서 상품명과 가격을 가져오는 흐름을 셀레니움 메서드와 연결해 보겠습니다.

# driver.get(f"https://www.kurly.com/search?keyword={search_word}")

# 원하는 검색어로 바로 접속합니다.

# driver.implicitly_wait(10)

# 검색 결과(상품 리스트)가 "은연중에" 나타날 때까지 기다립니다.

# driver.find_elements(By.CSS_SELECTOR, "a[class*='ProductItem']")

# 화면에 검색된 여러 개의 상품 카드들을 한꺼번에 리스트로 담습니다.

# for문과 find_element 조합

# 반복문을 돌며 각 상품 카드 안에서 이름(.name)과 가격(.price)을 하나씩 추출합니다.


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 검색어 설정
keyword = "고구마"
search_url = f"https://www.kurly.com/search?keyword={keyword}"

try:
    driver.get(search_url)
    driver.implicitly_wait(10) # 상품 목록이 뜰 때까지 대기

    # 상품 아이템들을 모두 찾음 (공통적인 클래스 패턴 활용)
    # 마켓컬리는 보통 css 선택자로 상품 레이아웃을 잡습니다.
    items = driver.find_elements(By.CSS_SELECTOR, "div[class*='StyledProductItem']")

    print(f"--- '{keyword}' 검색 결과 ---")
    for item in items[:5]: # 상위 5개만 확인
        name = item.find_element(By.CSS_SELECTOR, "span[class*='Name']").text
        price = item.find_element(By.CSS_SELECTOR, "span[class*='Price']").text
        print(f"상품명: {name} / 가격: {price}")

finally:
    time.sleep(2)
    driver.quit()
