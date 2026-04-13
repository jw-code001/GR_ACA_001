from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def visual_debug_scraping():
    chrome_options = Options()
    # 🎯 [수정 1] 브라우저 창이 뜨도록 헤드리스 모드 해제
    # chrome_options.add_argument("--headless") 

    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        url = "https://fourlab.co.kr/"
        driver.get(url)
        
        # 🎯 [수정 2] 명시적 대기 (Explicit Wait)
        # 단순히 time.sleep을 하는 것보다, 특정 요소가 화면에 나타날 때까지 기다립니다.
        print("페이지 로딩 및 데이터 채워짐 대기 중...")
        wait = WebDriverWait(driver, 15)
        
        # 메인 배너 섹션이 나타날 때까지 기다림
        wait.until(EC.presence_of_element_located((By.ID, "w_mv")))
        
        # 🎯 [수정 3] 카페24 특유의 동적 클래스 확인
        # swiper-slide-active 등 실제 활성화된 데이터 위주로 탐색
        items = driver.find_elements(By.CSS_SELECTOR, "#w_mv .swiper-slide:not(.swiper-slide-duplicate)")
        
        print(f"찾은 실제 배너 개수: {len(items)}")
        
        for item in items:
            try:
                # [수정] p 태그가 있는지 확인 후 텍스트 추출
                p_tags = item.find_elements(By.TAG_NAME, "p")
                if p_tags:
                    title = p_tags[0].text.strip()
                    if title:
                        print(f"✅ 수집 성공: {title}")
                else:
                    # p 태그가 없는 슬라이드는 그냥 무시하고 넘어감
                    continue
            except Exception as e:
                # 개별 아이템 처리 중 오류 발생 시 출력 후 다음 아이템으로
                print(f"⚠️ 특정 아이템 건너뜀")

    except Exception as e:
        print(f"❌ 오류 발생: {e}")
    finally:
        # 결과를 눈으로 확인할 시간을 준 뒤 종료
        time.sleep(5)
        driver.quit()

if __name__ == "__main__":
    visual_debug_scraping()
