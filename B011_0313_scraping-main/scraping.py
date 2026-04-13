import requests
from bs4 import BeautifulSoup

def get_simple_data(url, select):    
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }   
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")  

    titles = soup.select(select)
    print(f"--- 수집된 뉴스 제목 ({len(titles)}건) ---")
    
    scraped_results = [t.get_text().strip() for t in titles]  
    
    return scraped_results

if __name__ == "__main__":
    data = get_simple_data()
    print(data)