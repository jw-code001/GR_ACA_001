# selenium
- pip install selenium webdriver-manager

# 필수 메서드 TOP 5

① 브라우저 실행 및 이동
가장 먼저 브라우저를 켜고 특정 주소로 이동합니다.

driver.get("URL"): 해당 페이지로 이동합니다.

driver.maximize_window(): 창을 최대화합니다. (요소가 가려져서 클릭 안 되는 현상 방지)

driver.quit(): 브라우저와 드라이버를 완전히 종료합니다.

② 요소 찾기 (Locating Elements)
HTML 안에서 내가 원하는 버튼이나 글자를 찾는 과정입니다. By 모듈을 함께 사용합니다.

driver.find_element(By.ID, "id_name"): ID로 하나 찾기

driver.find_element(By.CLASS_NAME, "class_name"): 클래스명으로 찾기

driver.find_element(By.CSS_SELECTOR, "p.title"): CSS 선택자로 찾기 (가장 강력함)

find_elements(...): 조건에 맞는 모든 요소를 리스트 형태로 반환합니다. (상품 목록 수집 시 필수)

③ 요소 조작하기 (Interacting)
찾은 요소를 클릭하거나 글자를 입력합니다.

element.click(): 클릭합니다.

element.send_keys("검색어"): 텍스트를 입력합니다.

element.text: 해당 요소 내의 텍스트를 가져옵니다. (상품명, 가격 추출 시 사용)

element.get_attribute("href"): 링크 주소 같은 속성값을 가져옵니다.

④ 기다리기 (Waiting) - 중요!
웹페이지 로딩 속도보다 파이썬 코드 실행 속도가 훨씬 빠르기 때문에, 데이터가 나타날 때까지 기다려야 합니다.

time.sleep(3): 무조건 3초 대기 (가장 쉽지만 비효율적)

driver.implicitly_wait(10): 요소가 나타날 때까지 최대 10초 대기 (권장)
