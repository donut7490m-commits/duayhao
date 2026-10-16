import json
import re
import time
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}


def clean_date_str(raw_text):
    """สกัดเฉพาะวันที่ เช่น '16 ตุลาคม 2569' ออกมาจากข้อความ"""
    match = re.search(r"(\d{1,2}\s+[ก-ฮ\.]+\s+\d{2,4})", raw_text)
    if match:
        date_part = match.group(1)
        parts = date_part.split()
        if len(parts) == 3 and len(parts[2]) == 2:
            parts[2] = "25" + parts[2]
        return " ".join(parts)
    return None


def scrape_sanook_archive(max_pages=50):
    all_results = []
    seen_dates = set()

    print(
        "🚀 เริ่มดึงข้อมูลสลากย้อนหลังย้อนไปถึงปี 2550 จาก Sanook Archive (1 -"
        f" {max_pages} หน้า)..."
    )

    for page in range(1, max_pages + 1):
        # แก้ไข URL ให้ตรงกับโครงสร้างจริงของ Sanook (/archive/page/{page}/)
        url = (
            f"https://news.sanook.com/lotto/archive/page/{page}/"
            if page > 1
            else "https://news.sanook.com/lotto/archive/"
        )
        print(f"📖 [{page}/{max_pages}] กำลังดึงข้อมูลจาก: {url}")

        try:
            res = requests.get(url, headers=HEADERS, timeout=15)
            res.encoding = "utf-8"

            if res.status_code != 200:
                print(
                    f"⚠️ หน้า {page} ตอบกลับด้วย HTTP {res.status_code}"
                    " (ข้ามหน้านี้)"
                )
                continue

            soup = BeautifulSoup(res.text, "html.parser")
            articles = soup.find_all(
                "article", class_=re.compile(r"archive|lotto")
            ) or soup.select("div.archive-list__item")

            page_count = 0
            for art in articles:
                try:
                    title_tag = art.find(["h3", "h2", "a"])
                    if not title_tag:
                        continue

                    title_text = title_tag.get_text(strip=True)
                    date_str = clean_date_str(title_text)

                    if not date_str or date_str in seen_dates:
                        continue

                    body_text = art.get_text(" ", strip=True)

                    # 1. รางวัลที่ 1 (6 หลัก)
                    p1_match = re.search(
                        r"รางวัลที่\s*1\s*(?:รางวัลละ\s*[\d,]+\s*บาท)?\s*(\d{6})",
                        body_text,
                    )
                    first_prize = p1_match.group(1) if p1_match else ""

                    # 2. เลขหน้า 3 ตัว (ถ้ามี)
                    front3_match = re.search(
                        r"เลขหน้า\s*3\s*ตัว\s*(?:2\s*รางวัลละ\s*[\d,]+\s*บาท)?\s*(\d{3})\s*(\d{3})",
                        body_text,
                    )
                    front_three = (
                        [front3_match.group(1), front3_match.group(2)]
                        if front3_match
                        else []
                    )

                    # 3. เลขท้าย 3 ตัว
                    last3_match = re.search(
                        r"เลขท้าย\s*3\s*ตัว\s*(?:[\d]\s*รางวัลละ\s*[\d,]+\s*บาท)?\s*(\d{3})\s*(\d{3})(?:\s*(\d{3})\s*(\d{3}))?",
                        body_text,
                    )
                    last_three = []
                    if last3_match:
                        last_three = [
                            m for m in last3_match.groups() if m and len(m) == 3
                        ]

                    # 4. เลขท้าย 2 ตัว
                    last2_match = re.search(
                        r"เลขท้าย\s*2\s*ตัว\s*(?:1\s*รางวัลละ\s*[\d,]+\s*บาท)?\s*(\d{2})",
                        body_text,
                    )
                    last_two = last2_match.group(1) if last2_match else ""

                    if first_prize and last_two:
                        all_results.append({
                            "date": date_str,
                            "first_prize": first_prize,
                            "front_three": front_three,
                            "last_three": last_three,
                            "last_two": last_two,
                        })
                        seen_dates.add(date_str)
                        page_count += 1

                except Exception:
                    continue

            print(
                f"   └─ เพิ่มงวดใหม่จากหน้า {page}: {page_count} งวด (สะสมรวม"
                f" {len(all_results)} งวด)"
            )
            time.sleep(0.4)

        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาดในหน้า {page}: {e}")
            continue

    return all_results


def main():
    data = scrape_sanook_archive(max_pages=50)

    output = {
        "status": "online",
        "total_records": len(data),
        "history": data,
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(
        f"\n🎉 ดึงข้อมูลเสร็จสิ้น! ได้ข้อมูลย้อนหลังรวม {len(data)} งวด"
        " บันทึกลง data.json เรียบร้อยครับ"
    )


if __name__ == "__main__":
    main()
