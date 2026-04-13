from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def scrape_and_print():
    # 1. 브라우저 옵션 설정
    chrome_options = Options()
    # 주석 처리하여 브라우저 창이 뜨도록 설정 (직접 확인용)
    # chrome_options.add_argument("--headless") 
    
    # 2. 드라이버 실행
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        url = "https://fourlab.co.kr/"
        print(f"\n[1/4] {url} 접속 중...")
        driver.get(url)
        
        # 3. 충분한 로딩 대기 (카페24 동적 데이터 로딩 시간)
        print("[2/4] 페이지 로딩 대기 중 (10초)... 브라우저를 확인하세요.")
        time.sleep(10) 
        
        # 4. 메인 배너 영역 조준 (#w_mv 섹션 안의 .swiper-slide)
        print("[3/4] 데이터 추출 시도 중...")
        # 부모 섹션인 #w_mv를 먼저 찾고 그 안의 슬라이드들을 찾습니다.
        try:
            parent = driver.find_element(By.ID, "w_mv")
            items = parent.find_elements(By.CLASS_NAME, "swiper-slide")
        except:
            print("❌ 메인 배너 섹션(#w_mv)을 찾지 못했습니다.")
            return

        scraped_results = []
        for item in items:
            # Swiper 무한 루프용 복제본은 제외
            class_attr = item.get_attribute("class")
            if "swiper-slide-duplicate" in class_attr:
                continue
            
            try:
                # <a> 태그 내부의 <p>와 <span> 태그 텍스트 추출
                title = item.find_element(By.TAG_NAME, "p").text
                content = item.find_element(By.TAG_NAME, "span").text
                
                if title: # 제목이 있는 경우만 리스트에 추가
                    scraped_results.append({
                        "title": title.strip(),
                        "content": content.strip()
                    })
            except:
                continue

        # 5. 콘솔에 결과 출력
        print("\n" + "="*60)
        print(f"📊 수집 완료: 총 {len(scraped_results)}개의 배너 데이터를 찾았습니다.")
        print("="*60)
        
        if not scraped_results:
            print("☹ 수집된 데이터가 없습니다. 선택자나 로딩 시간을 확인하세요.")
        else:
            for idx, res in enumerate(scraped_results, 1):
                print(f"[{idx}] 제목: {res['title']}")
                print(f"    내용: {res['content']}")
                print("-" * 60)

    except Exception as e:
        print(f"❌ 실행 중 오류 발생: {e}")
        
    finally:
        print("\n[4/4] 5초 후 브라우저를 종료합니다.")
        time.sleep(5)
        driver.quit()

if __name__ == "__main__":
    scrape_and_print()