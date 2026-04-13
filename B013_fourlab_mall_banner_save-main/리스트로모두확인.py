from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def scrape_all_banners():
    chrome_options = Options()
    # chrome_options.add_argument("--headless") # 직접 보려면 주석 처리 유지
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        url = "https://fourlab.co.kr/"
        driver.get(url)
        print(f"\n[1/3] {url} 로딩 대기 (10초)...")
        time.sleep(10) # 모든 배너가 로드될 때까지 넉넉히 대기
        
        # 🎯 핵심: 부모 섹션(#w_mv) 내의 모든 swiper-slide를 리스트로 받음
        banner_elements = driver.find_elements(By.CSS_SELECTOR, "#w_mv .swiper-slide")
        
        final_list = []
        
        print(f"[2/3] 총 {len(banner_elements)}개의 슬라이드 요소를 발견했습니다. (복제본 포함)")

        for idx, item in enumerate(banner_elements):
            # 1. Swiper 복제본 제외 (무한 루프용 가짜 슬라이드)
            class_name = item.get_attribute("class")
            if "swiper-slide-duplicate" in class_name:
                continue
                
            try:
                # 2. 텍스트 추출 (innertext를 사용하면 숨겨진 텍스트도 더 잘 가져옵니다)
                title = item.find_element(By.TAG_NAME, "p").get_attribute("innerText").strip()
                content = item.find_element(By.TAG_NAME, "span").get_attribute("innerText").strip()
                
                # 데이터가 존재할 때만 리스트에 추가
                if title:
                    final_list.append([title, content])
                    print(f"✅ {len(final_list)}번 배너 수집 성공: {title[:20]}...")
            except:
                continue

        # 3. 최종 결과 콘솔 출력
        print("\n" + "="*60)
        print(f"📊 최종 수집 결과: 총 {len(final_list)}개 리스트")
        print("="*60)
        
        for i, data in enumerate(final_list, 1):
            print(f"{i}. 제목: {data[0]}")
            print(f"   내용: {data[1]}")
            print("-" * 60)

    finally:
        print("\n[3/3] 수집을 종료합니다.")
        time.sleep(5)
        driver.quit()

if __name__ == "__main__":
    scrape_all_banners()