import json
import urllib.request
from bs4 import BeautifulSoup

def fetch_latest_lottery():
    # ดึงข้อมูลผลสลากกินแบ่งงวดล่าสุดจากเว็บข่าว
    url = "https://news.sanook.com/lotto/"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        # ดึงวันที่และตัวเลขรางวัล
        date_text = soup.find('h2', class_='lotto-check__title').text.strip()
        first_prize = soup.find('strong', class_='lotto-check__number').text.strip()
        
        # (หากดึงสำเร็จ จะนำมาสร้างโครงสร้างข้อมูล JSON)
        new_entry = {
            "date": date_text,
            "running": [first_prize],
            "running3Front": ["000", "000"],
            "running3Back": ["000", "000"],
            "running2Back": "00"
        }
        return new_entry
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

if __name__ == "__main__":
    print("Bot is checking for new lottery data...")
