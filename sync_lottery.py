import json
import re
import time
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}


def scrape_sanook_archive(max_pages=8):
    """ดึงข้อมูลผลสลากกินแบ่งรัฐบาลย้อนหลังจาก Sanook Archive (8 หน้า = ประมาณ 5 ปี / 120 งวด)"""
    all_results = []
    print(
        f"🚀 กำลังเริ่มดึงข้อมูลสลากย้อนหลังจาก Sanook Archive (รวม {max_pages}"
        " หน้า)..."
    )

    for page in range(1, max_pages + 1):
        url = (
            f"https://news.sanook.com/lotto/archive/p/{page}/"
            if page > 1
            else "https://news.sanook.com/lotto/archive/"
        )
        print(f"📖 กำลังดึงข้อมูลจากหน้า {page}: {url}")

        try:
            res = requests.get(url, headers=HEADERS, timeout=15)
            if res.status_code != 200:
                print(f"⚠️ หน้า {page} ตอบกลับด้วยสถานะ {res.status_code}")
                break

            soup = BeautifulSoup(res.text, "html.parser")

            # ค้นหาบล็อกการ์ดผลสลากในหน้า Archive
            articles = soup.find_all(
                "article", class_=re.compile(r"archive|lotto")
            )
            if not articles:
                articles = soup.select("div.archive-list__item") or soup.find_all(
                    "article"
                )

            for art in articles:
                try:
                    # 1. ดึงวันที่
                    title_tag = art.find(["h3", "h2", "a"])
                    if not title_tag:
                        continue

                    title_text = title_tag.get_text(strip=True)
                    date_match = re.search(
                        r"ตรวจหวย\s+(.*?)\s+ผลสลาก", title_text
                    ) or re.search(r"\d{1,2}\s+[ก-ฮ\.]+\s+\d{2,4}", title_text)
                    date_str = (
                        date_match.group(1)
                        if (date_match and "ตรวจหวย" in title_text)
                        else (
                            date_match.group(0) if date_match else title_text
                        )
                    )

                    # 2. ดึงข้อความทั้งหมดในการ์ด
                    body_text = art.get_text(" ", strip=True)

                    # รางวัลที่ 1
                    p1_match = re.search(
                        r"รางวัลที่\s*1\s*(?:รางวัลละ\s*[\d,]+\s*บาท)?\s*(\d{6})",
                        body_text,
                    )
                    first_prize = p1_match.group(1) if p1_match else ""

                    # เลขหน้า 3 ตัว (2 รางวัล)
                    front3_match = re.search(
                        r"เลขหน้า\s*3\s*ตัว\s*(?:2\s*รางวัลละ\s*[\d,]+\s*บาท)?\s*(\d{3})\s*(\d{3})",
                        body_text,
                    )
                    front_three = (
                        [front3_match.group(1), front3_match.group(2)]
                        if front3_match
                        else []
                    )

                    # เลขท้าย 3 ตัว (2 รางวัล)
                    last3_match = re.search(
                        r"เลขท้าย\s*3\s*ตัว\s*(?:2\s*รางวัลละ\s*[\d,]+\s*บาท)?\s*(\d{3})\s*(\d{3})",
                        body_text,
                    )
                    last_three = (
                        [last3_match.group(1), last3_match.group(2)]
                        if last3_match
                        else []
                    )

                    # เลขท้าย 2 ตัว
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
                except Exception:
                    continue

            time.sleep(0.5)  # พัก 0.5 วินาทีเพื่อไม่ให้เซิร์ฟเวอร์บล็อก

        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาดในหน้า {page}: {e}")
            break

    return all_results


def main():
    data = scrape_sanook_archive(max_pages=8)

    output = {
        "status": "online",
        "total_records": len(data),
        "history": data,
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(
        f"🎉 ดึงข้อมูลสำเร็จ! บันทึกลง data.json ทั้งหมด {len(data)} งวดเรียบร้อยแล้ว"
    )


if __name__ == "__main__":
    main()
