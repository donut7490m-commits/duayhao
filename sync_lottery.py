import json
import os
import re
import urllib.request
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def fetch_sanook():
    """ แหล่งที่ 1: Sanook News """
    print("🔍 กำลังดึงข้อมูลจาก แหล่งที่ 1 (Sanook)...")
    url = "https://news.sanook.com/lotto/"
    req = urllib.request.Request(url, headers=HEADERS)
    html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    date_el = soup.find('h2', class_='lotto-check__title')
    numbers = [tag.text.strip() for tag in soup.find_all('strong', class_='lotto-check__number')]

    if date_el and len(numbers) >= 6:
        raw_date = date_el.text.strip()
        date_clean = re.sub(r'^(ผลสลากกินแบ่งรัฐบาล|ตรวจหวย)\s*', '', raw_date).strip()
        
        return {
            "date": date_clean,
            "running": [numbers[0]],
            "running3Front": [numbers[1], numbers[2]],
            "running3Back": [numbers[3], numbers[4]],
            "running2Back": numbers[5]
        }
    raise Exception("โครงสร้างหน้าเว็บ Sanook ไม่สมบูรณ์")

def fetch_kapook():
    """ แหล่งที่ 2: Kapook Lotto """
    print("🔍 กำลังดึงข้อมูลจาก แหล่งที่ 2 (Kapook)...")
    url = "https://lotto.kapook.com/"
    req = urllib.request.Request(url, headers=HEADERS)
    html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    date_el = soup.find('h1', class_='title') or soup.find('h2')
    numbers = [tag.text.strip() for tag in soup.find_all('div', class_='num') if tag.text.strip().isdigit()]

    if len(numbers) >= 6:
        date_text = date_el.text.strip() if date_el else "งวดล่าสุด"
        return {
            "date": date_text,
            "running": [numbers[0]],
            "running3Front": [numbers[1], numbers[2]],
            "running3Back": [numbers[3], numbers[4]],
            "running2Back": numbers[5]
        }
    raise Exception("โครงสร้างหน้าเว็บ Kapook ไม่สมบูรณ์")

def main():
    sources = [fetch_sanook, fetch_kapook]
    new_data = None

    # วนลูปดึงข้อมูลทีละแหล่ง ถ้าแหล่งแรกล่มจะสลับไปแหล่งถัดไปอัตโนมัติ
    for source_func in sources:
        try:
            new_data = source_func()
            print(f"✅ ดึงข้อมูลสำเร็จจาก {source_func.__name__}!")
            break
        except Exception as e:
            print(f"⚠️ {source_func.__name__} ขัดข้อง: {e}")

    if not new_data:
        print("❌ ไม่สามารถดึงข้อมูลจากทุกแหล่งได้ในขณะนี้")
        return

    # อ่านไฟล์ data.json เดิมที่มีอยู่
    file_path = "data.json"
    existing_json = {"status": "success", "response": []}

    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                existing_json = json.load(f)
        except Exception:
            pass

    # ตรวจสอบว่ามีข้อมูลของงวดนี้อยู่แล้วหรือยัง
    current_list = existing_json.get("response", [])
    if not current_list or current_list[0].get("date") != new_data["date"]:
        # เป็นงวดใหม่ -> แทรกไว้ด้านบนสุด
        current_list.insert(0, new_data)
        existing_json["response"] = current_list

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(existing_json, f, ensure_ascii=False, indent=2)
        print(f"🎉 อัปเดตข้อมูลหวยงวดใหม่เรียบร้อย: {new_data['date']}")
    else:
        print("ℹ️ ข้อมูลล่าสุดในระบบเป็นงวดปัจจุบันอยู่แล้ว ไม่ต้องอัปเดตเพิ่ม")

if __name__ == "__main__":
    main()
